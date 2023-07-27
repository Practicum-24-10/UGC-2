from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, Path
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field

from backend.src.local.api.v1 import local_reviews as errors
from backend.src.models.jwt import JWTPayload
from backend.src.models.pagination import PaginatedParams
from backend.src.services.autorization import get_token_payload
from backend.src.services.service_reviews import ReviewsService, get_reviews_service

router = APIRouter()


class Reviews(BaseModel):
    film_id: UUID = Field(
        title="UUID Фильма", example="3fa85f64-5717-4562-b3fc-2c963f66afa6"
    )
    review: str = Field(
        title="Рецензия", example="Райан Гослинг в этом фильме буквально я",
        max_length=300
    )


class ReviewsDelete(BaseModel):
    film_id: UUID = Field(
        title="UUID Фильма", example="3fa85f64-5717-4562-b3fc-2c963f66afa6"
    )


class ReviewsResponse(BaseModel):
    review_id: str | None = Field(title="ID Рецензии",
                                  example="64c046134ba01daa94d5e59c")
    status: bool = Field(title="Успех", example=True)


class ReviewGet(BaseModel):
    review: str = Field(
        title="Рецензия", example="Знаешь откуда эти шрамы?",
        max_length=300
    )
    review_id: str = Field(title="ID Рецензии",
                           example="64c046134ba01daa94d5e59c")
    user_id: str = Field(title="UUID пользователя",
                         example="9b3c278c-665f-4055-a824-891f19cb4993")


class ReviewsGetList(BaseModel):
    user_review_id: str | None = Field(title="ID Рецензии",
                                       example="64c046134ba01daa94d5e59c")
    reviews: list[ReviewGet] = Field(title="Рецензии")


@router.post(
    "/",
    response_description="Add new Review",
    response_model=ReviewsResponse,
    summary="Добавление рецензии",
)
async def add_review(
        review: Reviews = Body(...),
        jwt: None | JWTPayload = Depends(get_token_payload),
        review_service: ReviewsService = Depends(get_reviews_service),
):
    if jwt is None:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail=errors.NO_AUTHORIZED
        )
    user_id = jwt.user_id
    review_id = await review_service.get_review(user_id, review.film_id)
    if review_id is None:
        review_js = jsonable_encoder(review)
        new_review_id = await review_service.add_review(str(user_id),
                                                        review_js)
        if new_review_id is None:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail=errors.NOT_FOUND
            )
        return ReviewsResponse(review_id=str(new_review_id), status=True)
    raise HTTPException(status_code=HTTPStatus.CONFLICT,
                        detail=errors.CONFLICT)


@router.put(
    "/",
    response_description="Add new Review",
    response_model=ReviewsResponse,
    summary="Изменение рецензии",
)
async def change_review(
        review_new: Reviews = Body(...),
        jwt: None | JWTPayload = Depends(get_token_payload),
        review_service: ReviewsService = Depends(get_reviews_service),
):
    if jwt is None:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail=errors.NO_AUTHORIZED
        )
    user_id = jwt.user_id
    review_old = await review_service.get_review(user_id, review_new.film_id)
    if review_old is not None:
        result = await review_service.change_review(review_old['_id'],
                                                    review_new.review)
        if not result:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail=errors.NOT_CHANGE
            )
        return ReviewsResponse(review_id=str(review_old['_id']), status=True)
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                        detail=errors.NOT_FOUND)


@router.delete(
    "/",
    response_description="Delet new Review",
    response_model=ReviewsResponse,
    summary="Удаление рецензии",
)
async def delete_review(
        review_del: ReviewsDelete = Body(...),
        jwt: None | JWTPayload = Depends(get_token_payload),
        review_service: ReviewsService = Depends(get_reviews_service),
):
    if jwt is None:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail=errors.NO_AUTHORIZED
        )
    user_id = jwt.user_id
    review = await review_service.get_review(user_id, review_del.film_id)
    if review is not None:
        result = await review_service.del_review(review['_id'])
        if not result:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail=errors.NOT_DELETE
            )
        return ReviewsResponse(review_id=str(review['_id']), status=True)
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                        detail=errors.NOT_FOUND)


@router.get(
    "/{film_id}",
    response_description="All reviews",
    response_model=ReviewsGetList,
    summary="Получение всех рецензий фильма",
)
async def get_reviews(
        film_id: Annotated[UUID, Path(
            description="UUID фильма",
            example="9b3c278c-665f-4055-a824-891f19cb4993"
        )],
        pagination: PaginatedParams = Depends(),
        jwt: None | JWTPayload = Depends(get_token_payload),
        review_service: ReviewsService = Depends(get_reviews_service),
):
    if jwt is not None:
        user_id = jwt.user_id
        user_review = await review_service.get_review(user_id, film_id)
    else:
        user_review = None
    reviews = await review_service.get_reviews(film_id=str(film_id),
                                               size=pagination.size,
                                               page=pagination.page)
    if reviews is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=errors.NOT_FOUND)
    return ReviewsGetList(
        user_review_id=None if user_review is None else str(user_review['_id']),
        reviews=[ReviewGet(review=i['review'],
                           review_id=str(i['_id']),
                           user_id=i['user_id']) for i in reviews]
    )
