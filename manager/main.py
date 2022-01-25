# -*- coding: utf-8 -*-


def main():
    import logging
    import sys

    logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stdout)

    from manager.app import create_app
    from manager.const import NAMESPACE, SERVER_NAME

    logger = logging.getLogger(__name__)

    app = create_app()
    app.debug = False

    logger.info("%s start at %s:%s %s", SERVER_NAME, "0.0.0.0", 5000, NAMESPACE)

    return app


if __name__ == "__main__":
    from gevent import monkey

    monkey.patch_all()

    from gevent.pywsgi import WSGIServer

    WSGIServer(("0.0.0.0", 5000), main(), backlog=1024).serve_forever()
