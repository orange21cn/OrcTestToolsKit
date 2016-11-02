from OrcLib.LibNet import OrcHttpResource
from OrcLib.LibNet import OrcSocketResource
from OrcLib.LibDatabase import TabItem


class RunCoreService:

    def __init__(self):

        self.__resource_web_driver = OrcHttpResource("WebDriver")
        self.__resource_item = OrcHttpResource("Item")

    def run(self, p_step):

        step_type = p_step["run_det_type"]
        step_id = p_step["id"]

        if "ITEM" == step_type:
            self.__run_step(step_id)
        else:
            pass

    def __run_step(self, p_id):
        self.__resource_item.set_id(p_id)
        item = TabItem(self.__resource_item.get())

        if "WEB" == item.item_type:
            self.__resource_web_driver.get()
        else:
            pass


class RunState:

    state_waiting = "WAITING"
    state_pass = "PASS"
    state_fail = "FAIL"

    def __init__(self):
        pass
