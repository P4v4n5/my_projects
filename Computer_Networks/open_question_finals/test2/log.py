import logging


class MyLogger:
    def __init__(self, log_file):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        self.formatter = logging.Formatter("%(asctime)s | %(funcName)s | line %(lineno)d | %(levelname)s | %(message)s")

        self.file_handler = logging.FileHandler(log_file, mode='w')
        self.file_handler.setLevel(logging.INFO)
        self.file_handler.setFormatter(self.formatter)

        self.logger.addHandler(self.file_handler)

        # Check if console handler already exists
        console_handler_exists = any(isinstance(handler, logging.StreamHandler) for handler in self.logger.handlers)

        if not console_handler_exists:
            self.console_handler = logging.StreamHandler()
            self.console_handler.setLevel(logging.INFO)
            self.console_handler.setFormatter(self.formatter)
            self.logger.addHandler(self.console_handler)

        # Disable propagation to the root logger
        self.logger.propagate = False

    def get_logger(self):
        return self.logger

    @staticmethod
    def setup_user1_logger():
        user1_logger = MyLogger('FIB_logfile_Pavan.txt')
        return user1_logger.get_logger()
