
class OrcException(Exception):
    pass


class OrcLibException(OrcException):
    pass


class OrcNetException(OrcException):
    pass


class OrcPostFailedException(OrcNetException):
    pass


class OrcDatabaseException(OrcException):
    pass


class OrcViewException(OrcException):
    pass


class OrcValueCantBeNull(OrcViewException):
    pass


class OrcApiException(OrcException):
    pass


class OrcApiModelFailException(OrcApiException):
    pass