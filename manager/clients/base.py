def _retry_on_exception(err: Exception):
    error = str(err)
    if "ConnectionResetError" in error:
        return True
    if "RemoteDisconnected" in error:
        return True
    if "Bad Gateway" in error:
        return True
    return False