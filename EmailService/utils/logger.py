import logging


class Logger(object):

    application = "EmailService"

    def __init__(self, name=__name__):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(formatter)

        self.logger.addHandler(stream_handler)
        self.__log_map = self.__get_log_map()

    def __get_log_map(self):
        """Supporting 3 log levels DEBUG, INFO, CRITICAL"""

        return {
            "debug": self.logger.debug,
            "info": self.logger.info,
            "critical": self.logger.critical
        }

    def log(self, log_type="info", msg_params=None):
        """Logs the message"""

        if msg_params:
            log_func = self.__log_map.get(log_type.lower(), self.__log_map['info'])
            log_func(Logger.generate_msg_str(msg_params))

    @staticmethod
    def generate_msg_str(msg_params):
        """Generates log string"""

        msg_str = ""
        msg_type = type(msg_params)

        if msg_type is dict:
            for key, val in msg_params.items():
                msg_str += str(key) + " === " + str(val) + " :::: "
            msg_str = msg_str[:-6]

        elif msg_type is list:
            for item in msg_params:
                msg_str += str(item) + " :::: "
            msg_str = msg_str[:-6]

        else:
            msg_str = str(msg_params)

        return msg_str
