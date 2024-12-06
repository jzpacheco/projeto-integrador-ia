import traceback as tb

def format_traceback(self, exc):
        """
        Formata o traceback de uma exceção para enviar à LLM.

        Parameters:
            exc (Exception): A exceção que ocorreu.

        Returns:
            str: O traceback formatado.
        """
        formatted_tb = tb.format_exception(type(exc), exc, exc.__traceback__)
        return ''.join(formatted_tb)