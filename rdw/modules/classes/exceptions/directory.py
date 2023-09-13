class DirNotFound(Exception):
    def __init__(self, dir_name, dirname):
        super().__init__(
            f'directory {dir_name} not found {dirname}'
        )
