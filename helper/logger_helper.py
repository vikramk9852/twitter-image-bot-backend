import logging

def initLogger():
    logger = logging.getLogger()
    if not len(logger.handlers):
        logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()

        # create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        # add formatter to ch
        ch.setFormatter(formatter)
        # add ch to logger
        logger.addHandler(ch)
    return logger
