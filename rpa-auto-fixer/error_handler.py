class ErrorHandler:
    def init(self):
        pass

    def process_error(self, traceback, html, code):
        """
        Process the error details to create a formatted error message for LLM.

        Parameters:
            traceback (str): The traceback of the exception.
            html (str): The HTML content of the page.
            code (str): The code that caused the exception.

        Returns:
            str: A formatted error message.
        """
        error_details = f"Traceback:\n{traceback}\nHTML:\n{html}\nCode:\n{code}"
        return error_details

import os
import openai
from config import settings