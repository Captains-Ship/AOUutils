import crayons


class logger:
    def __init__(self):
        pass

    @staticmethod
    def log(text: str):
        print(f'[AOUutils/Log] {text}')

    @staticmethod
    def error(text: str):
        print(f'{crayons.red(f"[AOUutils/Error] {text}")}')

    @staticmethod
    def info(text: str):
        print(f'{crayons.yellow(f"[AOUutils/Info] {text}")}')

    @staticmethod
    def debug(text: str):
        print(f'{crayons.cyan(f"[AOUutils/Debug] {text}")}')

    @staticmethod
    def LG(text: str):
        print(f'{crayons.cyan(f"[AOUutils/Log] {text}")}')

    @staticmethod
    def I(text: str):
        print(f'{crayons.cyan(f"[AOUutils/Info] {text}")}')

    @staticmethod
    def ERR(text: str):
        print(f'{crayons.cyan(f"[AOUutils/Error] {text}")}')

    @staticmethod
    def DBG(text: str):
        print(f'{crayons.cyan(f"[AOUutils/Debug] {text}")}')


def log(text: str):
    print(f'[AOUutils/Log] {text}')


def error(text: str):
    print(f'{crayons.red(f"[AOUutils/Error] {text}")}')


def info(text: str):
    print(f'{crayons.green(f"[AOUutils/info] {text}")}')


def debug(text: str):
    print(f'{crayons.cyan(f"[AOUutils/Debug] {text}")}')


def warn(text: str):
    print(f'{crayons.yellow(f"[AOUutils/Warn] {text}")}')