from uuid import UUID

from pydantic import BaseModel


class JWTPayload(BaseModel):
    is_superuser: bool
    permissions: list[str]
    user_id: UUID
