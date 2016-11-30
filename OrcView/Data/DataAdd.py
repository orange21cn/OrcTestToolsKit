# coding=utf-8
from PySide.QtCore import Signal as OrcSignal

from OrcView.Lib.LibViewDef import def_view_data
from OrcView.Lib.LibAdd import ViewAdd

from DataService import DataService


class ViewDataAdd(ViewAdd):
    """
    View of table
    """
    sig_data_flag = OrcSignal()

    def __init__(self):
        """
        :return:
        """
        ViewAdd.__init__(self, def_view_data)

        self.__service = DataService()
        self.__id = None

        self.sig_submit.connect(self.__save)

    def set_type(self, p_type):

        self.set_data("src_type", p_type)
        self.set_enable("src_type", False)

    def set_path(self, p_path):
        self.set_data("src_id", p_path)
        self.set_enable("src_id", False)

    def set_id(self, p_id):
        self.__id = p_id

    def __save(self, p_data):
        p_data["src_id"] = self.__id
        self.__service.usr_add(p_data)
