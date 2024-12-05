class ErrorHandler:
    def __init__(self):
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
        return {"traceback_details": traceback, "html_snippet": html, "code_snippet": code}