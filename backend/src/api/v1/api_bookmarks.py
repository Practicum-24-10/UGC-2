from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field

from backend.src.models.jwt import JWTPayload
from backend.src.services.autorization import get_token_payload

from backend.src.local.api.v1 import local_bookmarks as errors
from backend.src.services.service_bookmarks import (
    BookmarksService,
    get_bookmarks_service,
)

router = APIRouter()


class BookmarksResponse(BaseModel):
    film_id: str | None = Field(
        title="UUID Фильма", example="3fa85f64-5717-4562-b3fc-2c963f66afa6"
    )
    status: bool = Field(title="Успех", example=True)


class BookmarksPost(BaseModel):
    film_id: UUID = Field(
        title="UUID Фильма", example="3fa85f64-5717-4562-b3fc-2c963f66afa6"
    )


class BookmarksAll(BaseModel):
    bookmarks: list[BookmarksPost] = Field(title="Закладки")


@router.post(
    "/",
    response_description="Add new bookmarks",
    response_model=BookmarksResponse,
    summary="Добавить закладку",
)
async def add_bookmarks(
    bookmarks: BookmarksPost = Body(...),
    jwt: None | JWTPayload = Depends(get_token_payload),
    bookmarks_service: BookmarksService = Depends(get_bookmarks_service),
):
    if jwt is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=errors.NO_AUTHORIZED
        )
    user_id = jwt.user_id
    bookmarks_json = jsonable_encoder(bookmarks)
    await bookmarks_service.add_bookmarks(str(user_id), bookmarks_json)

    return BookmarksResponse(film_id=bookmarks_json["film_id"], status=True)


@router.get(
    "/",
    response_description="All bookmarks",
    response_model=BookmarksAll,
    summary="Получить все закладки",
)
async def get_all_bookmarks(
    jwt: None | JWTPayload = Depends(get_token_payload),
    bookmarks_service: BookmarksService = Depends(get_bookmarks_service),
):
    if jwt is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=errors.NO_AUTHORIZED
        )
    user_id = jwt.user_id
    user_bookmarks = await bookmarks_service.get_all_bookmarks(user_id)

    if user_bookmarks is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=errors.NOT_FOUND
        )
    return BookmarksAll(bookmarks=[film_id for film_id in user_bookmarks])


@router.delete(
    "/",
    response_description="Delete bookmarks",
    response_model=BookmarksResponse,
    summary="Удалить закладку",
)
async def delete_bookmarks(
    bookmarks: BookmarksPost = Body(...),
    jwt: None | JWTPayload = Depends(get_token_payload),
    bookmarks_service: BookmarksService = Depends(get_bookmarks_service),
):
    if jwt is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=errors.NO_AUTHORIZED
        )
    user_id = jwt.user_id
    bookmarks_json = jsonable_encoder(bookmarks)
    await bookmarks_service.delete_bookmarks(str(user_id), bookmarks_json)

    return BookmarksResponse(film_id=bookmarks_json["film_id"], status=True)
