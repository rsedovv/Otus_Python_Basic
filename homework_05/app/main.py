from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import pages, products

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")  # Переносим инициализацию шаблонов сюда

app.include_router(pages.router)
app.include_router(products.router, prefix="/api", tags=["API"])

app.mount("/static", StaticFiles(directory="app/static"), name="static")  # Исправляем путь к статике