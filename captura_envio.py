import traceback
import requests

def capturar_dados(codigo):
    try:
        # Aqui você deve colocar a lógica do seu RPA
        exec(codigo)  # Executa o código do RPA (pode gerar um erro)
    except Exception as e:
        # Captura o traceback do erro
        tb_str = traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
        traceback_str = ''.join(tb_str)
        
        # Captura o HTML da página (exemplo)
        html = "<html>... seu HTML aqui ...</html>"  # Substitua pela lógica de captura do HTML
        
        return {
            "html": html,
            "traceback": traceback_str,
            "codigo": codigo
        }

def enviar_para_openai(dados):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": "Bearer sua_chave_api",  # Substitua com sua chave da API
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, json={"messages": [{"role": "user", "content": str(dados)}]})
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao enviar para OpenAI: {response.status_code} - {response.text}")
        return None

# Exemplo de código que pode causar um erro
codigo_rpa = """
def funcao_inexistente():
    pass

funcao_inexistente()  # Chamada para uma função que não existe para gerar erro
"""

# Captura de dados
dados = capturar_dados(codigo_rpa)
print(dados)  # Para verificar os dados capturados

# Envio dos dados capturados para a OpenAI
resposta_openai = enviar_para_openai(dados)
print(resposta_openai)  # Para verificar a resposta da OpenAI
