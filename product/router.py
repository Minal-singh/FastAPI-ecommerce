from fastapi import APIRouter, HTTPException, status
from product.serializer import product_serializer, product_list_serializer
from product.model import Product, CreateProduct
from database import Products
from bson.objectid import ObjectId

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_products(page: int = 1, limit: int = 10) -> list[Product]:
    skip = (page - 1) * limit
    products = product_list_serializer(Products.find().skip(skip).limit(limit))
    return products


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_product_by_id(id: str) -> Product:
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid id: {id}")
    product = Products.find_one({"_id": ObjectId(id)})
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id: '{id}' not found")
    product = product_serializer(product)
    return product


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(product: CreateProduct) -> Product:
    inserted_product = Products.insert_one(dict(product))
    inserted_product = Products.find_one({"_id": inserted_product.inserted_id})
    inserted_product = product_serializer(inserted_product)
    return inserted_product


@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_product(id: str, product: CreateProduct) -> Product:
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid id: {id}")
    updated_product = Products.update_one({"_id": ObjectId(id)}, {"$set": dict(product)})
    if updated_product.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id: '{id}' not found")
    updated_product = product_serializer(Products.find_one({"_id": ObjectId(id)}))
    return updated_product
