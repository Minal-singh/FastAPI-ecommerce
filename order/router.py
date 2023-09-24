from fastapi import APIRouter, HTTPException, status
from datetime import datetime as dt
from database import Orders, Products
from order.serializer import order_serializer, order_list_serializer
from order.model import CreateOrder, Order
from bson.objectid import ObjectId

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_orders(page: int = 1, limit: int = 10) -> list[Order]:
    skip = (page - 1) * limit
    orders = order_list_serializer(Orders.find().skip(skip).limit(limit))
    return orders


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_order_by_id(id: str) -> Order:
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid id: {id}")
    order = Orders.find_one({"_id": ObjectId(id)})
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id: '{id}' not found")
    order = order_serializer(order)
    return order


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(order: CreateOrder) -> Order:
    order = dict(order)
    order["timestamp"] = dt.timestamp(dt.now())
    order["items"] = [dict(item) for item in order["items"]]
    order["user_address"] = dict(order["user_address"])
    order["amount"] = get_amount(order["items"])
    if order["amount"] == -1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid product(s) id")
    if order["amount"] == -2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="We don't have enough product(s) in stock")
    inserted_order = Orders.insert_one(order)
    inserted_order = Orders.find_one({"_id": inserted_order.inserted_id})
    inserted_order = order_serializer(inserted_order)
    return inserted_order


# Helper function
def get_amount(items: list):
    amount = 0
    products_map = {}  # to store product_id and quantity of products in order

    for item in items:
        if not ObjectId.is_valid(item["product_id"]):
            return -1

        product = Products.find_one({"_id": ObjectId(item["product_id"])})
        if product is None:
            return -1
        if product["quantity"] < item["quantity"]:
            return -2

        products_map[str(product["_id"])] = product["quantity"]
        amount += product["price"] * item["quantity"]

    # Update quantity of products in stock only if order is placed successfully
    for product_id, product_quantity in products_map.items():
        Products.update_one({"_id": ObjectId(product_id)}, {"$inc": {"quantity": -product_quantity}})
    return amount
