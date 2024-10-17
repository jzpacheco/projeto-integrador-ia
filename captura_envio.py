import traceback
import requests

# Função para capturar dados e lidar com possíveis erros.
def capturar_dados(codigo):
    try:
        # Aqui você deve colocar a lógica do seu RPA (Robotic Process Automation).
        exec(codigo)  # Executa o código que foi passado como argumento (pode gerar um erro).
    except Exception as e:
        # Captura o traceback do erro (informações detalhadas sobre o erro ocorrido).
        tb_str = traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
        traceback_str = ''.join(tb_str)  # Concatena a lista de strings em uma única string.

        # Captura o HTML da página (simulado aqui, você deve substituir pela lógica real de captura do HTML).
        html = "<html>... seu HTML aqui ...</html>"  # Exemplo de como o HTML seria capturado.

        # Retorna um dicionário com os dados capturados: HTML da página, traceback do erro e o código original.
        return {
            "html": html,
            "traceback": traceback_str,
            "codigo": codigo
        }

# Função para enviar dados capturados para a API da OpenAI.
def enviar_para_openai(dados):
    url = "https://api.openai.com/v1/chat/completions"  # URL da API da OpenAI.
    
    # Cabeçalhos da requisição, incluindo a chave da API e o tipo de conteúdo JSON.
    headers = {
        "Authorization": "Bearer sua_chave_api",  # Substitua pela sua chave da API.
        "Content-Type": "application/json"
    }
    
    print('headers', headers)  # Mostra os cabeçalhos da requisição para depuração.
    print('Enviando para OpenAI...')
    
    # Faz uma requisição POST para a OpenAI com os dados, incluindo o código que falhou.
    response = requests.post(
        url, 
        headers=headers, 
        json={
            "model": "gpt-4o-mini",  # Define o modelo que será usado (supondo que seja esse, ajuste se necessário).
            "messages": [
                {
                    "role": "user", 
                    "content": f'RETURN FIXED CODE ONLY, CODE THAT ITS FULL READY TO ONLY COPY AND EXECUTE WITH COMMAND EXEC() {str(dados)}'
                }
            ]
        }
    )
    
    # Verifica se a requisição foi bem-sucedida.
    if response.status_code == 200:
        # Se for bem-sucedida, extrai o conteúdo da resposta JSON e retorna o código corrigido.
        content = response.json().get('choices')[0].get('message').get('content')
        # Remove qualquer formatação de código Markdown ("```python") da resposta e retorna o código final.
        return content.strip().replace("```python", "").replace("```", "")
    else:
        # Caso ocorra um erro na requisição, exibe a mensagem de erro.
        print(f"Erro ao enviar para OpenAI: {response.status_code} - {response.text}")
        return None  # Retorna None se não houver sucesso.

# Função para tratar a resposta recebida da OpenAI.
def tratar_resposta(resposta):
    if resposta:
        # Se houver uma resposta válida, extrai o código corrigido da estrutura JSON.
        codigo_corrigido = resposta.get("choices")[0].get("message").get("content")
        
        # Exibe o código corrigido no console.
        print("Código Corrigido:")
        print(codigo_corrigido)
        
        # Retorna o código corrigido.
        return codigo_corrigido
    else:
        # Se não for possível obter uma resposta válida, exibe uma mensagem de erro.
        print("Não foi possível obter uma resposta válida da OpenAI.")
        return None  # Retorna None se não houver uma resposta válida.
