import logging
from enum import Enum


class LoggingLevel(Enum):
    ERROR = 1
    CRITICAL = 2
    INFO = 3


class Logger:
    @staticmethod
    def set_configuration(logging_mode: str = "p") -> str:
        FileName = str()
        if logging_mode.lower().strip() == "f":
            FileName = "csen233midtermbalajimaheshkumaar.log"
            logging.basicConfig(level=logging.DEBUG, format="%(asctime)s  %(levelname)s %(message)s", datefmt="%d-%b-%y %H:%M:%S", filename=FileName, encoding="utf-8")
        else:
            logging.basicConfig(level=logging.DEBUG, format="%(asctime)s  %(levelname)s %(message)s", datefmt="%d-%b-%y %H:%M:%S")
        return FileName

    @staticmethod
    def logentry(message: str, entry_level: LoggingLevel = LoggingLevel.INFO):
        if entry_level == LoggingLevel.ERROR:
            logging.error(message)
        elif entry_level == LoggingLevel.CRITICAL:
            logging.critical(message)
        else:
            logging.info(message)
