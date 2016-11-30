# coding=utf-8
import sys

from OrcLib import init_log
from OrcLib import get_config

from OrcApi import app
from OrcApi import orc_api

from OrcApi.Data import api
from OrcApi.Driver.Web import api
from OrcApi.Lib import api

from OrcApi.Batch.BatchApi import BatchDefListAPI
from OrcApi.Batch.BatchApi import BatchDefAPI
from OrcApi.Batch.BatchApi import BatchDetListAPI
from OrcApi.Batch.BatchApi import BatchDetAPI

from OrcApi.Case.CaseApi import CaseDefListAPI
from OrcApi.Case.CaseApi import CaseDefAPI
from OrcApi.Case.CaseApi import CaseDetListAPI
from OrcApi.Case.CaseApi import CaseDetAPI
from OrcApi.Case.StepApi import StepDefListAPI
from OrcApi.Case.StepApi import StepDefAPI
from OrcApi.Case.StepApi import StepDetListAPI
from OrcApi.Case.StepApi import StepDetAPI
from OrcApi.Case.ItemApi import ItemListAPI
from OrcApi.Case.ItemApi import ItemAPI

from OrcApi.Data.DataApi import DataListAPI
from OrcApi.Data.DataApi import DataAPI

from OrcApi.Driver.Web.PageApi import PageDefListAPI
from OrcApi.Driver.Web.PageApi import PageDefAPI
from OrcApi.Driver.Web.PageApi import PageDetListAPI
from OrcApi.Driver.Web.PageApi import PageDetAPI
from OrcApi.Driver.Web.WindowApi import WindowListAPI
from OrcApi.Driver.Web.WindowApi import WindowAPI
from OrcApi.Driver.Web.WidgetApi import WidgetDefListAPI
from OrcApi.Driver.Web.WidgetApi import WidgetDefAPI
from OrcApi.Driver.Web.WidgetApi import WidgetDetListAPI
from OrcApi.Driver.Web.WidgetApi import WidgetDetAPI

configer = get_config("network")

# Batch
orc_api.add_resource(BatchDefListAPI, '/api/1.0/BatchDef', endpoint='BatchDefs')
orc_api.add_resource(BatchDefAPI, '/api/1.0/BatchDef/<int:p_id>', endpoint='BatchDef')
orc_api.add_resource(BatchDetListAPI, '/api/1.0/BatchDet', endpoint='BatchDets')
orc_api.add_resource(BatchDetAPI, '/api/1.0/BatchDet/<int:p_id>', endpoint='BatchDet')

# Case
orc_api.add_resource(CaseDefListAPI, '/api/1.0/CaseDef', endpoint='CaseDefs')
orc_api.add_resource(CaseDefAPI, '/api/1.0/CaseDef/<int:p_id>', endpoint='CaseDef')
orc_api.add_resource(CaseDetListAPI, '/api/1.0/CaseDet', endpoint='CaseDets')
orc_api.add_resource(CaseDetAPI, '/api/1.0/CaseDet/<int:p_id>', endpoint='CaseDet')

# Step
orc_api.add_resource(StepDefListAPI, '/api/1.0/StepDef', endpoint='StepDefs')
orc_api.add_resource(StepDefAPI, '/api/1.0/StepDef/<int:p_id>', endpoint='StepDef')
orc_api.add_resource(StepDetListAPI, '/api/1.0/StepDet', endpoint='StepDets')
orc_api.add_resource(StepDetAPI, '/api/1.0/StepDet/<int:p_id>', endpoint='StepDet')

# Item
orc_api.add_resource(ItemListAPI, '/api/1.0/Item', endpoint='Items')
orc_api.add_resource(ItemAPI, '/api/1.0/Item/<int:p_id>', endpoint='Item')

# Item
orc_api.add_resource(DataListAPI, '/api/1.0/Data', endpoint='Datas')
orc_api.add_resource(DataAPI, '/api/1.0/Data/<int:p_id>', endpoint='Data')

# Page
orc_api.add_resource(PageDefListAPI, '/api/1.0/PageDef', endpoint='PageDefs')
orc_api.add_resource(PageDefAPI, '/api/1.0/PageDef/<int:p_id>', endpoint='PageDef')
orc_api.add_resource(PageDetListAPI, '/api/1.0/PageDet', endpoint='PageDets')
orc_api.add_resource(PageDetAPI, '/api/1.0/PageDet/<int:p_id>', endpoint='PageDet')

# Widget
orc_api.add_resource(WidgetDefListAPI, '/api/1.0/WidgetDef', endpoint='WidgetDefs')
orc_api.add_resource(WidgetDefAPI, '/api/1.0/WidgetDef/<int:p_id>', endpoint='WidgetDef')
orc_api.add_resource(WidgetDetListAPI, '/api/1.0/WidgetDet', endpoint='WidgetDets')
orc_api.add_resource(WidgetDetAPI, '/api/1.0/WidgetDet/<int:p_id>', endpoint='WidgetDet')

orc_api.add_resource(WindowListAPI, '/api/1.0/WindowDef', endpoint='Windows')
orc_api.add_resource(WindowAPI, '/api/1.0/WindowDef/<int:p_id>', endpoint='Window')

driver_host = configer.get_option("CASE", "ip")
driver_port = configer.get_option("CASE", "port")

reload(sys)
init_log()

app.run(host=driver_host, port=driver_port)
