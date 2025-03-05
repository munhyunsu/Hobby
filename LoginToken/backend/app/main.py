from fastapi import FastAPI

from . import conf


app = FastAPI(
    root_path=conf.URLPREFIX
)


@app.get('/info', include_in_schema=False)
async def get_info():
    return {'message': 'Hello, World!'}

