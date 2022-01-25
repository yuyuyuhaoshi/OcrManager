from manager.apis.base import BaseBlueprint
from manager.apis.v1.image import ImageOcrResource

v1_bp = BaseBlueprint("v1", __name__)

v1_bp.register_resource(ImageOcrResource())
