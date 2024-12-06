import subprocess


def exec_in_subprocess(code):
    """
    Execute the given code in a subprocess.

    Parameters:
        code (str): The Python code to execute.

    Returns:
        str: Output or error message from the subprocess.
    """
    try:
        result = subprocess.run(
            ["python3", "-c", code],
            capture_output=True,
            text=True,
            check=True,
        )
        print('result:', result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error in subprocess: {e.stderr}"