from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean
from sqlalchemy.sql import func
from app.db.base import Base


class WooCommerceProduct(Base):
    __tablename__ = "woocommerce_products"

    id = Column(Integer, primary_key=True, index=True)
    woo_id = Column(Integer, unique=True, index=True, nullable=False)  # WooCommerce product ID
    name = Column(String(255), nullable=False)
    slug = Column(String(255), index=True)
    permalink = Column(String(500))
    
    # Product details
    type = Column(String(50))  # simple, grouped, external, variable
    status = Column(String(50))  # draft, pending, private, publish
    featured = Column(Boolean, default=False)
    catalog_visibility = Column(String(50))  # visible, catalog, search, hidden
    description = Column(Text)
    short_description = Column(Text)
    sku = Column(String(100), index=True)
    
    # Pricing
    price = Column(Float)
    regular_price = Column(Float)
    sale_price = Column(Float)
    
    # Inventory
    manage_stock = Column(Boolean, default=False)
    stock_quantity = Column(Integer)
    stock_status = Column(String(50))  # instock, outofstock, onbackorder
    
    # Images (storing first image URL)
    image_url = Column(String(500))
    
    # Categories (storing as comma-separated IDs)
    category_ids = Column(String(255))
    
    # Timestamps
    date_created = Column(DateTime(timezone=True))
    date_modified = Column(DateTime(timezone=True))
    synced_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Additional data stored as JSON string if needed
    raw_data = Column(Text)  # Store full JSON response for reference
