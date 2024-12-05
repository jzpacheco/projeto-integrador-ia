import pytest
from unittest.mock import patch
from llm_handler import LLMHandler

# Teste quando a chave API está correta
def test_generate_response_with_valid_api_key():
    valid_api_key = "your-valid-api-key"  # Substitua com uma chave válida para teste

    handler = LLMHandler(api_key=valid_api_key)
    prompt = "What is the capital of France?"
    
    # Simular resposta esperada da API
    with patch('openai.Completion.create') as mock_create:
        mock_create.return_value = type('obj', (object,), {
            'choices': [{'text': 'Paris'}]
        })
        
        response = handler.generate_response(prompt)
        assert response == "Paris", f"Expected 'Paris', but got {response}"

# Teste quando a chave API não está configurada
def test_generate_response_without_api_key():
    handler = LLMHandler(api_key=None)  # Sem chave API
    
    with pytest.raises(ValueError, match="API key is required"):
        handler.generate_response("What is 2 + 2?")
