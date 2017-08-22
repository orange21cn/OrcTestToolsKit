# coding=utf-8
from PySide.QtGui import QFormLayout
from PySide.QtGui import QWidget

from OrcLib import get_config
from OrcLib.LibProgram import OrcFactory

from OrcView.Lib.LibBaseWidget import WidgetCreator


class DataSrcBasic(QWidget):
    """
    基础控件,其他数据源的基类
    """
    def __init__(self):

        QWidget.__init__(self)

        # 配置
        self._configer = get_config('data_src')

        # 控件标识列表
        self._widget_index = list()

        # 控件库
        self._widget_lib = dict()

        # 名称控件
        self._add_widget('name', u'名称', WidgetCreator.create_line_text(), 0)

        # 描述控件
        self._add_widget('desc', u'描述', WidgetCreator.create_text_area(), 1)

        # 所有控件默认处于不可用状态
        self.set_enable(False)

    def init_ui(self):
        """
        初始化界面
        :return:
        """
        layout_main = QFormLayout()
        layout_main.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        layout_main.setContentsMargins(0, 0, 0, 0)

        for _key in self._widget_index:
            layout_main.addRow(self._widget_lib[_key][0], self._widget_lib[_key][1])

        self.setLayout(layout_main)

    def set_data(self, p_data):
        """
        设置数据
        :param p_data:
        :return:
        """
        if not isinstance(p_data, dict):
            return False

        data = OrcFactory.create_default_dict(p_data)
        for _key in self._widget_index:
            self.widget(_key).set_data(data.value(_key))

    def get_data(self):
        """
        获取数据
        :return:
        """
        return {_key: self.widget(_key).get_data() for _key in self._widget_index}

    def clean(self):
        """
        清空数据
        :return:
        """
        for _key in self._widget_index:
            self.widget(_key).set_data(None)

    def set_enable(self, p_flag):
        """
        设置控件是否可用
        :param p_flag:
        :return:
        """
        if not isinstance(p_flag, bool):
            return

        for _key in self._widget_index:
            self.widget(_key).setEnabled(p_flag)

    def widget(self, p_key):
        """
        获取对应 p_key
        :param p_key:
        :return:
        """
        return self._widget_lib[p_key][1]

    def _add_widget(self, p_key, p_name, p_widget, p_no):
        """
        增加控件
        :return:
        """
        self._widget_index.insert(p_no, p_key)
        self._widget_lib[p_key] = [p_name, p_widget]


class DataSrcEmpty(DataSrcBasic):
    """
    用于显示未定义的数据源
    """
    def __init__(self):

        DataSrcBasic.__init__(self)

        self.init_ui()


class DataSrcSqlite(DataSrcBasic):
    """
    mysql 界面
    """
    def __init__(self):

        DataSrcBasic.__init__(self)

        # 数据库文件
        self._add_widget('file', u'文件', WidgetCreator.create_line_text(), 1)

        # 初始化界面
        self. init_ui()


class DataSrcMySql(DataSrcBasic):
    """
    mysql 界面
    """
    def __init__(self):

        DataSrcBasic.__init__(self)

        # 主机
        self._add_widget('host', u'主机', WidgetCreator.create_line_text(), 1)

        # 数据库
        self._add_widget('database', u'数据库', WidgetCreator.create_line_text(), 2)

        # 用户名
        self._add_widget('user', u'用户名', WidgetCreator.create_line_text(), 3)

        # 密码
        self._add_widget('password', u'密码', WidgetCreator.create_line_text(), 4)

        # 初始化界面
        self. init_ui()


class DataSrcOracle(DataSrcBasic):
    """
    mysql 界面
    """
    def __init__(self):

        DataSrcBasic.__init__(self)

        # IP
        self._add_widget('ip', u'IP', WidgetCreator.create_line_text(), 1)

        # 端口
        self._add_widget('port', u'端口', WidgetCreator.create_line_text(), 2)

        # 用户名
        self._add_widget('user', u'用户名', WidgetCreator.create_line_text(), 3)

        # 密码
        self._add_widget('password', u'密码', WidgetCreator.create_line_text(), 4)

        # 服务
        self._add_widget('service', u'服务', WidgetCreator.create_line_text(), 5)

        # 初始化界面
        self.init_ui()
