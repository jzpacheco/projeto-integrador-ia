import pytest
from playwright.sync_api import sync_playwright
from rpa.form_fill import fill_form

@pytest.fixture(scope='module')
def setup_playwright():
    # Inicializando o Playwright e configurando o navegador
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # headless=True para não abrir a janela do navegador
        page = browser.new_page()
        page.goto('https://www.roboform.com/filling-test-all-fields')  # URL de teste
        yield page
        browser.close()

def test_fill_form(setup_playwright):
    # Testa se o formulário foi preenchido corretamente sem lançar erros
    page = setup_playwright
    fill_form(page)

    # Verificar se os campos foram preenchidos corretamente
    assert page.input_value('input[name="01___title"]') == 'Mr.', "Título incorreto"
    assert page.input_value('input[name="02frstname"]') == 'John', "Primeiro nome incorreto"
    assert page.input_value('input[name="03middle_i"]') == 'A', "Middle initial incorreto"
    assert page.input_value('input[name="04lastname"]') == 'Doe', "Sobrenome incorreto"
    assert page.input_value('input[name="04fullname"]') == 'John A Doe', "Nome completo incorreto"
    assert page.input_value('input[name="05_company"]') == 'Acme Inc.', "Empresa incorreta"
    assert page.input_value('input[name="06position"]') == 'Software Engineer', "Posição incorreta"

    # Verificar o preenchimento de mais campos de acordo com o seu código
    assert page.input_value('input[name="24emailadr"]') == 'john.doe@example.com', "Email incorreto"
    assert page.input_value('input[name="31password"]') == 'securepassword', "Senha incorreta"
    assert page.input_value('input[name="41ccnumber"]') == '4111111111111111', "Número de cartão incorreto"
    assert page.input_value('input[name="43cvc"]') == '123', "CVC incorreto"

    # Continuar verificando outros campos de acordo com seu código...
