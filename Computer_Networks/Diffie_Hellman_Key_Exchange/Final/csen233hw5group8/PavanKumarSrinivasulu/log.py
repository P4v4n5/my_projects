import logging

class MyLogger:
    def __init__(self, log_file):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        self.formatter = logging.Formatter("%(asctime)s | %(funcName)s | line %(lineno)d | %(levelname)s | %(message)s")

        self.file_handler = logging.FileHandler(log_file, mode='w')
        self.file_handler.setLevel(logging.INFO)
        self.file_handler.setFormatter(self.formatter)

        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(logging.INFO)
        self.console_handler.setFormatter(self.formatter)

        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.console_handler)

        # Disable propagation to the root logger
        self.logger.propagate = False

    def get_logger(self):
        return self.logger

    @staticmethod
    def setup_user1_logger():
        user1_logger = MyLogger('csen233hw5SrinivasuluPavanKumar_User1.txt')
        return user1_logger.get_logger()

    @staticmethod
    def setup_user2_logger():
        user2_logger = MyLogger('csen233hw5SrinivasuluPavanKumar_User2.txt')
        return user2_logger.get_logger()
