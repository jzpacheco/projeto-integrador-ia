from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=False)  # Altere para True para modo sem cabeça
    page = browser.new_page()
    page.goto('https://example.com')  # Exemplo de URL
    print(page.title())  # Exibe o título da página
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
