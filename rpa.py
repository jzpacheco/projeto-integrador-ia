from playwright.sync_api import sync_playwright

def fill_form(page):
    # Preencher campos de texto
    page.fill('input[name="01___title"]', 'Mr.')
    page.fill('input[name="02frstname"]', 'John')
    page.fill('input[name="03middle_i"]', 'A')
    page.fill('input[name="04lastname"]', 'Doe')
    page.fill('input[name="04fullname"]', 'John A Doe')
    page.fill('input[name="05_company"]', 'Acme Inc.')
    page.fill('input[name="06position"]', 'Software Engineer')
    page.fill('input[name="10address1"]', '123 Main St')
    page.fill('input[name="11address2"]', 'Apt 4B')
    page.fill('input[name="13adr_city"]', 'Metropolis')
    page.fill('input[name="14adrstate"]', 'NY')
    page.fill('input[name="15_country"]', 'USA')
    page.fill('input[name="16addr_zip"]', '10001')
    page.fill('input[name="20homephon"]', '555-1234')
    page.fill('input[name="21workphon"]', '555-5678')
    page.fill('input[name="22faxphone"]', '555-8765')
    page.fill('input[name="23cellphon"]', '555-4321')
    page.fill('input[name="24emailadr"]', 'john.doe@example.com')
    page.fill('input[name="25web_site"]', 'https://www.johndoe.com')

    # Preencher campos de senha e ID
    page.fill('input[name="30_user_id"]', 'johndoe123')
    page.fill('input[name="31password"]', 'securepassword')

    # Selecionar tipo de cartão de crédito
    page.select_option('select[name="40cc__type"]', value='9')

    # Preencher número do cartão de crédito e código de verificação
    page.fill('input[name="41ccnumber"]', '4111111111111111')
    page.fill('input[name="43cvc"]', '123')

    # Selecionar data de expiração do cartão de crédito
    page.select_option('select[name="42ccexp_mm"]', value='12')
    page.select_option('select[name="43ccexp_yy"]', value='2025')

    # Preencher nome do titular do cartão e outros detalhes
    page.fill('input[name="44cc_uname"]', 'John Doe')
    page.fill('input[name="45ccissuer"]', 'Bank of Example')
    page.fill('input[name="46cccstsvc"]', '555-6789')

    # Preencher dados pessoais
    page.fill('input[name="60pers_sex"]', 'Male')
    page.fill('input[name="61pers_ssn"]', '123-45-6789')
    page.fill('input[name="62driv_lic"]', 'D1234567')
    
    # Selecionar data de nascimento
    page.select_option('select[name="66mm"]', value='1')  # January
    page.select_option('select[name="67dd"]', value='1')  # 1st
    page.select_option('select[name="68yy"]', value='1990')  # 1990

    # Preencher idade, local de nascimento e renda
    page.fill('input[name="66pers_age"]', '34')
    page.fill('input[name="67birth_pl"]', 'Metropolis')
    page.fill('input[name="68__income"]', '75000')
    
    # Preencher mensagem personalizada e comentários
    page.fill('input[name="71__custom"]', 'This is a custom message.')
    page.fill('input[name="72__commnt"]', 'These are some comments.')

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        page = browser.new_page()
        page.goto('https://www.roboform.com/filling-test-all-fields')  # Substitua pela URL do seu formulário
        fill_form(page)
        # Você pode adicionar mais interações ou verificações aqui
        browser.close()

if __name__ == '__main__':
    main()