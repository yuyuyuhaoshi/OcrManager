# -*- coding: utf-8 -*-
import logging
import signal
import sys
import traceback

from flask import Flask, Response, request
from flask_cors import CORS
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException

from manager.apis import config_blueprints
from manager.config import config
from manager.const import SERVER_NAME
from manager.db import db
from manager.exceptions import (
    ApiClientException,
    BusinessException,
    InvalidRequest,
    ServerException,
)
from manager.extentions import ocr_client
from manager.utils.http import json_dumps, json_response

logger = logging.getLogger(__name__)


def create_app():
    app = Flask(SERVER_NAME)
    app.config["APP_NAME"] = SERVER_NAME
    config_configs(app)

    CORS(app=app, **(config.get("cors") or {}))

    config_logging(app)
    config_extensions(app)
    config_blueprints(app)
    config_errors(app)
    configure_db(app)

    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)

    return app


def config_configs(app):
    app.config["NAMESPACE"] = config.get("namespace")


def config_logging(app):
    ...


def config_extensions(app):
    ocr_client.configure()


def config_errors(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, ValidationError):
            logger.warning(e)
            return json_response(
                data=dict(
                    code=400400,
                    error="请求参数错误",
                    message=str(e.errors()),
                ),
                status=400,
            )
        elif isinstance(e, InvalidRequest):
            logger.warning(e)
            return json_response(
                data=dict(
                    code=e.code,
                    error=e.name(),
                    message=e.error,
                ),
                status=e.status_code,
            )
        elif isinstance(e, HTTPException):
            return json_response(
                data=dict(
                    code=e.code,
                    error=type(e).__name__,
                    message=e.name,
                ),
                status=e.code,
            )
        elif isinstance(e, ApiClientException):
            logger.exception(e)
            return json_response(
                data=dict(
                    code=e.code,
                    error=e.name(),
                    message=e.error,
                ),
                status=e.status_code,
            )
        elif isinstance(e, ServerException):
            logger.exception(e)
            return json_response(
                data=dict(
                    code=e.code,
                    error=e.name(),
                    message=e.error,
                ),
                status=e.status_code,
            )
        elif isinstance(e, BusinessException):
            logger.error(e)

            return Response(
                e.data, status=e.status, mimetype="application/json;charset=utf8"
            )
        else:
            logger.exception(traceback.format_exc())
            return json_response(
                data=dict(
                    code=500500,
                    error=type(e).__name__,
                    message=str(e),
                ),
                status=500,
            )

    @app.errorhandler(404)
    def handle_404(e):
        status = 200 if request.method == "OPTIONS" else 404
        resp = json_response(
            {
                "code": 404,
                "error": "NotFound",
                "message": "Not Found",
            },
            status=status,
        )
        return resp


def configure_db(app: Flask):

    app.config["SQLALCHEMY_DATABASE_URI"] = config.get("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    # app.config["SQLALCHEMY_ECHO"] = True
    db.init_app(app)
    db.app = app
    logging.info("Create mysql tables ~")
    db.create_all()


def handle_shutdown(signum, frame):
    logger.info("Shutdown Server")

    logger.info("Server exit")
    sys.exit(0)
