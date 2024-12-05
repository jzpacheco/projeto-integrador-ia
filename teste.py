import io
import json
import locale
import re
import subprocess
from rpa_auto_fixer.core import RPAFixer
import time
import traceback
from typing import Any, Dict, List
import uuid
import pandas as pd
from bs4 import BeautifulSoup
from captura_envio import enviar_para_openai
from playwright.sync_api import sync_playwright, Page

from rpa.enums import CorrectionTypes, TaxTypes

def get_dataframe_from_table(page: Page, header: int = None):
    html_table = page.content()
    table = BeautifulSoup(html_table, 'html.parser').find('table')
    bin_table = io.StringIO(str(table))
    df = pd.read_html(bin_table, flavor='bs4', header=header)[0]
    return df

def clean_currency_value(value: str) -> float:
    """Limpa um valor de moeda e converte para float."""
    cleaned_value = re.sub(r'[^0-9,]', '', value)
    return locale.atof(cleaned_value)

def is_value_present_in_table(page: Page, value):
    # Encontrar todos os elementos td na tabela
    td_elements = page.locator(
        'table.MuiTable-root td.MuiTableCell-body'
    ).element_handles()

    for td_element in td_elements:
        # Obter o texto do elemento
        cell_text = td_element.text_content()

        # Verificar se o valor desejado está presente no texto
        if value in cell_text:
            return True


def create_simulation_ci(
        financing_options: Dict[str, Any],
        simulation_input:  Dict[str, Any],
        page: Page,
    ) -> Dict[str, Any]:
        results: List[Dict[str, Any]] = []

        url = 'https://sfhsimulador.brb.com.br/simuladorbrb/'
        page.goto(url)
        page.wait_for_load_state('load')
        property_origin = {'residential': '033', 'commercial': '085'}
        person_type = simulation_input['person_type']  # Acesso corrigido
        income = simulation_input['gross_monthly_income']

        if person_type == 'pf':
            page.get_by_role('button', name='Pessoa Física').first.click()
        elif person_type == 'pj':
            income = simulation_input['company_revenue_last_month']
            property_origin = {'residential': '112', 'commercial': '094'}
            page.get_by_role('button', name='Pessoa Jurídica').first.click()
        else:
            raise ValueError(f'Invalid person type: {person_type}')

        is_lot = False
        brb_correction_index = {'ipca': '207', 'tr': '206'}
        if simulation_input['property_type'] not in [
            'commercial_lot',
            'street_lot',
            'condo_lot',
        ]:
            if simulation_input['property_usage_type'] == 'commercial':
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
                if simulation_input['property_usage_type'] == 'residential':
                    page.get_by_role('button', name='Residencial').click()
                else:
                    page.get_by_role('button', name='Comercial').click()

        page.locator('input[name="vlr_imovel"]').press_sequentially(
            str(int(simulation_input['property_value']))
        )
        page.locator('input[name="vlr_financ"]').press_sequentially(
            str(int(simulation_input['amount_financed']))
        )
        elem = page.get_by_placeholder('meses')
        elem.click()
        elem.fill(str(simulation_input['financing_term']))
        if person_type == 'pf':
            elem = page.get_by_placeholder('DD/MM/AAAA')
            elem.click()
            elem.fill(simulation_input['birth_date'])
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
            while is_value_present_in_table(page, 'NaN') and elapsed_time < 10:
                page.wait_for_timeout(100)
                elapsed_time = time.time() - start_time
            data = {}

            df1 = get_dataframe_from_table(page)
            df1.columns = ['Descrição', 'Valor']
            # Remover o prefixo "R$" e quaisquer espaços em branco
            df1['Valor'] = df1['Valor'].replace(r'[R$\s.]', '', regex=True)
            df1['Valor'] = df1['Valor'].apply(clean_currency_value)
            interest_year = df1.iloc[4]['Valor']
            interest_month = 0
            cet_year = df1.iloc[11]['Valor']
            cet_month = 0

            # Second table
            page.click('button:has-text("Simulação das Parcelas")')
            page.wait_for_load_state('domcontentloaded')

            expected_name = f'brb_ci_{table}_simulation_{uuid.uuid4().hex}.pdf'
            # file_name, file_b64 = download_pdf(
            #     page=page,
            #     expected_name=expected_name,
            #     resource=HealthcheckResources.get_file_simulation_ci,
            # )

            df2 = get_dataframe_from_table(page, header=0)
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
            detail_data = all_data.get('dadosDetalhamecreate_simulation_cintoSimulacao')
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
                # 'file_name': file_name,
                # 'file_b64': file_b64,
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
            results.append(data)
        except Exception as e:
            print(e)

        return results
    

def run_rpa():
    with  sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=False,
            slow_mo=500,
        )
        context = browser.new_context(
            user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            # storage_state=(
            #     session_storage_path if os.path.exists(session_storage_path) else None
            # ),
        )
        page = context.new_page()
            
        try:
            input_data = {
                "external_id": "sm_lvw35tgmu67zb59zf",
                "loan_type": "CI",
                "person_type": "pf",
                "full_name": "joaozinho silva",
                "cpf_number": "646.927.000-09",
                "birth_date": "1960-01-12",
                "company_revenue_last_month": "0.00",
                "property_type": "apartment",
                "property_usage_type": "residential",
                "property_value": "750000.00",
                "entry_value": "450000.00",
                "amount_financed": "300000.00",
                "financing_term": 36,
                "gross_monthly_income": "30000",
                "property_region": "SP",
                "table": "sac",
                "adjustment": "pre_tr"
            }
            financing_options = {
                'table': input_data['table'],
                'adjustment': input_data['adjustment'],
            }
            result = create_simulation_ci(financing_options=financing_options, simulation_input=input_data, page=page)
            print('result', result)
        except Exception as e:
            html = page.content()
            fixer = RPAFixer(func_name='create_simulation_ci', kwargs={'financing_options': financing_options, 'simulation_input': input_data, 'page': page})
            fixer.analyse_and_fix(e, html)

if __name__ == '__main__':
    run_rpa()