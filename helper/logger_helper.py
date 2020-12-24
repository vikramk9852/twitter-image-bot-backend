import logging


def getLogger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    # if not len(logger.handlers):
    ch = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    ch.setFormatter(formatter)

    logger.addHandler(ch)
    return logger
