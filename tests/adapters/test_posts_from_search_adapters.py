from tests.conftest import read_testdata_file
from unittest.case import TestCase
from vagabot.adapters.posts_from_search_adapters import PostsFromSearchExtractor

_test = TestCase()


def test_get_data_from_post(read_testdata_file):
    post = read_testdata_file("post_from_search.html")
    service = PostsFromSearchExtractor([post])
    result = service.to_dict()
    _test.assertEqual(len(result), 1)

    first_post = result[0]
    _test.assertIn("Claudia Antunes", first_post["author"]["name"])
    _test.assertIn(
        first_post["post"]["link"],
        "https://www.linkedin.com/feed/update/urn:li:activity:7029104699224039424",
    )
