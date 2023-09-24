from fastapi import FastAPI
from order.router import router as order_router
from product.router import router as product_router

app = FastAPI()

app.include_router(order_router, prefix="/order", tags=["order"])
app.include_router(product_router, prefix="/product", tags=["product"])


@app.get("/ping")
async def ping():
    return "pong"