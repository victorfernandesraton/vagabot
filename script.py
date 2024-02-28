import argparse
from vagabot.workflows.linkedin_get_posts import LinkedinGetPosts
from decouple import config

import sys


def search_posts(args):
    """
    Function to search posts.
    """
    service = LinkedinGetPosts()
    print(f"Searching posts with query: {args.query} in {args.user}")
    service.execute(args.query, args.user, args.password)


def post_comment(args):
    """
    Function to post a comment.
    """
    print(f"Posting comment: {args.comment}")


def main():
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
        search_posts(args)
    elif args.command == "post-comment":
        post_comment(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
