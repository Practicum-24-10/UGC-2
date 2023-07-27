from uuid import UUID

from backend.src.models.model_mixin import ModelMixin


class Like(ModelMixin):
    film_id: UUID
    value: int
