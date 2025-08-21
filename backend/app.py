from .database import database
from fastapi import FastAPI
from .models import models
from .routers import metrics

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(metrics.router, prefix="/api", tags=["Metrics"])
