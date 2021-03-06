from main.service.service import app
import configparser
import logging

config = configparser.ConfigParser()
config.read("config.ini")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)-12s %(levelname)-8s %(funcName)s() %(message)s",
)


def startApp():
    app.run(host='0.0.0.0', port=80)


if __name__ == "__main__":
    startApp()
