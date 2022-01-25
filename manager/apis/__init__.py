# -*- coding: utf-8 -*-

from flask import Flask

from manager.apis.healthz import healthz_bp
from manager.apis.v1 import v1_bp


def config_blueprints(app: Flask):
    app.register_blueprint(healthz_bp, url_prefix="/api")
    app.register_blueprint(v1_bp, url_prefix="/api/v1")
