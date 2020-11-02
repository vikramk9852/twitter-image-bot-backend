import logging

def initLogger():
    logger = logging.getLogger()
    if not len(logger.handlers):
        logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        ch.setFormatter(formatter)

        logger.addHandler(ch)
    return logger
