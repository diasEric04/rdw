import json
from pathlib import Path
from .exceptions.config import ConfigKeyNotFound
from .directory import Directory
from .file import ConfigFile

CONFIG_FILENAME = 'rdw-config.json'
CK_DJANGO_ROOT_PATH = 'django_root_path'
CK_REACT_ROOT_PATH = 'react_root_path'
CK_REACT_APP_PATH = 'react_app_path'
CK_DJANGO_APP_PATH = 'django_app_path'

cks = [
    CK_DJANGO_ROOT_PATH, CK_REACT_ROOT_PATH,
    CK_REACT_APP_PATH, CK_DJANGO_APP_PATH
]


class ConfigController:
    def __init__(self, ROOT_DIR: Path):
        config_path = ROOT_DIR / CONFIG_FILENAME
        self.config_path = ConfigFile(config_path)
        with open(self.config_path.str_path, 'r+', encoding='utf8') as cfg:
            data_config: dict = json.load(cfg)

            for ck in cks:
                if ck not in data_config.keys():
                    raise ConfigKeyNotFound(ck, CONFIG_FILENAME)

            # aqui o arquivo de configuração existe, e todas as
            # cks que eu preciso

            self.DJANGO_ROOT_PATH = Directory(
                str(data_config.get(CK_DJANGO_ROOT_PATH))
            )

            self.REACT_ROOT_PATH = Directory(
                str(data_config.get(CK_REACT_ROOT_PATH))
            )

            self.REACT_APP_PATH = Directory(
                str(data_config.get(CK_REACT_APP_PATH)).replace(
                    '$react_root_path', self.REACT_ROOT_PATH.str_path
                )
            )

            self.DJANGO_APP_PATH = Directory(
                str(data_config.get(CK_DJANGO_APP_PATH)).replace(
                    '$django_root_path', self.DJANGO_ROOT_PATH.str_path
                )
            )

    def get_path_map(self) -> dict[str, Directory]:
        return {
            CK_DJANGO_ROOT_PATH: self.DJANGO_ROOT_PATH,
            CK_REACT_ROOT_PATH: self.REACT_ROOT_PATH,
            CK_REACT_APP_PATH: self.REACT_APP_PATH,
            CK_DJANGO_APP_PATH: self.DJANGO_APP_PATH,
        }
