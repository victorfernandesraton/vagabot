import sqlite3
import pytest
import os

from vagabot.repository.author_repository import AuthorRepository


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


@pytest.fixture(scope="session")
def author_repository_fixture(db) -> AuthorRepository:
    repo = AuthorRepository(db)
    repo.create_table_ddl()

    return repo


@pytest.fixture(scope="session", autouse=True)
def author_repository_tierdown(db):
    db.cursor().execute("DROP TABLE IF EXISTS authors")
    db.commit()
