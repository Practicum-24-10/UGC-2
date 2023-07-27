from uuid import UUID

from pydantic import BaseModel


class Like(BaseModel):
    user_id: str
    film_id: str
    value: int
    collection: str = "likes"


class Reviews(BaseModel):
    user_id: str
    film_id: str
    review: str
    collection: str = "reviews"


class Bookmarks(BaseModel):
    film_id: str
    user_id: str
    collection: str = "bookmarks"
