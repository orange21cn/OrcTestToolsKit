import json
import os

from OrcCaseMag import OrcCaseDef
from OrcCaseMag import OrcCaseDet
from OrcCaseMag import OrcItem
from OrcCaseMag import OrcStepDet
from OrcDataMag import DataMag
from OrcLib.LibDriver import OrcDriver
from OrcLib.LibTableBase import TestBase

from OrcLib.LibSelenium import slm_click
from OrcLib.LibSelenium import slm_input
from OrcFrame.OrcBatch.OrcBatchDet.BatchDetData import OrcBatchDet
from OrcFrame.OrcLib.LibCommon import gen_date_str


class OrcLaunch(TestBase):

    def __init__(self):

        TestBase.__init__(self)

        self.__batch = OrcBatchDet()
        self.__group = OrcCaseDef()
        self.__case = OrcCaseDet()
        self.__step = OrcStepDet()
        self.__item = OrcItem()

        self.__data = DataMag()
        self.__driver = OrcDriver()

        # Create test folder
        self.__home_fld = self._config.get_config("DEFAULT_RESULT_FOLD") + "/" + gen_date_str()
        os.makedirs(self.__home_fld)

    def launch_batch(self, p_batch_id):
        """
        Get all case/group of batch and involve run_case
        :param p_batch_id:
        :return:
        """
        self._share.set_data("BATCH_ID", p_batch_id)

        for t_case_id in self.__batch.usr_get_list(p_batch_id):
            self.run_case(t_case_id)

    def run_case(self, p_group_id):
        """
        Get all step of case and invoke __run_step
        :param p_group_id:
        :return:
        """
        for t_case_id in self.__group.get_children(p_group_id):

            self._share.set_data("CASE_ID", t_case_id)

            for t_step_id in self.__case.get_step_list(t_case_id):
                self.__run_step(t_step_id)

    def __run_step(self, p_step_id):
        """
        Get all step of step and run __run_item
        :return:
        """
        self._share.set_data("STEP_ID", p_step_id)
        for t_item_id in self.__step.get_item_list(p_step_id):

            self.__run_item(t_item_id)

        # Screen saver
        screen_file = self.get_folder("CASE") + "\\" + str(p_step_id) + ".png"
        self.__driver.driver_web.object.save_screen(screen_file)

    def __run_item(self, p_item_id):

        """
        Run a item
        :rtype: object
        """
        self._share.set_data("ITEM_ID", p_item_id)

        _type = self.__item.get_type(p_item_id)

        if "WEB" == _type:
            self.__run_web(p_item_id)
        elif "WEBSERVICE" == _type:
            self.__run_webservice(p_item_id)
        elif "ANDROID" == _type:
            self.__run_android(p_item_id)
        elif "IOS" == _type:
            self.__run_ios(p_item_id)
        else:
            pass

    def __run_web(self, p_item_id):
        """
        Run web item and record the result
        :return:
        """
        i_item_mode = self.__item.get_mode(p_item_id)
        i_item_operate = json.loads(self.__item.get_operate(p_item_id))

        if not self.__driver.driver_web.state:
            self.__driver.driver_web.create("CHROME")

        if "OPERATE" == i_item_mode:

            t_object = self.__driver.driver_web.object.get_item(i_item_operate["OBJECT"])

            if "INPUT" == i_item_operate["TYPE"]:
                t_data = self.__get_data(i_item_operate["OBJECT"])
                slm_input(t_object, t_data)

            elif "SUBMIT" == i_item_operate["TYPE"]:
                slm_click(t_object)
            else:
                pass  # Todo

        elif "CHECK" == i_item_mode:
            pass
        else:
            pass

    def __run_webservice(self, p_item_id):
        pass

    def __run_android(self, p_item_id):
        pass

    def __run_ios(self, p_item_id):
        pass

    def __get_data(self, p_data_flg):

        # Get item data
        res_value = self.__data.get_data(self._share.get_data("ITEM_ID"), p_data_flg)

        # Get step data
        if not res_value:
            res_value = self.__data.get_data(self._share.get_data("STEP_ID"), p_data_flg)

        # Get case group data
        t_case_id = self._share.get_data("CASE_ID")

        while not res_value:

            res_value = self.__data.get_data(t_case_id, p_data_flg)

            t_case_id = self.__group.get_parent_id(t_case_id)
            if not t_case_id:
                break

        # Get batch data
        if not res_value:
            res_value = self.__data.get_data(self._share.get_data("BATCH_ID"), p_data_flg)

        # Get run time data
        if not res_value:
            res_value = self._share.get_data(p_data_flg)

        if not res_value:
            pass  # Todo

        return res_value

    def get_folder(self, p_flag):

        t_folder = self.__home_fld

        if "BATCH" == p_flag:
            t_folder += "\\" + self._share.get_data("BATCH_ID")
        elif "CASE" == p_flag:
            t_folder += "\\" + self._share.get_data("BATCH_ID") +\
                        "\\" + self._share.get_data("CASE_ID")

        if not os.path.exists(t_folder):
            os.makedirs(t_folder)

        return t_folder

