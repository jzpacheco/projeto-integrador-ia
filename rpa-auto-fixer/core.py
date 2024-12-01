import openai
import logging
from .llm_handler import LLMHandler
from .error_handler import ErrorHandler
# from .config import Config

#Configuração do log
logging.basicConfig(level=logging.INFO)

class RPAFixer:
    def __init__(self):
        self.llm_handler = LLMHandler()
        self.error_handler = ErrorHandler()
        # self.config = Config()

    def handle_exception(self, traceback, html, code):
        """
        Handle exceptions by interacting with LLM to suggest a fix.

        Parameters:
            traceback (str): The traceback of the exception.
            html (str): The HTML content of the page where the error occurred.
            code (str): The code that resulted in the exception.

        Returns:
            str: A suggestion from the LLM for fixing the error.
        """
        try:
            logging.info("Capturing exception details.")
            # Process the exception to prepare it for LLM interaction
            error_details = self.error_handler.process_error(traceback, html, code)
            
            # Interact with LLM to get a suggestion for the error
            suggestion = self.llm_handler.get_suggestion(error_details)
            
            # Return the suggestion received from the LLM
            return suggestion

        except Exception as e:
            logging.error(f"Error while handling exception: {str(e)}")
            return f"Error: {str(e)}"


# Função principal para testar a implementação
if __name__ == "__main__":
    # Exemplo de uso do RPAFixer
    rpa_fixer = RPAFixer()

    # Simulação de exceção
    traceback = "Traceback error"
    html = "<html>Error page</html>"
    code = "def buggy_function():\n    1 / 0  # Division by zero"

    suggestion = rpa_fixer.handle_exception(traceback, html, code)
    print(suggestion)