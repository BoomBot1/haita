from fastapi import FastAPI
from src.core.config import settings
from src.api.v1.questions import router as questions_router
from src.api.v1.answers import router as answers_router

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(questions_router,  prefix=settings.API_V1_PREFIX)
app.include_router(answers_router, prefix=settings.API_V1_PREFIX)