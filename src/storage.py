import json
from abc import ABC, abstractmethod
from sqlite import SqliteConnection


class StorageAbstract(ABC):
    @abstractmethod
    def store(self, data, filename):
        pass
    @abstractmethod
    def load(self):
        pass


class SqliteStorage(StorageAbstract):
    def __init__(self):
        self.sqlite = SqliteConnection()

    def store(self, data, filename):
        if filename == 'links':
            for d in data:
                temp_d = tuple(d.values())
                stm = '''INSERT INTO links VALUES(?, ?);'''
                self.sqlite.connection.execute(stm, temp_d)
                self.sqlite.connection.commit()
        else:
            for d in data:
                temp_d = tuple(d.values())
                stm = '''INSERT INTO data VALUES(?, ?, ?, ?, ?);'''
                self.sqlite.connection.execute(stm, temp_d)
                self.sqlite.connection.commit()

    def load(self):
        urls = self.sqlite.connection.execute('''SELECT url FROM links;''')
        return urls.fetchall()


class FileStorage(StorageAbstract):
    def store(self, data, filename):
        with open(f'data/{filename}.json', 'w') as f:
            f.write(json.dumps(data))

    def load(self):
        with open('data/links.json', 'r') as f:
            links = json.loads(f.read())
        return links


