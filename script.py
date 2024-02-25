import argparse
from vagabot.workflows.linkedin_get_posts import LinkedinGetPosts


def search_posts(args):
    query = args.a
    print(f"Searching posts with query: {query}")
    service = LinkedinGetPosts()
    service.execute(query)


def comment_post(args):
    print(f"Commenting on post with text: {args.a}")


# Configurando o parser de argumentos
parser = argparse.ArgumentParser(
    description="CLI for searching and commenting on posts"
)
subparsers = parser.add_subparsers()

# Comando search-posts
search_parser = subparsers.add_parser("search-posts")
search_parser.add_argument("-a", required=True, help="Query + Info")
search_parser.set_defaults(func=search_posts)

# Comando comment-post
comment_parser = subparsers.add_parser("comment-post")
comment_parser.add_argument("-a", required=True, help="Text to comment")
comment_parser.set_defaults(func=comment_post)

# Parse dos argumentos e chamada da função correspondente
args = parser.parse_args()
args.func(args)
