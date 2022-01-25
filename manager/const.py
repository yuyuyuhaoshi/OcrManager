import pathlib
from os import environ, path

ROOT_DIR = pathlib.Path(path.abspath(path.join(path.dirname(__file__))))

SERVER_NAME = "ocr-manager"
CONFIG_DIR = "ocr-manager"
NAMESPACE = environ.get("NAMESPACE", "dev")
