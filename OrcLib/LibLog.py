import sys
import logging
import traceback
import StringIO


class OrcLog:
    """
    Logging
    """
    def __init__(self, p_mod):
        self.logger = logging.getLogger(p_mod)

    def debug(self, p_msg):
        self.logger.debug(p_msg)

    def info(self, p_msg):
        self.logger.info(p_msg)

    def warning(self, p_msg):
        self.logger.warning(p_msg)

    def step(self, p_msg=""):
        _func = sys._getframe().f_back.f_code.co_name
        self.logger.info("STEP %s %s" % (_func, p_msg))

    def error(self, p_msg):
        self.logger.error(p_msg)
        self.logger.error(self.get_trace())

    def critical(self, p_msg):
        self.logger.critical(p_msg)
        self.logger.critical(self.get_trace())

    @staticmethod
    def get_trace():
        _file = StringIO.StringIO()
        traceback.print_exc(file=_file)
        return _file.getvalue()
