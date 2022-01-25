# -*- coding: utf-8 -*-
from flask import Blueprint

from manager.utils.http import json_response

healthz_bp = Blueprint("healthz", __name__)


@healthz_bp.route("/healthz")
def healthz():
    return json_response(dict(ok=True))
