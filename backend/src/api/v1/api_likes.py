from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response, JSONResponse
from http import HTTPStatus

from backend.src.models.model_likes import Like
from backend.src.services.service_likes import LikeService, get_like_service

router = APIRouter()


@router.post("/", response_description="Add new like",
             response_model=Like)
async def create_student(like: Like = Body(...),
                         like_service: LikeService = Depends(
                             get_like_service)
                         ):
    like_js = jsonable_encoder(like)
    new_like_id = await like_service.add_like(like_js)
    created_new_like = await like_service.get_like(like.user_id, like.film_id)
    return JSONResponse(status_code=HTTPStatus.OK,
                        content=created_new_like)
