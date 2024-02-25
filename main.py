from vagabot.workflows.linkedin_get_posts import LinkedinGetPosts
from vagabot.adapters.posts_from_search_adapters import PostsFromSearchExtractor
from vagabot.workflows.linkedin_comment_post import LinkedinCommentPost

service = LinkedinGetPosts()
posts = service.execute("vagas + javascript")
print(posts[1])
posts_adapter = PostsFromSearchExtractor(posts)
result = posts_adapter.to_dict()
print(result)

service2 = LinkedinCommentPost("Quero me candidatar, entre em contato comigo")
service2.execute(result)
