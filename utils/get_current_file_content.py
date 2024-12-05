def get_current_file_content():
        import inspect
        current_file = inspect.stack()[2].filename
        print('current_file:', current_file)
        with open(current_file, 'r', encoding='utf-8') as file:
            return file.read()