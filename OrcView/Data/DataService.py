from OrcLib.LibNet import OrcHttpNewResource


class DataService:

    def __init__(self):
        self.__resource_data = OrcHttpNewResource("Data")

    def usr_add(self, p_data):
        return self.__resource_data.post(p_data)

    def usr_delete(self, p_cond):
        self.__resource_data.delete(p_cond)

    def usr_update(self, p_cond):
        self.__resource_data.put(p_cond)

    def usr_search(self, p_cond):
        return self.__resource_data.get(p_cond)
