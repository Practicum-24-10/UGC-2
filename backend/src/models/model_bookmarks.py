from uuid import UUID

from backend.src.models.model_mixin import OrjsonMixin


class Bookmarks(OrjsonMixin):
    film_id: UUID
