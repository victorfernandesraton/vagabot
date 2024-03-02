import os
import sqlite3
from typing import Optional

import pytest

from vagabot.entities import Author
from vagabot.repository.author_repository import AuthorRepository
from vagabot.repository.post_repository import PostRepository


@pytest.fixture(scope="session")
def read_testdata_file():
    def _read_file(filename):
        # Assume que os arquivos estão na pasta "testdata"
        testdata_dir = os.path.join(os.path.dirname(__file__), "testdata")
        file_path = os.path.join(testdata_dir, filename)

        try:
            with open(file_path, "r") as file:
                content = file.read()
                return content
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Arquivo '{filename}' não encontrado em 'testdata'."
            )

    return _read_file


@pytest.fixture(scope="session")
def db():
    conn = sqlite3.connect("file::memory:?cache=shared", uri=True)

    yield conn

    conn.close()


@pytest.fixture(scope="function")
def author_repository_fixture(db) -> AuthorRepository:
    repo = AuthorRepository(db)
    repo.create_table_ddl()

    return repo


@pytest.fixture(scope="function")
def create_author_fixture(author_repository_fixture) -> Optional[Author]:
    repo = author_repository_fixture
    author = Author(name="Victor Raton", link="https://linkedin.com/in/v_raton")
    result = repo.upsert_by_link(author)
    return result


@pytest.fixture(scope="function", autouse=True)
def author_repository_tierdown(db):
    db.cursor().execute("DROP TABLE IF EXISTS authors")
    db.commit()


@pytest.fixture(scope="function")
def post_repository_fixture(db) -> PostRepository:
    repo = PostRepository(db)
    repo.create_table_ddl()

    return repo


@pytest.fixture(scope="function", autouse=True)
def post_repository_tierdown(db):
    db.cursor().execute("DROP TABLE IF EXISTS posts")
    db.commit()
