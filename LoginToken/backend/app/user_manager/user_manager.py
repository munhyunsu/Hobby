from fastapi import FastAPI, APIRouter, Depends, HTTPException, status as HTTPStatus

from . import database, models


models.Base.metadata.create_all(bind=database.engine)
