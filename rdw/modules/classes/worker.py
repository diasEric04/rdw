from .config import ConfigController
from pathlib import Path
from .file import CommonFile
import os
from threading import Lock
import time
from .builder import Builder
from .messages import success_message, info_message


class WorkerController:
    def __init__(self, ROOT_PATH: Path, time_limit: int):
        config = ConfigController(ROOT_PATH)
        self.lock = Lock()
        self.time_limit = time_limit
        self.path_map = config.get_path_map()
        self.REACT_SRC_DIR = self.path_map['react_app_path'] / 'src'
        self.REACT_PUBLIC_DIR = self.path_map['react_app_path'] / 'public'

    def watch(self):
        success_message('watching react app...')
        while True:
            self.REACT_SRC_DIR.self_walk(
                func_files=self.func_watch_files
            )
            self.REACT_PUBLIC_DIR.self_walk(
                func_files=self.func_watch_files
            )

    def func_watch_files(self, root: str, file: str):
        common_file = CommonFile(Path(root, file))
        timestamp_now = time.time()
        timestamp_file = os.path.getmtime(common_file.str_path)
        seconds_dif = timestamp_now - timestamp_file
        if seconds_dif < self.time_limit:
            info_message('changes detected..')
            input('press [ENTER] to build')
            self.lock.acquire()
            self.run_builder()
            self.lock.release()

    def run_builder(self):
        builder = Builder(self.path_map)
        builder.run()
