from uuid import UUID

from backend.src.models.model_mixin import ModelMixin


class JWTPayload(ModelMixin):
    is_superuser: bool
    permissions: list[str]
    user_id: UUID
