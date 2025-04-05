from fastapi import FastAPI, APIRouter, Depends, HTTPException, status as HTTPStatus


router = APIRouter(
    prefix='/token-manager',
    tags=['Token manager'],
    responses={404: {'description': 'Not Found'}},
)


@router.get('/info', include_in_schema=False)
async def get_info():
    return {'prefix': router.prefix,
            'tags': router.tags,
            'responses': router.responses}

