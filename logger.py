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


def log(text: str):
    logger.log(text)


def error(text: str):
    logger.error(text)


def info(text: str):
    logger.info(text)


def debug(text: str):
    logger.debug(text)
