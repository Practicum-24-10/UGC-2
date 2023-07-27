from uuid import UUID

from backend.src.models.model_mixin import ModelMixin


class Bookmarks(ModelMixin):
    film_id: UUID
