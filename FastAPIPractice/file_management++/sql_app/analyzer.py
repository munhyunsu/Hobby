import os
import importlib

from contextlib import asynccontextmanager
from fastapi import FastAPI

from . import models
from .database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup codes

    yield
    # Shutdown codes
    models.Base.metadata.drop_all(bind=engine)

