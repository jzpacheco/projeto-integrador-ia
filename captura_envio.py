#Aplicado eng de prompt

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

    # Resumir HTML e traceback caso sejam muito longos.
    html_summary = dados['html'][:500] + '... [HTML truncado]' if len(dados['html']) > 500 else dados['html']
    traceback_summary = dados['traceback'][:500] + '... [Traceback truncado]' if len(dados['traceback']) > 500 else dados['traceback']

    # Mensagem detalhada para o prompt enviado à API.
    prompt = f"""
        Você é um assistente especializado em correção de código Python.
        Recebi um código com o seguinte erro:
        {traceback_summary}

        HTML capturado durante a execução:
        {html_summary}

        Código original:
        {dados['codigo']}

        Por favor, corrija o código acima. Certifique-se de que o código corrigido:
        - Seja funcional e pronto para execução.
        - Inclua comentários explicativos para qualquer mudança ou otimização realizada.
        - Siga boas práticas de programação.
        Retorne apenas o código corrigido, sem explicações adicionais.
        """

    # Enviando a requisição para a API.
    response = requests.post(
        url,
        headers=headers,
        json={
            "model": "gpt-4",  # Ajuste o modelo conforme necessário.
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2, 
            "max_tokens": 1500,  
            "top_p": 1.0,
        },
    )

    # Verifica se a requisição foi bem-sucedida.
