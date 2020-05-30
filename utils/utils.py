import datetime


class Logger:
    def __init__(self, option: str = "Muted", name="Untitled"):
        """
        Initialize a logger
        :param option: str ("Muted", "FileName" or "Print") or function
        """
        self._log = None
        self._name = name
        if isinstance(option, str):
            option = option.lower()
            if option == "print":
                self._log = lambda s: print(s)
            elif option == "muted":
                self._log = lambda s: s
            else:
                fn = option
                option = "file output"
                with open(fn, "w") as f:
                    f.write(f"###################Logger Initialized###################")

                def log(s):
                    with open(fn, "a") as fp:
                        fp.write(s)
                        
                self._log = log
        self.log(f"Logger Initialized - Name: {self._name} Mode: {option}")

    def log(self, *args, dt: datetime.datetime = None):
        if not dt:
            dt = datetime.datetime.now()
        s = " ".join([f'{arg}' for arg in args])
        message = f"[{dt.isoformat()}] {s}"
        return self._log(message)
        

