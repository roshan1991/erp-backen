from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

# Import all models here for Alembic
from app.models.woocommerce_product import WooCommerceProduct  # noqa
from app.models.product import Product  # noqa
from app.models.coupon import Coupon  # noqa
from app.models.loyalty_settings import LoyaltySettings  # noqa
