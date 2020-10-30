import threading
import time

from bot import TwitterHandleWatcher
from helper.logger_helper import initLogger
from app import initServer

def main():
    initLogger()
    botWatcher = TwitterHandleWatcher(pause=600)
    botWatcher.start()

    initServer()

    while True:
        try:
            time.sleep(10)
        except KeyboardInterrupt:
            botWatcher.stop()
            break

if __name__ == "__main__":
    main()