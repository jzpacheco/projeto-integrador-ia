from typing import Any, Dict


def create_simulation_ci(
        self,
        financing_options: Dict[str, Any],
        simulation_input:  Dict[str, Any],
        page: Page,
    ) -> Dict[str, Any]:
        results: List[Dict[str, Any]] = []

        url = self.ENDPOINTS.get('simulation')
        page.goto(url)
        page.wait_for_load_state('load')
        property_origin = {'residential': '033', 'commercial': '085'}
        person_type = simulation_input.person_type
        income = simulation_input.gross_monthly_income

        if person_type == 'pf':
            page.get_by_role('button', name='Pessoa Física').first.click()
        elif person_type == 'pj':
            income = simulation_input.company_revenue_last_month
            property_origin = {'residential': '112', 'commercial': '094'}
            page.get_by_role('button', name='Pessoa Jurídica').first.click()
        else:
            raise ValueError(f'Invalid person type: {person_type}')

        is_lot = False
        brb_correction_index = {'ipca': '207', 'tr': '206'}
        if simulation_input.property_type not in [
            'commercial_lot',
            'street_lot',
            'condo_lot',
        ]:
            if simulation_input.property_usage_type == 'commercial':
                brb_correction_index = {'ipca': '217', 'tr': '216'}
                page.get_by_role('button', name='Imóvel Comercial22222 Imóvel').click()#TODO:REMOVE THIS
                page.get_by_role('combobox', name='Origem do imóvel').select_option(
                    property_origin['commercial']
                )

            else:
                page.get_by_role(
                    'button', name='Imóvel Residencial Imóvel213131 Residencial'
                ).click()
                page.get_by_role('combobox', name='Origem do imóvel').select_option(
                    property_origin['residential']
                )
        else:
            is_lot = True
            page.get_by_role('button', name='Lote Regularizado222 Lote').click() #TODO:REMOVE THIS
            if person_type == 'pf':
                if simulation_input.property_usage_type == 'residential':
                    page.get_by_role('button', name='Residencial').click()
                else:
                    page.get_by_role('button', name='Comercial').click()

        page.locator('input[name="vlr_imovel"]').press_sequentially(
            str(int(simulation_input.property_value))
        )
        page.locator('input[name="vlr_financ"]').press_sequentially(
            str(int(simulation_input.amount_financed))
        )
        elem = page.get_by_placeholder('meses')
        elem.click()
        elem.fill(str(simulation_input.financing_term))
        if person_type == 'pf':
            elem = page.get_by_placeholder('DD/MM/AAAA')
            elem.click()
            elem.fill(simulation_input.birth_date)
        page.locator('input[name="vlr_rendafaturamento"]').press_sequentially(
            str(int(income))
        )

        def get_result(table, adjustment):
            correction_type = CorrectionTypes.tr
            correction_rate = 0
            if not is_lot and person_type != 'pj':
                if adjustment == 'pre_tr':
                    page.locator('#IndiceCorrecao').select_option(
                        brb_correction_index['tr']
                    )
                elif adjustment == 'pos_ipca':
                    correction_type = CorrectionTypes.ipca
                    page.locator('#IndiceCorrecao').select_option(
                        brb_correction_index['ipca']
                    )
                else:
                    raise ValueError(f'Invalid option: {adjustment}')
            # Submit
            page.get_by_role('button', name='Calcular').click()
            page.locator('#btn_1').click()
            # Wait load page for 10 seconds
            start_time = time.time()
            elapsed_time = 0

            while self.is_value_present_in_table(page, 'NaN') and elapsed_time < 10:
                page.wait_for_timeout(100)
                elapsed_time = time.time() - start_time
            data = {}

            df1 = self.get_dataframe_from_table(page)
            df1.columns = ['Descrição', 'Valor']
            # Remover o prefixo "R$" e quaisquer espaços em branco
            df1['Valor'] = df1['Valor'].replace(r'[R$\s.]', '', regex=True)
            df1['Valor'] = df1['Valor'].apply(clean_currency_value)
            interest_year = df1.iloc[4]['Valor']
            interest_month = annual_to_monthly_rate(interest_year)
            cet_year = df1.iloc[11]['Valor']
            cet_month = annual_to_monthly_rate(cet_year)

            # Second table
            page.click('button:has-text("Simulação das Parcelas")')
            page.wait_for_load_state('domcontentloaded')

            expected_name = f'brb_ci_{table}_simulation_{uuid.uuid4().hex}.pdf'
            file_name, file_b64 = self.download_pdf(
                page=page,
                expected_name=expected_name,
                resource=HealthcheckResources.get_file_simulation_ci,
            )

            df2 = self.get_dataframe_from_table(page, header=0)
            # Remover o prefixo "R$" e quaisquer espaços em branco
            for col in df2.columns:
                if col in ('Parcela N°'):
                    continue
                df2[col] = df2[col].replace(r'[R$\s.]', '', regex=True)
                df2[col] = df2[col].apply(clean_currency_value)

            first_payment = df2.iloc[0]['Prestação']
            last_payment = df2.iloc[-1]['Prestação']
            storage_data = page.evaluate(
                '() => { return JSON.parse(localStorage.getItem("persist:root")); }'
            )
            all_data = json.loads(storage_data.get('dadosResultadoSimulacao'))
            detail_data = all_data.get('dadosDetalhamentoSimulacao')
            amount_financed = float(detail_data.get('VA_FINANCIAMENTO'))

            data = {
                'first_payment': first_payment,
                'last_payment': last_payment,
                'interest_year': interest_year,
                'interest_month': interest_month,
                'cet_year': cet_year,
                'cet_month': cet_month,
                'amount_financed': amount_financed,
                'extra_data': storage_data,
                'correction_type': correction_type,
                'correction_rate': correction_rate,
                'file_name': file_name,
                'file_b64': file_b64,
            }

            return data

        amortization = financing_options['table']

        split_values = financing_options['adjustment'].split('_')

        if len(split_values) == 2:
            form_correction, correction_type = split_values
        else:
            form_correction, correction_type = split_values[0], None

        form_correction = 'variable' if form_correction == 'pos' else 'pre'
        correction_type = (
            CorrectionTypes[correction_type] if correction_type else CorrectionTypes.nan
        )
        tax_type = (
            TaxTypes.pre_fixed if form_correction == 'pre' else TaxTypes.variable_rate
        )
        try:
            data = get_result(**financing_options)
            results.append(
                SimulationResult(
                    bank=self.bank_context.bank_name,
                    status=SimulationBankStatus.completed,
                    first_payment=data['first_payment'],
                    last_payment=data['last_payment'],
                    interest_year=data['interest_year'],
                    interest_month=data['interest_month'],
                    cet_year=data['cet_year'],
                    cet_month=data['cet_month'],
                    amortization_system=AmortizationType[amortization],
                    tax_type=tax_type,
                    correction_type=correction_type,
                    correction_rate=data['correction_rate'],
                    financing_term=simulation_input.financing_term,
                    amount_financed=data['amount_financed'],
                    file_name=data['file_name'],
                    file_b64=data['file_b64'],
                    extra_data=data['extra_data'],
                )
            )

        except Exception:
            results.append(
                SimulationResult(
                    bank=self.bank_context.bank_name,
                    status=SimulationBankStatus.error,
                    first_payment=0,
                    last_payment=0,
                    interest_year=0,
                    interest_month=0,
                    cet_year=0,
                    cet_month=0,
                    amortization_system=AmortizationType[amortization],
                    correction_type=correction_type,
                    tax_type=tax_type,
                    financing_term=simulation_input.financing_term,
                    amount_financed=simulation_input.amount_financed,
                )
            )
            temp_send_error_alert_and_healthcheck(
                page=page,
                bank=FinancialInstituitionTypes.brb,
                resource=HealthcheckResources.create_simulation_ci,
                status='off',
                raw_payload=self.raw_payload,
            )

        return results
