class ConfigFileNotFound(Exception):
    def __init__(self, config_file_name, dirname):
        super().__init__(
            f' config file: {config_file_name} do not exists in root folder: '
            f'{dirname}'
        )


class ConfigKeyNotFound(Exception):
    def __init__(self, key_name, config_file_name):
        super().__init__(
            f'{key_name} do not exists in {config_file_name} config file'
        )
