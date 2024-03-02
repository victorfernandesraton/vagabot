from unittest.case import TestCase

from tests.conftest import create_author_fixture, db, post_repository_fixture
from vagabot.entities import Post, PostStatus
from vagabot.repository.post_repository import PostRepository

_test = TestCase()


def test_create_table_post(db):
    repository = PostRepository(db)
    try:
        repository.create_table_ddl()
    except Exception as err:
        _test.assertIsNone(err)


def test_create_post(create_author_fixture, post_repository_fixture):
    repository = post_repository_fixture
    author = create_author_fixture
    total_posts = repository.count_posts()

    _test.assertEqual(total_posts, 0)

    post_param = Post(
        linkedin_id="121212",
        author_id=author.id,
        link="https://linkedin.com/feed/1212",
        content="Some text",
    )
    created_post = repository.upsert_by_linkedin_id(post_param)

    _test.assertEqual(created_post.author_id, author.id)
    _test.assertEqual(created_post.link, post_param.link)
    _test.assertEqual(created_post.linkedin_id, post_param.linkedin_id)
    _test.assertEqual(created_post.content, post_param.content)

    total_posts = repository.count_posts()
    _test.assertEqual(total_posts, 1)


def test_upsert_posts(create_author_fixture, post_repository_fixture):
    repository = post_repository_fixture
    author = create_author_fixture
    total_posts = repository.count_posts()

    _test.assertEqual(total_posts, 0)

    post_param = Post(
        linkedin_id="121212",
        author_id=author.id,
        link="https://linkedin.com/feed/1212",
        content="Some text",
    )
    created_post = repository.upsert_by_linkedin_id(post_param)

    _test.assertEqual(created_post.author_id, author.id)
    _test.assertEqual(created_post.link, post_param.link)
    _test.assertEqual(created_post.linkedin_id, post_param.linkedin_id)
    _test.assertEqual(created_post.content, post_param.content)

    total_posts = repository.count_posts()
    _test.assertEqual(total_posts, 1)

    update_post_params = Post(
        linkedin_id=created_post.linkedin_id,
        author_id=created_post.author_id,
        link=created_post.link,
        id=created_post.id,
        content="Other text xablau",
    )

    updated_post = repository.upsert_by_linkedin_id(update_post_params)

    _test.assertEqual(updated_post.author_id, created_post.author_id)
    _test.assertEqual(updated_post.link, created_post.link)
    _test.assertEqual(updated_post.linkedin_id, created_post.linkedin_id)
    _test.assertNotEqual(updated_post.content, created_post.content)
    _test.assertEqual(updated_post.author_id, update_post_params.author_id)
    _test.assertEqual(updated_post.link, update_post_params.link)
    _test.assertEqual(updated_post.linkedin_id, update_post_params.linkedin_id)
    _test.assertEqual(updated_post.content, update_post_params.content)

    total_posts = repository.count_posts()
    _test.assertEqual(total_posts, 1)


def test_get_by_id(create_author_fixture, post_repository_fixture):
    repository = post_repository_fixture
    author = create_author_fixture
    total_posts = repository.count_posts()

    _test.assertEqual(total_posts, 0)

    post_param = Post(
        linkedin_id="121212",
        author_id=author.id,
        link="https://linkedin.com/feed/1212",
        content="Some text",
    )
    created_post = repository.upsert_by_linkedin_id(post_param)
    finded_post = repository.get_by_id(created_post.id)
    total_posts = repository.count_posts()

    _test.assertEqual(total_posts, 1)
    _test.assertEqual(created_post.author_id, finded_post.author_id)
    _test.assertEqual(created_post.link, finded_post.link)
    _test.assertEqual(created_post.linkedin_id, finded_post.linkedin_id)
    _test.assertEqual(created_post.content, finded_post.content)


def test_get_by_linkedin_id(create_author_fixture, post_repository_fixture):
    repository = post_repository_fixture
    author = create_author_fixture
    total_posts = repository.count_posts()

    _test.assertEqual(total_posts, 0)

    post_param = Post(
        linkedin_id="121212",
        author_id=author.id,
        link="https://linkedin.com/feed/1212",
        content="Some text",
    )
    created_post = repository.upsert_by_linkedin_id(post_param)
    finded_post = repository.get_by_linkedin_id(created_post.linkedin_id)
    total_posts = repository.count_posts()

    _test.assertEqual(total_posts, 1)
    _test.assertEqual(created_post.author_id, finded_post.author_id)
    _test.assertEqual(created_post.link, finded_post.link)
    _test.assertEqual(created_post.linkedin_id, finded_post.linkedin_id)
    _test.assertEqual(created_post.content, finded_post.content)


def test_get_by_author_id(create_author_fixture, post_repository_fixture):
    repository = post_repository_fixture
    author = create_author_fixture
    total_posts = repository.count_posts()

    _test.assertEqual(total_posts, 0)

    post_param = Post(
        linkedin_id="121212",
        author_id=author.id,
        link="https://linkedin.com/feed/1212",
        content="Some text",
    )

    other_post = Post(
        linkedin_id="121213",
        author_id=author.id,
        link="https://linkedin.com/feed/121213",
        content="Other post",
    )

    _test.assertNotEqual(post_param.id, other_post.id)
    created_post = repository.upsert_by_linkedin_id(post_param)
    created_other_post = repository.upsert_by_linkedin_id(other_post)
    finded_posts = repository.get_by_author_id(author.id)
    total_posts = repository.count_posts()

    _test.assertEqual(total_posts, 2)
    _test.assertEqual(len(finded_posts), 2)
    _test.assertEqual(created_post.author_id, finded_posts[0].author_id)
    _test.assertEqual(created_post.link, finded_posts[0].link)
    _test.assertEqual(created_post.linkedin_id, finded_posts[0].linkedin_id)
    _test.assertEqual(created_post.content, finded_posts[0].content)
    _test.assertEqual(created_other_post.author_id, finded_posts[1].author_id)
    _test.assertEqual(created_other_post.link, finded_posts[1].link)
    _test.assertEqual(created_other_post.linkedin_id, finded_posts[1].linkedin_id)
    _test.assertEqual(created_other_post.content, finded_posts[1].content)
