from pathlib import Path
from .modules.classes.worker import WorkerController
from .modules.classes.threads import MainThread
from .modules.classes.exceptions.config import (
    ConfigKeyNotFound, ConfigFileNotFound
)
from .modules.utils.help_text import config_keys_help_text


class ApplicationController:
    def __init__(self, ROOT_DIR: Path):
        self.worker = WorkerController(ROOT_DIR, 10)
        self.main_thread = MainThread(
            worker_function=self.worker.watch,
            worker_args=tuple()
        )

    def start_main_thread(self):
        self.main_thread.start_thread()


def app():
    ROOT_DIR = Path(__file__).resolve().parent
    application_thread = ApplicationController(ROOT_DIR)
    try:
        application_thread.start_main_thread()
    except ConfigKeyNotFound as e:
        print(e)
        e.add_note(
            config_keys_help_text()
        )
        raise e

    except ConfigFileNotFound as e:
        print(e)
        e.add_note(
            (
                'create config file in the root of the project'
                '\n\n'+config_keys_help_text()
            )
        )
        raise e


if __name__ == "__main__":
    app()
