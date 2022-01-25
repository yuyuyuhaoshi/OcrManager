import requests
from retrying import retry

from manager.clients.base import _retry_on_exception
from manager.exceptions import BusinessError


class ImageClient:
    @retry(
        stop_max_attempt_number=3,
        wait_random_min=10,
        wait_random_max=200,
        retry_on_exception=_retry_on_exception,
    )
    def get_image(self, url: str) -> bytes:
        res = requests.get(url=url, timeout=60)
        if res.status_code != 200:
            raise BusinessError(f"获取图片: {url}失败")
        return res.content
