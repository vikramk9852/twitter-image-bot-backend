from bot import TwitterWatcher
from helper.logger_helper import initLogger
from server import initServer
import time


def start():
    initLogger()

    botWatcher = TwitterWatcher(pause=600)
    botWatcher.start()

    initServer()

    while True:
        try:
            time.sleep(10)
        except KeyboardInterrupt:
            botWatcher.stop()
            break


if __name__ == "__main__":
    start()
