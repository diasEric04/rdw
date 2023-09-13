from threading import Thread


class MainThread:
    def __init__(self, worker_function, worker_args: tuple):
        self.t = Thread(target=worker_function, args=worker_args, daemon=True)

    def start_thread(self):
        self.t.start()
        try:
            while self.t.is_alive():
                pass
        except KeyboardInterrupt:
            pass
