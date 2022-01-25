import os
import sys

from manager.const import ROOT_DIR

Config = {
    "DEBUG": False,
    "TESTING": False,
    "NAMESPACE": "dev",
    "SQLALCHEMY_DATABASE_URI": "sqlite:///" + str(ROOT_DIR / "../example.sqlite"),
}
