from typing import Optional
import uuid
from sqlite3 import IntegrityError
from vagabot.entities import Author, AuthorStatus

from vagabot.repository.repository import SqliteRepository


class AuthorRepository(SqliteRepository):
    def create_table_ddl(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS authors (
                id TEXT PRIMARY KEY,
                name TEXT,
                description TEXT,
                link TEXT,
                avatar TEXT,
                status INTEGER
            )
            """
        )

        self.conn.commit()

    def count_authors(self) -> int:
        row = self.cursor.execute(
            "SELECT COUNT(*) FROM authors WHERE status != ?",
            (AuthorStatus.DELETED.value,),
        ).fetchone()

        if not row:
            return 0

        return int(row[0])

    def get_by_id(self, author_id: uuid.UUID) -> Optional[Author]:
        self.cursor.execute("SELECT * FROM authors WHERE id = ?", (str(author_id),))
        row = self.cursor.fetchone()
        if row:
            return Author(
                name=row[1],
                description=row[2],
                link=row[3],
                avatar=row[4],
                status=AuthorStatus(row[5]),
                id=row[0],
            )
        return None

    def get_by_link(self, link: str) -> Optional[Author]:
        self.cursor.execute("SELECT * FROM authors WHERE link = ?", (str(link),))
        row = self.cursor.fetchone()
        if row:
            return Author(
                name=row[1],
                description=row[2],
                link=row[3],
                avatar=row[4],
                status=AuthorStatus(row[5]),
                id=row[0],
            )
        return None

    def upsert_by_link(self, author: Author) -> Optional[Author]:
        try:
            self.cursor.execute(
                """
                INSERT INTO authors (id, name, description,link, avatar, status)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    str(author.id),
                    author.name,
                    author.description,
                    author.link,
                    author.avatar,
                    author.status.value,
                ),
            )
            self.conn.commit()

        except IntegrityError:
            self.cursor.execute(
                """
                UPDATE authors
                SET name = ?, description = ?, avatar = ?, status = ?
                WHERE link = ?
                """,
                (
                    author.name,
                    author.description,
                    author.avatar,
                    author.status.value,
                    str(author.link),
                ),
            )
            self.conn.commit()
        return self.get_by_link(author.link)

    def close(self):
        self.conn.close()
