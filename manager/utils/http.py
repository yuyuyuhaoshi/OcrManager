# -*- coding: utf-8 -*-
from datetime import date, datetime
from decimal import Decimal
from typing import Any, Union

from flask import Response
from orjson import OPT_PASSTHROUGH_DATETIME, dumps


def _default(o: Any) -> Union[str, int, float]:
    if isinstance(o, datetime):
        return o.isoformat(sep=" ")
    elif isinstance(o, date):
        return o.isoformat()
    elif isinstance(o, Decimal):
        return str(o)
    else:
        raise TypeError(o)


def json_dumps(data: Any) -> str:
    return dumps(data, option=OPT_PASSTHROUGH_DATETIME, default=_default).decode(
        "utf-8"
    )


def json_response(
    data: Union[dict, list, str, int, float], status: int = 200, headers: dict = None
) -> Response:
    content = dumps(data, option=OPT_PASSTHROUGH_DATETIME, default=_default)
    return Response(
        content,
        status=status,
        mimetype="application/json; charset=utf-8",
        headers=headers,
    )
