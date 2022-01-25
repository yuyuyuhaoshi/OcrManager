# -*- coding: utf-8 -*-
import os
import logging
import sys

os.environ["NAMESPACE"] = "test"  # noqa

from unittest import TestCase
from unittest.mock import patch

patch("manager.clients.ocr.OCRClient.configure", lambda *a, **kw: None).start()

logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stdout)

from manager.app import create_app
from manager.db import db


class BaseTestCase(TestCase):
    app_context = None

    @classmethod
    def setUpClass(cls) -> None:
        

        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.app.config['WTF_CSRF_ENABLED'] = False
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.app_context.pop()

    def setUp(self):
        db.init_app(self.app)
        db.app = self.app
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        # db.drop_all()
