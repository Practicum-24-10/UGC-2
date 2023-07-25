from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from http import HTTPStatus
from backend.src.models.jwt import JWTPayload
from backend.src.services.autorization import get_token_payload
from backend.src.local.api.v1 import local_likes as errors
from backend.src.services.service_likes import LikeService, get_like_service
from pydantic import BaseModel, Field

router = APIRouter()


class LikeResponse(BaseModel):
    like_id: str | None = Field(title="ID Лайка",
                                example="64c046134ba01daa94d5e59c")
    status: bool = Field(title="Успех", example=True)


class LikePost(BaseModel):
    film_id: UUID = Field(title="UUID Фильма",
                          example="3fa85f64-5717-4562-b3fc-2c963f66afa6")
    value: int = Field(title="Лайк",
                       ge=0, le=1,
                       example=1)


@router.post("/", response_description="Add new like",
             response_model=LikeResponse,
             summary="Добавление/Удаление лайка")
async def dell_add_like(like: LikePost = Body(...),
                         jwt: None | JWTPayload = Depends(get_token_payload),
                         like_service: LikeService = Depends(
                             get_like_service)
                         ):
    if jwt is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=errors.NO_AUTHORIZED)
    user_id = jwt.user_id
    like_id = await like_service.get_like(user_id, like.film_id)
    if like_id is None:
        like_js = jsonable_encoder(like)
        new_like_id = await like_service.add_like(str(user_id), like_js)
        if new_like_id is None:
            raise HTTPException(status_code=HTTPStatus.CONFLICT,
                                detail=errors.NOT_FOUND)
        return LikeResponse(like_id=str(new_like_id), status=True)
    del_result = await like_service.dell_like(like_id)
    if del_result:
        return LikeResponse(like_id=None, status=True)
    raise HTTPException(status_code=HTTPStatus.CONFLICT,
                        detail=errors.NOT_FOUND)
