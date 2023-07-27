from uuid import UUID

from backend.src.models.model_mixin import OrjsonMixin


class Like(OrjsonMixin):
    film_id: UUID
    value: int
