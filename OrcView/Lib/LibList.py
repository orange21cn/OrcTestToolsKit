# coding=utf-8
from PySide.QtCore import QAbstractListModel
from PySide.QtCore import Qt
from PySide.QtGui import QListView

from OrcLib.LibCommon import is_null
from OrcView.Lib.LibView import get_dict


class ViewList(QListView):
    """
    View of table
    """
    def __init__(self):

        QListView.__init__(self)

    def set_model(self, p_model):
        self.setModel(p_model)


class ModelList(QAbstractListModel):
    """
    Base model  Todo 是否是无用的 get_dict
    """
    def __init__(self):

        QAbstractListModel.__init__(self)

        self.__state_cond = {}  # now sql condition
        self.__state_data = [1,2,3,4]  # data

    def flags(self, index):

        flag = super(ModelList, self).flags(index)

        return flag

    def rowCount(self, parent):
        return len(self.__state_data)

    def data(self, index, role):

        if not index.isValid():
            return None

        if role == Qt.DisplayRole:

            return self.__state_data[index.row()]

        return None

    def usr_refresh(self):
        """
        Refresh the table when data changed
        :return:
        """
        # Clean condition
        for _key, value in self.__state_cond.items():
            if is_null(value):
                self.__state_cond.pop(_key)

        # Search
        # self.__state_data = orc_invoke(self.__interface['usr_search'], self.__state_cond)

        # Clean checked list
        self.__state_check = []

        self.reset()

    def usr_set_interface(self, p_interface):
        self.__interface = p_interface

    def usr_set_definition(self, p_def):
        """
        :param p_def:
        :return:
        """
        for t_field in p_def:

            if t_field["DISPLAY"]:

                self.__state_fields_name.append(t_field["NAME"])
                self.__state_fields_id.append(t_field["ID"])

                if "SELECT" == t_field["TYPE"]:
                    _res = get_dict(t_field["ID"])
                    self.__state_select[t_field["ID"]] = {}

                    for t_couple in _res:
                        self.__state_select[t_field["ID"]][t_couple.dict_value] = t_couple.dict_text

                if t_field["EDIT"]:
                    self.__state_edit_fields.append(t_field["ID"])
