from uuid import UUID

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class Like(BaseModel):
    user_id: UUID
    film_id: UUID
    value: int
