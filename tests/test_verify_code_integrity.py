from utils.verify_code_integrity import VerifyCodeIntegrity

def test_is_code_safe():
    verifier = VerifyCodeIntegrity()
    
    # Testa se o código é seguro
    code = "print('Hello, world!')"
    assert verifier.is_code_safe(code) == True

    # Testa se o código é inseguro
    code = "os.system('rm -rf /')"
    assert verifier.is_code_safe(code) == False