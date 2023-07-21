from uuid import UUID

from pydantic import BaseModel


class Like(BaseModel):
    user_id: UUID
    film_id: UUID
    value: int
    collection: str = "likes"


class Reviews(BaseModel):
    user_id: UUID
    film_id: UUID
    review: str
    collection: str = "reviews"


class Bookmarks(BaseModel):
    film_id: UUID
    user_id: UUID
    collection: str = "bookmarks"
