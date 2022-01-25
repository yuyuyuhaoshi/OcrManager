from io import BytesIO
from typing import List

from easyocr import Reader
from retrying import retry

from manager.clients.base import _retry_on_exception



class OCRClient:
    def configure(self):
        self.reader: Reader = Reader(
            ["ch_sim", "en"]
        )

    @retry(
        stop_max_attempt_number=3,
        wait_random_min=10,
        wait_random_max=200,
        retry_on_exception=_retry_on_exception,
    )
    def get_content(self, image: bytes) -> List:
        result = self.reader.readtext(image, detail=0)
        return result
