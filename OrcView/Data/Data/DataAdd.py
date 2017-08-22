# coding=utf-8
from DataModel import DataModel
from OrcLib.LibProcess import get_mark
from OrcView.Lib.LibAdd import ViewNewAdd
from OrcView.Driver.Cmd.DataFlagSelector import DataFlagSelector
from OrcView.Case.Case.CaseSelector import CaseSelector
from OrcView.Batch.BatchSelector import BatchSelector


class DataAdder(ViewNewAdd):
    """
    View of table
    """
    def __init__(self):
        """
        :return:
        """
        ViewNewAdd.__init__(self, 'Data')

        self._model = DataModel()

        # +---- connection ----+
        # 控件被点击
        self.sig_clicked.connect(self._action)

        # 提交操作
        self.sig_submit.connect(self._save)

    def _action(self, p_flag):
        """
        控件被点击时的操作
        :param p_flag:
        :return:
        """
        if "data_flag" == p_flag:
            _data = DataFlagSelector.static_get_data(self.get_data('src_id'), self.get_data('src_type'))
            if _data:
                self.set_data('data_flag', (_data['id'], _data['flag']))

        elif 'src_id' == p_flag:
            src_type = self.get_data('src_type')
            if 'BATCH' == src_type:
                _data = BatchSelector.static_get_data()
                self.set_src_id(_data['id'])

            elif 'CASE' == src_type:
                _data = CaseSelector.static_get_data()
                self.set_src_id(_data['id'])

            else:
                pass

        else:
            pass

    def set_flag(self, p_data):
        """
        设置数据标识
        :param p_data:
        :return:
        """
        self.set_data('data_flag', (p_data['id'], get_mark(p_data['data_flag_type'], p_data['id'])))

    def set_src_type(self, p_type):
        """
        设置数据源类型, SELECT
        :param p_type:
        :return:
        """
        self.set_data("src_type", p_type)
        # self.set_enable("src_type", False)

    def set_src_id(self, p_id):
        """
        设置数据源标识, DISPLAY
        :param p_id:
        :return:
        """
        if p_id is None:
            return

        self.set_data("src_id", (p_id, get_mark(self.get_data('src_type'), p_id)))

    def _save(self, p_data):
        """
        保存数据
        :param p_data:
        :return:
        """
        self._model.service_add(p_data)

    @staticmethod
    def static_add_data(p_src_type=None, p_src_id=None, p_flag=None):
        """
        静态新增数据
        :param p_src_type:
        :param p_src_id:
        :param p_flag:
        :return:
        """
        view = DataAdder()

        if p_src_type is not None:
            view.set_src_type(p_src_type)

        if p_src_id is not None:
            view.set_src_id(p_src_id)

        if p_flag is not None:
            view.set_flag(p_flag)

        view.exec_()