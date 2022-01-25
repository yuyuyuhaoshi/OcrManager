import logging
from typing import Dict, Optional, Union

from manager.apis.base import BaseResource, Router
from manager.schemas import model
from manager.src.controllers.image import ImageOCRController

logger = logging.getLogger(__name__)


@Router.prefix("image", summary="图像识别")
class ImageOcrResource(BaseResource):
    @Router.post("/ocr", summary="图片链接识别")
    def image_url_search(
        self, url: str = model.Source(embed=True, description="图片地址", data_from="JSON")
    ):
        c = ImageOCRController()
        return c.image_ocr(url)

    @Router.post("/ocr/file", summary="图片文件识别")
    def image_file_search(
        self,
        file: model.File = model.Source(
            embed=True, description="图片文件", data_from="FILE"
        ),
    ):
        c = ImageOCRController()
        return c.image_file_ocr(file)
