from typing import List
from bs4 import BeautifulSoup


class PostsFromSearchExtractor:
    AUTHOR_TITLE_SELECTOR = (
        "div.update-components-actor div .update-components-actor__title"
    )
    AUTHOR_DESCRIPTION_SELECTOR = (
        "div.update-components-actor div .update-components-actor__description"
    )
    AUTHOR_AVATAR_SELECTOR = "div.update-components-actor div  a.app-aware-link"
    POST_CONTENT_SELECTOR = "div.update-components-text span.break-words"
    POST_LINK_SELECTOR = "a.app-aware-link"

    def __init__(self, posts: List[str]) -> None:
        self.posts = posts

    def __get_author(self, soup: BeautifulSoup) -> dict:
        avatar = soup.select_one(self.AUTHOR_AVATAR_SELECTOR)
        return {
            "title": soup.select_one(self.AUTHOR_TITLE_SELECTOR).text,
            "description": soup.select_one(self.AUTHOR_DESCRIPTION_SELECTOR).text,
            "link": avatar.get("href"),
            "avatar_url": avatar.find("img").get("src"),
        }

    def __get_publication(self, soup: BeautifulSoup) -> dict:
        return {
            "content": soup.select_one(self.POST_CONTENT_SELECTOR).text,
            "link": soup.select_one(self.POST_LINK_SELECTOR).get("href"),
        }

    def __to_dict(self, post: str) -> dict:
        soup = BeautifulSoup(post)
        return {
            "author": self.__get_author(soup),
            "post": self.__get_publication(soup),
        }

    def to_dict(self) -> List[dict]:
        return [self.__to_dict(post) for post in self.posts]

    def __str__(self) -> str:
        return "\n".join(str(post) for post in self.to_dict())
