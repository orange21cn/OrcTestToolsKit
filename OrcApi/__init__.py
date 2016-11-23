# -*- coding: utf-8 -*-
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from OrcLib import get_config

app = Flask(__name__)
orc_api = Api(app)

_config = get_config()
print _config
_data_str = _config.get_option("DATABASE", "DATA_STR")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = _data_str

orc_db = SQLAlchemy(app)