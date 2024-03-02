from typing import List

from bs4 import BeautifulSoup

from vagabot.entities import Author, Post


class PostsFromSearchExtractor:
    AUTHOR_TITLE_SELECTOR = (
        "li div.update-components-actor div .update-components-actor__title"
    )
    AUTHOR_DESCRIPTION_SELECTOR = (
        "li div.update-components-actor div .update-components-actor__description"
    )
    AUTHOR_AVATAR_SELECTOR = "li div.update-components-actor div  a.app-aware-link"
    POST_CONTENT_SELECTOR = "li div.update-components-text span.break-words"
    POST_LINK_SELECTOR = "li div.feed-shared-update-v2"

    def __init__(self, posts: List[str]) -> None:
        self.posts = posts

    def __get_author(self, soup: BeautifulSoup) -> Author:
        avatar = soup.select_one(self.AUTHOR_AVATAR_SELECTOR)
        return Author(
            name=soup.select_one(self.AUTHOR_TITLE_SELECTOR).text.replace("\n", ""),
            description=soup.select_one(self.AUTHOR_DESCRIPTION_SELECTOR).text,
            avatar=avatar.find("img").get("src"),
            link=avatar.get("href"),
        )

    def __get_publication(self, soup: BeautifulSoup, author: Author) -> Post:
        urn = soup.select_one(self.POST_LINK_SELECTOR).get("data-urn")

        return Post(
            linkedin_id=urn,
            link=f"https://www.linkedin.com/feed/update/{urn}",
            author_id=author.id,
            content=soup.select_one(self.POST_CONTENT_SELECTOR).text,
        )

    def __to_dict(self, post: str) -> dict:
        soup = BeautifulSoup(post, features="lxml")
        urn = soup.select_one(self.POST_LINK_SELECTOR)
        if not urn:
            return None

        author = self.__get_author(soup)
        post = self.__get_publication(soup, author)
        return {"author": author, "post": post}

    def to_dict(self) -> List[dict]:
        result = []
        for idx, post_content in enumerate(self.posts):
            post = self.__to_dict(post_content)
            if not post:
                print(f"Not found valid content in post[{idx}]")
            else:
                result.append(post)

        return result
