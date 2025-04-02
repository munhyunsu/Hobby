from fastapi import FastAPI, APIRouter, Depends, HTTPException, status as HTTPStatus

from . import database, models


models.Base.metadata.create_all(bind=database.engine)

router = APIRouter(
    prefix='/user-manager',
    tags=['User manager'],
    responses={404: {'description': 'Not Found'}},
)


@router.get('/info', include_in_schema=False)
async def get_info():
    return {'prefix': router.prefix,
            'tags': router.tags,
            'responses': router.responses}


