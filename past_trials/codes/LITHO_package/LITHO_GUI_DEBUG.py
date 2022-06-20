

class deco_SQLite:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):

        print(f"START {self.func.__name__}")

        try:
            self.func(self, *args, **kwargs)
        except Exception as ex:
            print(f"Exception occured : {ex}")

        print(f"END {self.func.__name__}")
