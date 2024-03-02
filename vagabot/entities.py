import uuid
from dataclasses import dataclass, field
from enum import Enum


class PostStatus(Enum):
    CREATED = 1
    COMMENTED = 2
    DELETED = 0


@dataclass(frozen=True, order=True)
class Post:
    linkedin_id: str
    link: str
    author_id: str
    content: str
    status: PostStatus = PostStatus.CREATED
    id: str = field(default_factory=lambda: str(uuid.uuid4()))


class AuthorStatus(Enum):
    CREATED = 1
    FOLLOWED = 2
    MUTUAL = 3
    DELETED = 0


@dataclass(frozen=True, order=True)
class Author:
    name: str
    link: str
    avatar: str = ""
    status: AuthorStatus = AuthorStatus.CREATED
    description: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid1()))
