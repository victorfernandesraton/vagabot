import argparse
import sqlite3
from vagabot.workflows.linkedin_get_posts import LinkedinGetPosts
from vagabot.repository.post_repository import PostRepository
from vagabot.repository.author_repository import AuthorRepository
from vagabot.adapters.posts_from_search_adapters import PostsFromSearchExtractor
from decouple import config

import sys


def search_posts(args) -> list:
    """
    Function to search posts.
    """
    service = LinkedinGetPosts()
    print(f"Searching posts with query: {args.query} in {args.user}")
    finded_posts = service.execute(args.query, args.user, args.password)
    result = PostsFromSearchExtractor(finded_posts).to_dict()
    return result


def post_comment(args):
    """
    Function to post a comment.
    """
    print(f"Posting comment: {args.comment}")


def main():
    conn = sqlite3.connect(
        "vagabot.db",
    )
    author_repository = AuthorRepository(conn)
    author_repository.create_table_ddl()
    post_repository = PostRepository(conn)
    post_repository.create_table_ddl()

    # create common argarse without helper to keep global args
    common = argparse.ArgumentParser(add_help=False)

    # Add global arguments
    common.add_argument(
        "-u", "--user", help="Linkedin Username", default=config("LINKEDIN_EMAIL", "")
    )
    common.add_argument(
        "-p",
        "--password",
        help="Linkedin Password",
        default=config("LINKEDIN_PASS", ""),
    )

    # Create the parser
    parser = argparse.ArgumentParser(
        description="CLI for user and password management.", parents=[common]
    )

    # Create the subparsers
    subparsers = parser.add_subparsers(dest="command")

    search_posts_parser = subparsers.add_parser(
        "search-posts", help="Search posts", parents=[common]
    )
    search_posts_parser.add_argument(
        "-q", "--query", required=False, help="Query for search", type=str
    )

    post_comment_parser = subparsers.add_parser(
        "post-comment", help="Post a comment", parents=[common]
    )
    post_comment_parser.add_argument(
        "-c", "--comment", required=True, help="Comment to post", type=str
    )

    args = parser.parse_args()

    if args.command == "search-posts":
        result = search_posts(args)
        print(result)
        for item in result:
            author_repository.upsert_by_linkk(item["author"])
            post_repository.upsert_by_linkedin_id(item["post"])

    elif args.command == "post-comment":
        post_comment(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
