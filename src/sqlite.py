import sqlite3


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class SqliteConnection(metaclass=SingletonMeta):
    def __init__(self, *args, **kwargs):
        self.connection = sqlite3.connect('craig_list.db')



