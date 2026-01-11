# Pydantic schemas (for API validation)
from .product import Product, ProductCreate, ProductUpdate
from .customer import Customer, CustomerCreate, CustomerUpdate

# SQLAlchemy models (for database)
from .product_model import ProductModel
from .customer_model import CustomerModel

__all__ = [
    # Pydantic
    "Product", "ProductCreate", "ProductUpdate",
    "Customer", "CustomerCreate", "CustomerUpdate",
    # SQLAlchemy
    "ProductModel", "CustomerModel",
]
