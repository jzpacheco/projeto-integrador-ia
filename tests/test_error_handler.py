import pytest
from error_handler import ErrorHandler  # Importe sua classe corretamente

# Teste 1: Verificar se process_error retorna a mensagem formatada corretamente com dados válidos
def test_process_error_with_valid_data():
    handler = ErrorHandler()

    # Entradas de exemplo
    traceback = "Traceback (most recent call last):\n  File 'script.py', line 10, in <module>\n    some_function()"
    html = "<html><body>Error Page</body></html>"
    code = "some_function()"

    expected_output = (
        "Traceback:\n"
        "Traceback (most recent call last):\n  File 'script.py', line 10, in <module>\n    some_function()\n"
        "HTML:\n<html><body>Error Page</body></html>\n"
        "Code:\nsome_function()"
    )

    # Verificando se a saída é igual ao esperado
    assert handler.process_error(traceback, html, code) == expected_output


# Teste 2: Verificar se process_error lida com entradas vazias
def test_process_error_with_empty_data():
    handler = ErrorHandler()

    # Entradas vazias
    traceback = ""
    html = ""
    code = ""

    expected_output = "Traceback:\n\nHTML:\n\nCode:\n"

    # Verificando se a saída é bem formatada mesmo com entradas vazias
    assert handler.process_error(traceback, html, code) == expected_output
