import ast

class VerifyCodeIntegrity:

    DANGEROUS_FUNCTIONS = [
        'open', 'os.system', 'subprocess', 'eval', 'exec', 'input', 'os.popen'
    ]

    def is_code_safe(self, code: str) -> bool:
        """
        Verifica se o código contém funções potencialmente perigosas.
        
        Parâmetros:
            code (str): O código que será validado.
            
        Retorna:
            bool: True se o código for seguro, False caso contrário.
        """
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id in self.DANGEROUS_FUNCTIONS:
                        return False
            return True
        except SyntaxError:
            return False