from pathlib import Path
import os
from typing import TYPE_CHECKING
from .exceptions.file import FileNotFound
from .exceptions.config import ConfigFileNotFound

if TYPE_CHECKING:
    from .directory import Directory


class File:
    def __init__(self, *paths):
        file_path = Path(*paths).resolve()
        self.file_path = file_path
        self.file_name = file_path.name
        self.str_path = str(file_path)
        _, self.extesion = os.path.splitext(self.file_name)
        self.dirname = os.path.dirname(self.str_path)

    def exists(self):
        return os.path.exists(self.str_path)


class ConfigFile(File):
    def __init__(self, *paths):
        super().__init__(*paths)
        if not self.exists():
            raise ConfigFileNotFound(self.file_name, self.dirname)


class CommonFile(File):
    def __init__(self, *paths):
        super().__init__(*paths)
        if not self.exists():
            raise FileNotFound(self.file_name, self.dirname)

    def update_text(self, func_read=None, func_write=None):

        if func_read is not None:
            with open(self.str_path, 'r', encoding='utf8') as file:
                func_read(file)

        if func_write is not None:
            with open(self.str_path, 'w', encoding='utf8') as file:
                func_write(file)

    def self_copy(self, directory: 'Directory'):
        return directory.append_file(self)

    def self_remove(self):
        os.remove(self.str_path)
