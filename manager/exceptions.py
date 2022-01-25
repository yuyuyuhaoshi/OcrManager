# -*- coding: utf-8 -*-


class ServerException(Exception):
    status_code = 500
    code = 500500
    error = "Internal Server Error"

    def __init__(self, error=""):
        self.error = error or self.error

    @classmethod
    def name(cls) -> str:
        return cls.__name__

    def __str__(self):
        return f"{self.name()}({self.error})"


class CallOssServiceError(ServerException):
    status_code = 500
    code = 500001
    error = "上传文件失败"


class InvalidRequest(ServerException):
    status_code = 422
    code = 422422
    error = "Invalid Request"


class ObjectNotFound(InvalidRequest):
    status_code = 404
    code = 404400
    error = "Object Not Found"


class ObjectAlreadyDeleted(ObjectNotFound):
    code = 404401
    error = "Object Already Deleted"


class SchemaError(InvalidRequest):
    code = 400400
    error = "Schema Error"


class DuplicateNamed(InvalidRequest):
    status_code = 400
    code = 400401
    error = "存在重名数据"


class BusinessError(InvalidRequest):
    status_code = 400
    code = 400402
    error = "非法请求"


class PermissionDenied(InvalidRequest):
    status_code = 403
    code = 403000
    error = "你没有权限访问"


class ApiClientTimeout(ServerException):
    status_code = 500
    code = 500400
    error = "业务系统接口调用超时"

    def __init__(self, error="", e: Exception = None, business_type: str = None):
        super(ApiClientTimeout, self).__init__(error=error)
        self.e = e
        self.business_type = business_type

    def __str__(self):
        return f"ApiClientTimeout({self.business_type}, {self.e})"


class ApiClientError(InvalidRequest):
    status_code = 400
    code = 400500
    error = "业务系统接口调用错误"


class ApiClientException(ServerException):
    status_code = 500
    code = 500300
    error = "业务系统接口调用失败"

    def __init__(self, error="", e: Exception = None, business_type: str = None):
        super(ApiClientException, self).__init__(error=error)
        self.e = e
        self.business_type = business_type

    def __str__(self):
        return f"ApiClientException({self.business_type}, {self.e})"


class BusinessException(Exception):
    def __init__(self, status: int, data: bytes, business_type: str):
        self.status = status
        self.data = data
        self.business_type = business_type

    def __str__(self):
        message = self.data
        try:
            message = message.decode("utf-8")
        except (UnicodeDecodeError, Exception):
            pass
        return f"BusinessException({self.business_type}, {self.status}, {message})"
