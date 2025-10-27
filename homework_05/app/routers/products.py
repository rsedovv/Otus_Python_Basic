from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class Product(BaseModel):
    name: str
    price: float
    description: str | None = None

products_db = []

@router.get("/products")
async def read_products():
    return products_db

@router.get("/products/{product_id}")
async def read_product(product_id: int):
    if product_id >= len(products_db):
        raise HTTPException(status_code=404, detail="Product not found")
    return products_db[product_id]

@router.post("/products")
async def create_product(product: Product):
    products_db.append(product.dict())
    return {"message": "Product created"}