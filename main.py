from bot import TwitterWatcher
import time


def start():
    botWatcher = TwitterWatcher(pause=600)
    botWatcher.start()

    while True:
        try:
            time.sleep(10)
        except KeyboardInterrupt:
            botWatcher.stop()
            break


if __name__ == "__main__":
    start()
