from pydantic import BaseModel


class CreateProduct(BaseModel):
    name: str
    price: float
    quantity: int

    model_config = {"json_schema_extra": {"examples": [{"name": "Product 1", "price": 100.0, "quantity": 10}]}}


class Product(CreateProduct):
    id: str
    model_config = {
        "json_schema_extra": {
            "examples": [{"id": "60f1b2b9c9e9f9b3f0f3e4a1", "name": "Product 1", "price": 100.0, "quantity": 10}]
        }
    }
