# coding=utf-8
from PySide.QtGui import QWidget
from PySide.QtGui import QHBoxLayout
from PySide.QtGui import QVBoxLayout
from PySide.QtGui import QFormLayout
from PySide.QtGui import QGridLayout
from PySide.QtGui import QStackedWidget
from PySide.QtGui import QLineEdit
from PySide.QtGui import QGroupBox
from PySide.QtGui import QLabel
from PySide.QtCore import Signal as OrcSignal

from OrcLib import get_config

from OrcView.Lib.LibTree import ModelTree
from OrcView.Lib.LibTree import ViewTree
from OrcView.Lib.LibControl import ControlBase
from OrcView.Lib.LibView import WidgetFactory


class ConfMain(QWidget):
    """
    主界面
    """
    def __init__(self):

        QWidget.__init__(self)

        # 菜单栏
        self.menu_col = ConfMenuView()

        # 内容显示
        self.content_col = ConfContentView()

        # 布局
        layout_main = QHBoxLayout()
        layout_main.addWidget(self.menu_col)
        layout_main.addWidget(self.content_col)

        self.setLayout(layout_main)

        self.menu_col.sig_conf_now.connect(self.content_col.set_widget)


class ConfMenuControl(ControlBase):
    """
    菜单 control
    """
    def __init__(self):

        ControlBase.__init__(self, 'ConfMenu')


class ConfMenuModel(ModelTree):
    """
    菜单 model
    """
    def __init__(self):

        ModelTree.__init__(self, 'ConfMenu')

    def service_add(self, p_data):
        pass

    def service_delete(self, p_list):
        pass

    def service_update(self, p_data):
        pass

    def service_search(self, p_cond):

        return [
            dict(id='service', pid=None, name=u'服务'),
            dict(id='server', pid='service', name=u'服务器'),
            dict(id='client', pid='service', name=u'客户端'),
        ]


class ConfMenuView(ViewTree):
    """
    菜单界面
    """
    sig_conf_now = OrcSignal(str)

    def __init__(self):

        ViewTree.__init__(self, 'ConfMenu', ConfMenuModel, ConfMenuControl)

        self.model.mod_search(dict())

        self.clicked.connect(self.emit_id)

    def emit_id(self):
        self.sig_conf_now.emit(self.model.mod_get_current_data().content['id'])


class ConfContentView(QStackedWidget):
    """
    内容界面
    """
    def __init__(self):

        QStackedWidget.__init__(self)

        # 控件库
        widget_lib = dict(
            default=QWidget(),
            server=ServerConf(),
            client=ClientConf()
        )

        # 控件索引
        self.__widget_id_lib = [_id for _id in widget_lib]

        # 添加控件
        for _key in self.__widget_id_lib:
            self.addWidget(widget_lib[_key])

    def set_widget(self, p_id):
        """
        设置当前控件
        :param p_id:
        :return:
        """
        _index = 0 if p_id not in self.__widget_id_lib else self.__widget_id_lib.index(p_id)

        self.setCurrentIndex(_index)


class ClientConf(QWidget):
    """
    客户端配置
    """
    class Client(QGroupBox):

        def __init__(self, p_flag):

            QGroupBox.__init__(self)

            self._conf = get_config('client')

            self._desc, self._type, self._mode, self._ip, self._port =\
                [self.create_widget() for i in range(5)]

            self._desc.set_data()
            self._type.set_data()
            self._mode.set_data()
            self._ip.set_data()
            self._port.set_data()

            self.setTitle(self._conf.get_option(p_flag, 'name').decode('utf-8'))

            layout_main = QFormLayout()
            layout_main.addRow(u'描述: ', self._desc)
            layout_main.addRow(u'类型: ', self._type)
            layout_main.addRow(u'模式: ', self._mode)
            layout_main.addRow('IP: ', self._ip)
            layout_main.addRow(u'端口: ', self._port)

            layout_main.setSpacing(2)

            self.setLayout(layout_main)

        @staticmethod
        def create_widget():
            _widget = WidgetFactory.create_basic('LINETEXT')
            _widget.setDisabled(True)
            return _widget

    class Default(QGroupBox):

        def __init__(self):

            QGroupBox.__init__(self)

            self._conf = get_config('client')

            self.setTitle(self._conf.get_option('DEFAULT', 'name').decode('utf-8'))

            _local = WidgetFactory.create_basic('LINETEXT')
            _local.setDisabled(True)
            _local.set_data()

            _remote = WidgetFactory.create_basic('LINETEXT')
            _remote.set_data()

            layout_main = QHBoxLayout()
            layout_main.addWidget(QLabel(u'本地IP: '))
            layout_main.addWidget(_local)
            layout_main.addWidget(QLabel(u'远程IP: '))
            layout_main.addWidget(_remote)

            self.setLayout(layout_main)

            _remote.textChanged.connect(self.update_data)

        def update_data(self, p_data):
            self._conf.set_option('DEFAULT', 'remote', p_data)

    def __init__(self):

        QWidget.__init__(self)

        conf_list = ('BATCH', 'CASE', 'DATA',
                     'WEB_LIB', 'DRIVER', 'SERVER_WEB_001',
                     'MEM', 'RUN', 'RUN')

        layout_bottom = QGridLayout()
        for _index in range(len(conf_list)):
            layout_bottom.addWidget(self.Client(conf_list[_index]), _index / 3, _index % 3)

        widget_default = self.Default()

        layout_main = QVBoxLayout()
        layout_main.addWidget(widget_default)
        layout_main.addLayout(layout_bottom)

        layout_main.setSpacing(2)

        self.setLayout(layout_main)


class ServerConf(QWidget):
    """
    客户端配置
    """
    def __init__(self):

        QWidget.__init__(self)

        test = QLineEdit()

        layout_main = QHBoxLayout()
        layout_main.addWidget(test)

        self.setLayout(layout_main)


class DriverConf(QWidget):

    class Driver(QGroupBox):

        def __init__(self):

            QGroupBox.__init__(self)

            # 名称
            self._name = WidgetFactory.create_basic('LINE_EDIT')

            # 地址选择
            self._path = WidgetFactory.create_basic('LINE_EDIT')

            layout_main = QHBoxLayout()
            layout_main.addWidget(QLabel(u'名称'))
            layout_main.addWidget(self._name)
            layout_main.addWidget(QLabel(u'名称'))
            layout_main.addWidget(self._path)

            self.setLayout()

    class Default(QGroupBox):

        def __init__(self):

            QGroupBox.__init__(self)

            # 浏览器驱动选择

            # 环境选择

            # 临时文件选择

    def __init__(self):

        QWidget.__init__(self)

