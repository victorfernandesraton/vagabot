from sqlite3 import Connection
from abc import abstractmethod


class SqliteRepository:
    def __init__(self, conn: Connection):
        self.conn = conn
        self.cursor = self.conn.cursor()

    @abstractmethod
    def create_table_ddl(self):
        pass
