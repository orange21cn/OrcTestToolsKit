# coding=utf-8


class WebItemModeType:
    """
    操作项模式
    """
    # 操作
    OPERATE = 'OPERATE'

    # 检查
    CHECK = 'CHECK'

    def __init__(self):
        pass

    @classmethod
    def all(cls):
        return cls.OPERATE, cls.CHECK


class WebObjectType:
    """
    对象类型
    """
    # 页面
    PAGE = 'PAGE'

    # 窗口
    WINDOW = 'WINDOW'

    # 控件
    WIDGET = 'WIDGET'

    def __init__(self):
        pass

    @classmethod
    def all(cls):
        return cls.PAGE, cls.WINDOW, cls.WIDGET


class DriverType:
    """
    驱动类型
    """
    # WEB 类型
    WEB = 'WEB'

    # DAT 类型数据
    DATA = 'DATA'

    def __init__(self):
        pass

    @classmethod
    def all(cls):
        return cls.WEB, cls.DATA


class WebDriverOccupyStatusType:
    """
    驱动占用状态
    """
    # 等待状态
    WAITING = 'WAITING'

    # 占用状态
    OCCUPY = 'OCCUPY'

    def __init__(self):
        pass

    @classmethod
    def all(cls):
        return cls.WAITING, cls.OCCUPY


class WebDriverRunningStatusType:
    """
    驱动运行状态
    """
    # 空闲状态
    IDLE = 'IDLE'

    # 使用中状态
    BUSY = 'BUSY'

    # 出错状态
    ERROR = 'ERROR'

    def __init__(self):
        pass

    @classmethod
    def all(cls):
        return cls.IDLE, cls.BUSY, cls.ERROR


class RunRecordType:
    """
    运行结果状态
    """
    # 新建状态
    NEW = 'NEW'

    # 等待状态
    WAITING = 'WAITING'

    # 运行状态
    RUNNING = 'RUNNING'

    # 通过状态
    PASS = 'PASS'

    # 失败状态
    FAIL = 'FAIL'

    def __init__(self):
        pass

    @classmethod
    def all(cls):
        return cls.NEW, cls.WAITING, cls.RUNNING, cls.PASS, cls.FAIL

    @classmethod
    def from_bool(cls, p_status):
        if not isinstance(p_status, bool):
            return cls.FAIL

        return cls.PASS if p_status else cls.FAIL


class DataFlagType:
    """
    数据标识类型
    """
    # WEB 类型
    WEB = 'WEB'

    # DAT 类型数据
    DATA = 'DATA'

    def __init__(self):
        pass

    @classmethod
    def all(cls):
        return cls.WEB, cls.DATA


class DataScopeType:
    """
    数据作用域类型
    """
    # 计划数据
    BATCH = 'BATCH'

    # 用例数据
    CASE = 'CASE'

    # 步骤数据
    STEP = 'STEP'

    # 步骤项数据
    ITEM = 'ITEM'

    def __init__(self):
        pass

    @classmethod
    def all(cls):
        return cls.BATCH, cls.CASE, cls.STEP, cls.ITEM
