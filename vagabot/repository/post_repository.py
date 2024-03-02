from sqlite3 import IntegrityError
from typing import List, Optional

from vagabot.entities import Post, PostStatus
from vagabot.repository.repository import SqliteRepository


class PostRepository(SqliteRepository):
    def create_table_ddl(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS posts (
                id TEXT PRIMARY KEY,
                linkedin_id TEXT UNIQUE,
                link TEXT,
                author_id TEXT,
                content TEXT,
                status INTEGER,
                FOREIGN KEY(author_id) REFERENCES authors(id)
            )
            """
        )

        self.conn.commit()

    def count_posts(self) -> int:
        row = self.cursor.execute(
            "SELECT COUNT(*) FROM posts WHERE status != ?",
            (PostStatus.DELETED.value,),
        ).fetchone()

        if not row:
            return 0

        return int(row[0])

    def get_by_id(self, post_id: str) -> Optional[Post]:
        self.cursor.execute("SELECT * FROM posts WHERE id = ?", (str(post_id),))
        row = self.cursor.fetchone()
        if row:
            return Post(
                linkedin_id=row[1],
                link=row[2],
                author_id=row[3],
                content=row[4],
                status=PostStatus(row[5]),
                id=row[0],
            )
        return None

    def get_by_author_id(self, author_id: str) -> List[Post]:
        self.cursor.execute("SELECT * FROM posts WHERE author_id = ?", (author_id,))
        rows = self.cursor.fetchall()
        return [
            Post(
                linkedin_id=row[1],
                link=row[2],
                author_id=row[3],
                content=row[4],
                status=PostStatus(row[5]),
                id=row[0],
            )
            for row in rows
        ]

    def get_by_linkedin_id(self, linkedin_id: str) -> Optional[Post]:
        self.cursor.execute(
            "SELECT * FROM posts WHERE linkedin_id = ?", (str(linkedin_id),)
        )
        row = self.cursor.fetchone()
        if row:
            return Post(
                linkedin_id=row[1],
                link=row[2],
                author_id=row[3],
                content=row[4],
                status=PostStatus(row[5]),
                id=row[0],
            )
        return None

    def get_by_status(self, status: PostStatus) -> Optional[Post]:
        self.cursor.execute(
            "SELECT * FROM posts WHERE status = ?", (int(status.value),)
        )
        rows = self.cursor.fetchall()
        return [
            Post(
                linkedin_id=row[1],
                link=row[2],
                author_id=row[3],
                content=row[4],
                status=PostStatus(row[5]),
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

    def upsert_by_linkedin_id(self, post: Post) -> Optional[Post]:
        try:
            self.cursor.execute(
                """
                INSERT INTO posts (id, linkedin_id, link, author_id, content, status)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    str(post.id),
                    post.linkedin_id,
                    post.link,
                    post.author_id,
                    post.content,
                    post.status.value,
                ),
            )
            self.conn.commit()
        except IntegrityError:
            self.cursor.execute(
                """
                UPDATE posts
                SET author_id = ?, content = ?, status = ?, link = ?
                WHERE linkedin_id = ?
                """,
                (
                    post.author_id,
                    post.content,
                    post.status.value,
                    post.link,
                    post.linkedin_id,
                ),
            )
            self.conn.commit()

        return self.get_by_linkedin_id(post.linkedin_id)

    def close(self):
        self.conn.close()
