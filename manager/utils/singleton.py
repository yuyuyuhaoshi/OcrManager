import functools
import threading


def singleton(cls):
    instances = {}
    lock = threading.Lock()

    @functools.wraps(cls)
    def getinstance(*args):
        _id = args
        if _id not in instances:
            with lock:
                if _id not in instances:
                    instances[_id] = cls(*args)
        return instances[_id]

    return getinstance


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        index = str((cls, tuple([id(arg) for arg in args]), tuple(kwargs.items())))
        if index not in cls._instances:
            cls._instances[index] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[index]
