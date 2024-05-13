import argparse
import logging
import sqlite3
import sys

from decouple import config

from vagabot.adapters.posts_from_search_adapters import PostsFromSearchExtractor
from vagabot.entities import PostStatus
from vagabot.repository.author_repository import AuthorRepository
from vagabot.repository.post_repository import PostRepository
from vagabot.services import RemoteBrowserService
from vagabot.workflows import LinkedinAuth, LinkedinCommentPost, LinkedinGetPosts

_se_router_host = config("SE_ROUTER_HOST", "localhost")
_se_router_port = config("SE_ROUTER_PORT", "4444")

remote_browser_service = RemoteBrowserService(
    se_router_host=_se_router_host, se_router_port=_se_router_port
)


def linkedin_auth(args) -> str:
    logging.info(f"Login for {args.user} in linkedin")
    service_auth = LinkedinAuth(remote_browser_service)
    driver_key = remote_browser_service.open_browser()
    service_auth.execute(driver_key, args.user, args.password)
    return driver_key


def search_posts(args) -> list:
    logging.info(f"Search posts: {args.query}")
    driver_key = linkedin_auth(args)
    service = LinkedinGetPosts(remote_browser_service)
    # TODO: passing default value, but planing for get these data from configuration
    finded_posts = service.execute(driver_key, args.query, {"datePosted": "LAST_WEEK"})
    finded_posts = list(filter(lambda i: i is not None, finded_posts))
    remote_browser_service.close(driver_key)
    return finded_posts


def post_comment(args, posts: list, post_repository: PostRepository):
    logging.info(f"Posting comment: {args.comment}")
    driver_key = linkedin_auth(args)
    service = LinkedinCommentPost(
        browser_service=remote_browser_service,
        post_repository=post_repository,
        message=args.comment,
    )
    service.execute(driver_key, posts)
    remote_browser_service.close(driver_key)


def main():
    database_filename = config("DB_FILENAME", None)
    if database_filename:
        conn = sqlite3.connect(config(database_filename))
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
        "-q", "--query", required=False, help="Query for search", type=str, default=""
    )

    search_posts_parser.add_argument(
        "-o", "--output", required=False, help="Output type", type=str
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
        logging.debug(result)

        formated_results = PostsFromSearchExtractor(result)

        if args.output:
            if args.output.lower().endswith(".csv"):
                df = formated_results.to_dataframe()
                df.to_csv(args.output)
        elif database_filename:
            for item in formated_results.to_dict():
                author_repository.upsert_by_link(item["author"])
                post_repository.upsert_by_linkedin_id(item["post"])

    elif args.command == "post-comment":
        posts_uncommented = post_repository.get_by_status(PostStatus.CREATED)
        post_comment(args, posts_uncommented, post_repository=post_repository)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    username = config("LINKEDIN_EMAIL")
    password = config("LINKEDIN_PASS")

    service_auth = LinkedinAuth(remote_browser_service)
    driver_key = remote_browser_service.open_browser()
    service_auth.execute(driver_key, username, password)
    service = LinkedinGetPosts(remote_browser_service)
    # TODO: passing default value, but planing for get these data from configuration
    finded_posts = service.execute(driver_key, "VAGAS + NODEJS + REMOTO", {"datePosted": "LAST_WEEK"})
    finded_posts = list(filter(lambda i: i is not None, finded_posts))
    remote_browser_service.close(driver_key)
    formated_results = PostsFromSearchExtractor(finded_posts)
    df = formated_results.to_dataframe()
