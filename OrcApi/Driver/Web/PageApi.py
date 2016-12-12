from flask_restful import Resource

from OrcLib.LibLog import OrcLog
from OrcLib.LibNet import OrcParameter
from OrcLib.LibNet import orc_api
from PageBus import PageDefBus
from PageBus import PageDetBus


class PageDefListAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("resource.pages.api.def")
        self.__business = PageDefBus()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    @orc_api
    def post(self):
        """
        Add
        :return:
        """
        parameter = OrcParameter.receive_para()

        self.__logger.info("Add page, parameter is: %s" % parameter)

        return self.__business.bus_list_add(parameter)

    @orc_api
    def delete(self):
        """
        Delete
        :return:
        """
        parameter = OrcParameter.receive_para()

        self.__logger.info("Delete page, parameter is: %s" % parameter)

        return self.__business.bus_list_delete(parameter)

    @orc_api
    def get(self):
        """
        Search
        :return:
        """
        parameter = OrcParameter.receive_para()

        self.__logger.info("Search page, parameter is: %s" % parameter)

        return self.__business.bus_list_search(parameter)


class PageDefAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("resource.page.api.def")
        self.__business = PageDefBus()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    @orc_api
    def get(self, p_id):
        """
        Search
        :param p_id:
        :return:
        """
        self.__logger.info("Search page, parameter is: %s" % p_id)

        return self.__business.bus_search(p_id)

    @orc_api
    def put(self, p_id):
        """
        Update
        :param p_id:
        :return:
        """
        parameter = OrcParameter.receive_para()

        self.__logger.info("Update page, parameter is: %s, %s" % (p_id, parameter))

        return self.__business.bus_update(p_id, parameter)

    @orc_api
    def delete(self, p_id):
        """
        Delete
        :param p_id:
        :return:
        """
        self.__logger.info("Delete page, parameter is: %s" % p_id)

        return self.__business.bus_delete(p_id)


class PageDetListAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("resource.pages.api.det")
        self.__business = PageDetBus()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    @orc_api
    def post(self):
        """
        Add
        :return:
        """
        parameter = OrcParameter.receive_para()

        self.__logger.info("Add page, parameter is: %s" % parameter)

        return self.__business.bus_list_add(parameter)

    @orc_api
    def get(self):
        """
        Search
        :return:
        """
        parameter = OrcParameter.receive_para()

        self.__logger.info("Search page, parameter is: %s" % parameter)

        return self.__business.bus_list_search(parameter)

    @orc_api
    def delete(self):
        """
        Delete
        :return:
        """
        parameter = OrcParameter.receive_para()

        self.__logger.info("Delete page, parameter is: %s" % parameter)

        return self.__business.bus_list_delete(parameter)


class PageDetAPI(Resource):

    def __init__(self):

        self.__logger = OrcLog("resource.page.api.det")
        self.__business = PageDetBus()

    def dispatch_request(self, *args, **kwargs):
        return super(Resource, self).dispatch_request(*args, **kwargs)

    @orc_api
    def get(self, p_id):
        """
        Search
        :param p_id:
        :return:
        """
        self.__logger.info("Search page, parameter is: %s" % p_id)

        return self.__business.bus_search(p_id)

    @orc_api
    def put(self, p_id):
        """
        Update
        :param p_id:
        :return:
        """
        parameter = OrcParameter.receive_para()

        self.__logger.info("Update page, parameter is: %s, %s" % (p_id, parameter))

        return self.__business.bus_update(p_id, parameter)

    @orc_api
    def delete(self, p_id):
        """
        Delete
        :param p_id:
        :return:
        """
        self.__logger.info("Delete page, parameter is: %s" % p_id)

        return self.__business.bus_delete(p_id)
