class FileNotFound(Exception):
    def __init__(self, file_name, basedir):
        super().__init__(
            f'file {file_name} not found {basedir}'
        )
