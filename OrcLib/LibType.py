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


class WebDriverType:
    """
    驱动类型
    """
    # WEB 类型
    WEB = 'WEB'

    def __init__(self):
        pass

    @classmethod
    def all(cls):
        return cls.WEB,
