from pathlib import Path
from shutil import rmtree, copy
import os
from .exceptions.directory import DirNotFound
from .file import CommonFile


class Directory:
    def __init__(self, *paths):
        dir_path = Path(*paths).resolve()
        self.dir_path = dir_path
        self.dir_name = dir_path.name
        self.str_path = str(dir_path)
        self.dirname = os.path.dirname(self.str_path)

        if not self.exists():
            raise DirNotFound(self.dir_name, self.dirname)

    def remove_all(self):
        rmtree(self.str_path)

    def remove_one(self, children: 'Directory | CommonFile'):
        if isinstance(children, (Directory, CommonFile)):
            children.self_remove()

    def self_walk(self, func_dirs=None, func_files=None):
        for root, dirs, files in os.walk(self.str_path):
            for dir in dirs:
                if func_dirs is not None:
                    func_dirs(root, dir)

            for file in files:
                if func_files is not None:
                    func_files(root, file)

    def self_list_dir(self, func_dirs=None, func_files=None):
        if not self.exists():
            return
        for item in os.listdir(self.str_path):
            item_full_path = Path(self.str_path, item)
            if os.path.isdir(str(item_full_path)):
                if func_dirs is not None:
                    func_dirs(item)
            elif os.path.isfile(str(Path(item_full_path))):
                if func_files is not None:
                    func_files(item_full_path)

    def append_file(self, file: 'CommonFile'):
        new_file_path = self.dir_path / file.file_name
        copy(file.file_path, str(new_file_path))
        return CommonFile(new_file_path)

    def self_remove(self):
        os.remove(self.str_path)

    def exists(self):
        return os.path.exists(self.str_path)

    def __truediv__(self, children_name: str):
        children_path = self.dir_path / children_name
        children_path.mkdir(exist_ok=True)
        return Directory(children_path)

    def __str__(self):
        return self.str_path

    def __repr__(self):
        class_name = type(self).__name__
        return f'{class_name}({self.str_path})'
