import logging

from utils import exec_in_subprocess, get_current_file_content, VerifyCodeIntegrity
from .llm_handler import LLMHandler
from .error_handler import ErrorHandler

logging.basicConfig(level=logging.INFO)

class RPAFixer:
    def __init__(self, func_name, kwargs):
        self.func = func_name
        self.kwargs = kwargs
        self.llm_handler = LLMHandler()
        self.error_handler = ErrorHandler()

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
            error_details = self.error_handler.process_error(traceback, html, code)
            error_details.update({'func': self.func, 'kwargs': self.kwargs})
            explanation, code_snippet = self.llm_handler.generate_response(**error_details)
            return explanation, code_snippet
        except Exception as e:
            logging.error(f"Error while handling exception: {str(e)}")
            return f"Error: {str(e)}"

    def exec_fixed_code(self, fixed_code):
        """
        Execute the fixed code in a subprocess.

        Parameters:
            fixed_code (str): The code that has been fixed.

        Returns:
            str: Output or error details.
        """
        if not VerifyCodeIntegrity().is_code_safe(code=fixed_code):
            logging.error("The code provided failed security validation.")
            return "Error: Unsafe code detected."

        try:
            logging.info("Executing the fixed code in a subprocess.")
            result = exec_in_subprocess(fixed_code)
            return f"Execution result: {result}"
        except Exception as e:
            logging.error(f"Error while executing fixed code: {str(e)}")
            return f"Error: {str(e)}"

    def analyse_and_fix(self, traceback, html, code = None):
        """
        Analyse the error details and attempt to fix the issue.

        Parameters:
            traceback (str): The traceback of the exception.
            html (str): The HTML content of the page where the error occurred.
            code (str): The code that resulted in the exception.

        Returns:
            str: A message indicating the outcome of the process.
        """
        try:
            if code is None:
                logging.info("Capturando o conteúdo do arquivo atual.")
                code = get_current_file_content()
                
            logging.info("Analysing and fixing the error.")
            explanation,code_snippet = self.handle_exception(traceback, html, code)
            print('explanation:', explanation)
            print('code_snippet:', code_snippet)
            if not code_snippet:
                logging.warning("Invalid or incomplete suggestion from LLM.")
                return "Error: LLM returned invalid code."
            execution_result = self.exec_fixed_code(code_snippet)
            return execution_result, explanation
        except Exception as e:
            logging.error(f"Error in analyse_and_fix: {str(e)}")
            return f"Error: {str(e)}"
