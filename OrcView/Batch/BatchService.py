from OrcLib.LibNet import OrcHttpResource


class BatchDefService:

    def __init__(self):

        self.__resource_run_def = OrcHttpResource("RunDef")

    def add_to_run(self, p_id):

        cond = dict(id=p_id, run_def_type="BATCH")

        self.__resource_run_def.set_path(p_id)
        self.__resource_run_def.post(cond)
