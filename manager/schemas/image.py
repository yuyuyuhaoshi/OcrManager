from typing import Dict, List

from manager.schemas import model


class ImageBaseResponse(model.BaseModel):
    id: int = model.Field(description="ID")
    tdate: str = model.Field(description="创建时间")
    udate: str = model.Field(description="修改时间")
    name: str = model.Field(description="文件名称")
    url: str = model.Field(description="文件地址")
    content: List[str] = model.Field(description="内容")

class ImageResponse(model.BaseResponse):
    image: ImageBaseResponse = model.Field(description="图片识别结果")
