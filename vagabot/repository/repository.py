import sqlite3
from abc import abstractmethod


class SqliteRepository:
    def __init__(self, database_path: str = "vagabot.db"):
        self.conn = sqlite3.connect(database_path)
        self.cursor = self.conn.cursor()

    @abstractmethod
    def create_table_ddl(self):
        pass
