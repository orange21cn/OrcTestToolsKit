# coding=utf-8
from DataDef import _data_def
from OrcLib.LibNet import orc_invoke
from OrcView.Lib.LibAdd import ViewAdd


class ViewDataAdd(ViewAdd):
    """
    View of table
    """
    def __init__(self, p_def):
        """
        :param p_def: table definition
        :return:
        """
        ViewAdd.__init__(self, p_def)

        i_base_url = 'http://localhost:5000/Data'
        self.__interface = {
            'usr_search': '%s/usr_search' % i_base_url,
            'usr_add': '%s/usr_add' % i_base_url,
            'usr_delete': '%s/usr_delete' % i_base_url,
            'usr_modify': '%s/usr_modify' % i_base_url
        }

        self.sig_submit.connect(self.__save)

    def set_type(self, p_type):

        _widget = self.__widgets["src_type"]["WIDGET"]

        _widget.set_data(p_type)
        _widget.setEnabled(False)

    def set_id(self, p_id):

        _widget = self.__widgets["src_id"]["WIDGET"]

        _widget.set_data(p_id)
        _widget.setEnabled(False)

    def __save(self, p_data):

        orc_invoke(self.__interface['usr_add'], p_data)


class ViewCommonDataAdd(ViewAdd):
    """
    View of table
    """
    def __init__(self):
        """
        :param p_def: table definition
        :return:
        """
        ViewAdd.__init__(self, _data_def)

        i_base_url = 'http://localhost:5000/Data'
        self.__interface = {
            'usr_search': '%s/usr_search' % i_base_url,
            'usr_add': '%s/usr_add' % i_base_url,
            'usr_delete': '%s/usr_delete' % i_base_url,
            'usr_modify': '%s/usr_modify' % i_base_url
        }
        self.__id = None
        self.sig_submit.connect(self.__save)

    def set_type(self, p_type):

        _widget = self.__widgets["src_type"]["WIDGET"]

        _widget.set_data(p_type)
        _widget.setEnabled(False)

    def set_path(self, p_path):

        _widget = self.__widgets["src_id"]["WIDGET"]

        _widget.set_data(p_path)
        _widget.setEnabled(False)

    def set_id(self, p_id):
        self.__id = p_id

    def __save(self, p_data):
        p_data["src_id"] = self.__id
        orc_invoke(self.__interface['usr_add'], p_data)