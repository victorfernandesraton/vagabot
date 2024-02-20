from vagabot.workflows.linkedin_get_posts import LinkedinGetPosts
from vagabot.adapters.posts_from_search_adapters import PostsFromSearchExtractor

service = LinkedinGetPosts()
posts = service.execute("vagas + javascript")
posts_adapter = PostsFromSearchExtractor(posts)
result = posts_adapter.to_dict()
print(result)
