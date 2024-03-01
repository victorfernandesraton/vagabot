from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import uuid


class PostStatus(Enum):
    CREATED = 1
    COMMENTED = 2
    DELETED = 0


@dataclass(frozen=True)
class Post:
    likedin_id: str
    author_id: str
    content: str
    status: PostStatus
    id: Optional[uuid.UUID] = field(default_factory=lambda: None)

    def __post_init__(self):
        if self.id is None:
            self.id = uuid.uuid4()


class AuthorStatus(Enum):
    CREATED = 1
    FOLLOWED = 2
    MUTUAL = 3
    DELETED = 0


@dataclass(frozen=True)
class Author:
    id: Optional[uuid.UUID] = field(default_factory=lambda: None)
    linkedin_id: Optional[str] = ""
    name: str
    description: str
    link: str
    avatar: str
    status: AuthorStatus

    def __post_init__(self):
        if self.id is None:
            self.id = uuid.uuid4()
