




class Logging():

    def __init__(self):
        self.stop_logging_thread = False

    def _stop(self):
        self.stop_logging_thread = True

    def _ready(self):
        self.stop_logging_thread = False

    def create_log_thread(self):
        import threading
        log_thread = threading.Thread(target=self.log)
        log_thread.setDaemon(True)
        log_thread.start()

    def log(self):
        from time import sleep
        sleep(0.1)
        print("Hello, world! From before_log_while")
        while 1:
            if self.stop_logging_thread:
                break
            sleep(1)
            print("Hello, world! From in_log_while")