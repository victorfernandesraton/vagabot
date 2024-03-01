from typing import Optional
import uuid
from sqlite3 import OperationalError
from typing import List
from vagabot.entities import Post, PostStatus
from vagabot.repository.repository import SqliteRepository


class PostRepository(SqliteRepository):
    def create_table_ddl(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS posts (
                id TEXT PRIMARY KEY,
                likedin_id TEXT,
                author_id TEXT,
                content TEXT,
                status INTEGER
                FOREIGN KEY(author_id) REFERENCES authors(id)
            )
            """
        )

        self.conn.commit()
        self.conn.close()

    def create(self, post: Post):
        self.cursor.execute(
            """
            INSERT INTO posts (id, likedin_id, author_id, content, status)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                str(post.id),
                post.likedin_id,
                post.author_id,
                post.content,
                post.status.value,
            ),
        )
        self.conn.commit()

    def get_by_id(self, post_id: uuid.UUID) -> Optional[Post]:
        self.cursor.execute("SELECT * FROM posts WHERE id = ?", (str(post_id),))
        row = self.cursor.fetchone()
        if row:
            return Post(
                likedin_id=row[1],
                author_id=row[2],
                content=row[3],
                status=PostStatus(row[4]),
                id=row[0],
            )
        return None

    def get_by_author_id(self, author_id: str) -> List[Post]:
        self.cursor.execute("SELECT * FROM posts WHERE author_id = ?", (author_id,))
        rows = self.cursor.fetchall()
        return [
            Post(
                likedin_id=row[1],
                author_id=row[2],
                content=row[3],
                status=PostStatus(row[4]),
                id=row[0],
            )
            for row in rows
        ]

    def get_by_linkedin_id(self, likedin_id: str) -> List[Post]:
        self.cursor.execute("SELECT * FROM posts WHERE likedin_id = ?", (likedin_id,))
        rows = self.cursor.fetchall()
        return [
            Post(
                likedin_id=row[1],
                author_id=row[2],
                content=row[3],
                status=PostStatus(row[4]),
                id=row[0],
            )
            for row in rows
        ]

    def set_deleted(self, post: Post):
        self.cursor.execute(
            """
            UPDATE posts
            SET status = ?
            WHERE id = ?
            """,
            (
                PostStatus.DELETED,
                str(post.id),
            ),
        )
        self.conn.commit()

    def upsert(self, post: Post):
        try:
            self.cursor.execute(
                """
                UPDATE posts
                SET likedin_id = ?, author_id = ?, content = ?, status = ?
                WHERE id = ?
                """,
                (
                    post.likedin_id,
                    post.author_id,
                    post.content,
                    post.status.value,
                    str(post.id),
                ),
            )
            self.conn.commit()
        except OperationalError:
            self.cursor.execute(
                """
                INSERT INTO posts (id, likedin_id, author_id, content, status)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    str(post.id),
                    post.likedin_id,
                    post.author_id,
                    post.content,
                    post.status.value,
                ),
            )
            self.conn.commit()

    def close(self):
        self.conn.close()
