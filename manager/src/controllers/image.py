import logging
from typing import List

from manager.exceptions import BusinessError
from manager.schemas import model
from manager.schemas.image import ImageResponse, ImageBaseResponse
from manager.src.controllers.base import BaseController
from manager.extentions import ocr_client, image_client
from manager.db import Image

logger = logging.getLogger(__name__)


class ImageOCRController(BaseController):
    def image_ocr(self, url: str) -> ImageResponse:
        logger.info(f"{self.__class__.__name__} start image url ocr")

        image_bytes: bytes = image_client.get_image(url)
        content: List[str] = ocr_client.get_content(image_bytes)
        logging.info(f"{self.__class__.__name__} file content: {content}")
        image = Image(
            name="",
            url = url,
            content = content
        )
        image.save()

        i = ImageBaseResponse(**image.to_dict())
        return ImageResponse(image=i)

    def image_file_ocr(self, image: model.File) -> ImageResponse:
        try:
            filename = str(image.filename)
            logger.info(f"{self.__class__.__name__} upload filename: {filename}")
        except IOError as e:
            logger.error("get file failed, error: {}".format(e))
            raise BusinessError("文件错误, 请重新上传")
        logging.info(f"{self.__class__.__name__} start image ocr file: {filename}")
        content: List[str] = ocr_client.get_content(image.stream.read())
        logging.info(f"{self.__class__.__name__} file content: {content}")
        image_model = Image(
            name=filename,
            url = "",
            content = content
        )
        image_model.save()
        i = ImageBaseResponse(**image_model.to_dict())
        return ImageResponse(image=i)
