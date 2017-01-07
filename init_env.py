# coding=utf-8
from datetime import datetime
from OrcLib.LibCommon import gen_date_str
from OrcLib.LibCommon import is_null
from OrcLib.LibException import OrcDatabaseException
from OrcLib.LibDatabase import TabBatchDef
from OrcLib.LibDatabase import gen_id
from OrcLib.LibDatabase import orc_db
from OrcLib.LibLog import OrcLog


sess = orc_db.session.query(TabBatchDef).offset(1).limit(1)
for item in sess.all():
    print item.to_json()["id"]