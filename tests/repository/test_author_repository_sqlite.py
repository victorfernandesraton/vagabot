import sqlite3
from unittest.case import TestCase

from tests.conftest import author_repository_fixture, db
from vagabot.entities import Author, AuthorStatus
from vagabot.repository.author_repository import AuthorRepository

_test = TestCase()

conn = sqlite3.connect("file::memory:?cache=shared", uri=True)


def test_create_database_dql(db):
    repository = AuthorRepository(conn)
    try:
        repository.create_table_ddl()
    except Exception as err:
        _test.assertIsNone(err)


def test_create_author(db, author_repository_fixture):
    repository = author_repository_fixture
    author_param = Author(
        name="Victor Raton", link="https://linkedin.com/in/v_raton", avatar=""
    )
    created_author = repository.upsert_by_link(author_param)
    _test.assertIsNotNone(created_author.id)
    _test.assertEqual(author_param.name, created_author.name)
    _test.assertEqual(author_param.link, created_author.link)
    _test.assertEqual(AuthorStatus.CREATED, created_author.status)


def test_upsert_author(db, author_repository_fixture):
    repository = author_repository_fixture
    count_authors = repository.count_authors()
    _test.assertEqual(count_authors, 0)
    author_param = Author(
        name="Victor Raton", link="https://linkedin.com/in/v_raton", avatar=""
    )
    created_author = repository.upsert_by_link(author_param)
    _test.assertIsNotNone(created_author.id)
    _test.assertEqual(author_param.name, created_author.name)
    _test.assertEqual(author_param.link, created_author.link)
    _test.assertEqual(AuthorStatus.CREATED, created_author.status)
    _test.assertEqual(author_param.description, created_author.description)
    count_authors = repository.count_authors()
    _test.assertEqual(count_authors, 1)
    upsert_author_params = Author(
        name=created_author.name,
        link=created_author.link,
        avatar="",
        status=AuthorStatus.FOLLOWED,
        description="Now i have description",
    )
    upserted_author = repository.upsert_by_link(upsert_author_params)

    _test.assertEqual(created_author.id, upserted_author.id)
    _test.assertEqual(created_author.name, upserted_author.name)
    _test.assertEqual(created_author.link, upserted_author.link)
    _test.assertEqual(AuthorStatus.FOLLOWED, upserted_author.status)
    _test.assertNotEqual(created_author.status, upserted_author.status)
    _test.assertEqual(upsert_author_params.description, upserted_author.description)
    _test.assertNotEqual(created_author.description, upserted_author.description)
    _test.assertEqual(upsert_author_params.description, upserted_author.description)

    count_authors = repository.count_authors()
    _test.assertEqual(count_authors, 1)


def test_by_id(db, author_repository_fixture):
    repository = author_repository_fixture
    author_param = Author(
        name="Victor Raton", link="https://linkedin.com/in/v_raton", avatar=""
    )
    created_author = repository.upsert_by_link(author_param)
    finded_author = repository.get_by_id(author_param.id)

    _test.assertEqual(created_author.id, finded_author.id)
    _test.assertEqual(created_author.name, finded_author.name)
    _test.assertEqual(created_author.link, finded_author.link)


def test_by_link(db, author_repository_fixture):
    repository = author_repository_fixture
    author_param = Author(
        name="Victor Raton", link="https://linkedin.com/in/v_raton", avatar=""
    )
    created_author = repository.upsert_by_link(author_param)
    finded_author = repository.get_by_link(author_param.link)

    _test.assertEqual(created_author.id, finded_author.id)
    _test.assertEqual(created_author.name, finded_author.name)
    _test.assertEqual(created_author.link, finded_author.link)
