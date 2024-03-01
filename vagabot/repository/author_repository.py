from typing import Optional
import uuid
from sqlite3 import OperationalError
from entities import Author, AuthorStatus
from typing import List

from vagabot.repository.repository import SqliteRepository


class AuthorRepository(SqliteRepository):
    def create_table_ddl(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS authors (
                id TEXT PRIMARY KEY,
                linkedin_id TEXT,
                name TEXT,
                description TEXT,
                link TEXT,
                avatar TEXT,
                status INTEGER
            )
            """
        )

        self.conn.commit()
        self.conn.close()

    def create(self, author: Author):
        self.cursor.execute(
            """
            INSERT INTO authors (id, linkedin_id, name, description, link, avatar, status)
            VALUES (?, ?, ?, ?, ?, ? , ?)
            """,
            (
                str(author.id),
                author.linkedin_id,
                author.name,
                author.description,
                author.link,
                author.avatar,
                author.status.value,
            ),
        )
        self.conn.commit()

    def get_by_id(self, author_id: uuid.UUID) -> Optional[Author]:
        self.cursor.execute(
            "SELECT * FROM authors WHERE id = ? LIMIT 1", (str(author_id),)
        )
        row = self.cursor.fetchone()
        if row:
            return Author(
                linkedin_id=row[1],
                name=row[2],
                description=row[3],
                link=row[4],
                avatar=row[5],
                status=AuthorStatus(row[6]),
                id=row[0],
            )
        return None

    def get_by_linkedin_id(self, linkedin_id: str) -> List[Author]:
        self.cursor.execute(
            "SELECT * FROM authors WHERE linkedin_id = ?", (linkedin_id,)
        )
        rows = self.cursor.fetchall()
        return [
            Author(
                linkedin_id=row[1],
                name=row[2],
                description=row[3],
                link=row[4],
                avatar=row[5],
                status=AuthorStatus(row[6]),
                id=row[0],
            )
            for row in rows
        ]

    def upsert(self, author: Author):
        # Upsert logic: try to update, if not exists, insert
        try:
            self.cursor.execute(
                """
                UPDATE authors
                SET linkedin_id = ?, name = ?, author = ? ,link = ?, avatar = ?, status = ?
                WHERE id = ?
                """,
                (
                    author.linkedin_id,
                    author.name,
                    author.description,
                    author.link,
                    author.avatar,
                    author.status.value,
                    str(author.id),
                ),
            )
            self.conn.commit()
        except OperationalError:
            self.cursor.execute(
                """
                INSERT INTO authors (id, linkedin_id, name, description,link, avatar, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    str(author.id),
                    author.linkedin_id,
                    author.name,
                    author.description,
                    author.link,
                    author.avatar,
                    author.status.value,
                ),
            )
            self.conn.commit()

    def close(self):
        self.conn.close()
