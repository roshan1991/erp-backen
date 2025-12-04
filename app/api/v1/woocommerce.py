from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
from sqlalchemy.orm import Session
import json
from datetime import datetime
from app.integrations.woocommerce_client import WooCommerceClient
from app.api import deps
from app.models.woocommerce_product import WooCommerceProduct
from app.crud import crud_woocommerce_settings
from app.schemas import woocommerce_settings as settings_schemas

router = APIRouter()

def get_woocommerce_client(db: Session = Depends(deps.get_db)):
    """Dependency to get WooCommerce API client with database credentials"""
    settings = crud_woocommerce_settings.get_settings(db)
    if not settings:
        raise HTTPException(status_code=404, detail="WooCommerce settings not configured")
    return WooCommerceClient(
        url=settings.store_url,
        consumer_key=settings.consumer_key,
        consumer_secret=settings.consumer_secret
    )

# Settings Endpoints
@router.get("/settings", response_model=settings_schemas.WooCommerceSettings)
def get_settings(
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_superuser)
):
    """Get WooCommerce settings (super admin only)"""
    settings = crud_woocommerce_settings.get_settings(db)
    if not settings:
        raise HTTPException(status_code=404, detail="WooCommerce settings not found")
    return settings

@router.put("/settings", response_model=settings_schemas.WooCommerceSettings)
def update_settings(
    settings_data: settings_schemas.WooCommerceSettingsUpdate,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_superuser)
):
    """Update WooCommerce settings (super admin only)"""
    settings = crud_woocommerce_settings.get_settings(db)
    if settings:
        # Update existing settings
        updated_settings = crud_woocommerce_settings.update_settings(db, settings.id, settings_data)
        return updated_settings
    else:
        # Create new settings if none exist
        create_data = settings_schemas.WooCommerceSettingsCreate(**settings_data.dict(exclude_unset=True))
        return crud_woocommerce_settings.create_settings(db, create_data)


# Product Endpoints
@router.get("/products")
def get_products(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    status: Optional[str] = None,
    client: WooCommerceClient = Depends(get_woocommerce_client),
    current_user = Depends(deps.get_current_active_user)
):
    """Get list of products from WooCommerce"""
    try:
        return client.get_products(page=page, per_page=per_page, search=search, status=status)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/products/{product_id}")
def get_product(
    product_id: int,
    client: WooCommerceClient = Depends(get_woocommerce_client),
    current_user = Depends(deps.get_current_active_user)
):
    """Get single product"""
    try:
        return client.get_product(product_id=product_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/products")
def create_product(
    product_data: dict,
    client: WooCommerceClient = Depends(get_woocommerce_client),
    current_user = Depends(deps.get_current_active_user)
):
    """Create a new product"""
    try:
        return client.create_product(product_data=product_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/products/{product_id}")
def update_product(
    product_id: int,
    product_data: dict,
    client: WooCommerceClient = Depends(get_woocommerce_client),
    current_user = Depends(deps.get_current_active_user)
):
    """Update a product"""
    try:
        return client.update_product(product_id=product_id, product_data=product_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    force: bool = Query(False),
    client: WooCommerceClient = Depends(get_woocommerce_client),
    current_user = Depends(deps.get_current_active_user)
):
    """Delete a product"""
    try:
        return client.delete_product(product_id=product_id, force=force)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Order Endpoints
@router.get("/orders")
def get_orders(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    status: Optional[str] = None,
    client: WooCommerceClient = Depends(get_woocommerce_client),
    current_user = Depends(deps.get_current_active_user)
):
    """Get list of orders"""
    try:
        return client.get_orders(page=page, per_page=per_page, status=status)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/orders/{order_id}")
def get_order(
    order_id: int,
    client: WooCommerceClient = Depends(get_woocommerce_client),
    current_user = Depends(deps.get_current_active_user)
):
    """Get single order"""
    try:
        return client.get_order(order_id=order_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/orders/{order_id}")
def update_order(
    order_id: int,
    order_data: dict,
    client: WooCommerceClient = Depends(get_woocommerce_client),
    current_user = Depends(deps.get_current_active_user)
):
    """Update an order"""
    try:
        return client.update_order(order_id=order_id, order_data=order_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Customer Endpoints
@router.get("/customers")
def get_customers(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    client: WooCommerceClient = Depends(get_woocommerce_client),
    current_user = Depends(deps.get_current_active_user)
):
    """Get list of customers"""
    try:
        return client.get_customers(page=page, per_page=per_page, search=search)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/customers/{customer_id}")
def get_customer(
    customer_id: int,
    client: WooCommerceClient = Depends(get_woocommerce_client),
    current_user = Depends(deps.get_current_active_user)
):
    """Get single customer"""
    try:
        return client.get_customer(customer_id=customer_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Coupon Endpoints
@router.get("/coupons")
def get_coupons(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    client: WooCommerceClient = Depends(get_woocommerce_client),
    current_user = Depends(deps.get_current_active_user)
):
    """Get list of coupons"""
    try:
        return client.get_coupons(page=page, per_page=per_page)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Category Endpoints
@router.get("/categories")
def get_categories(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    client: WooCommerceClient = Depends(get_woocommerce_client),
    current_user = Depends(deps.get_current_active_user)
):
    """Get list of product categories"""
    try:
        return client.get_categories(page=page, per_page=per_page)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Reports Endpoints
@router.get("/reports/sales")
def get_sales_report(
    period: str = Query("week", description="Period: week, month, last_month, year"),
    client: WooCommerceClient = Depends(get_woocommerce_client),
    current_user = Depends(deps.get_current_active_user)
):
    """Get sales report"""
    try:
        return client.get_sales_report(period=period)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/reports/top-sellers")
def get_top_sellers_report(
    period: str = Query("week"),
    client: WooCommerceClient = Depends(get_woocommerce_client),
    current_user = Depends(deps.get_current_active_user)
):
    """Get top sellers report"""
    try:
        return client.get_top_sellers_report(period=period)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/reports/totals")
def get_totals(
    client: WooCommerceClient = Depends(get_woocommerce_client),
    current_user = Depends(deps.get_current_active_user)
):
    """Get all totals (orders, products, customers)"""
    try:
        return {
            "orders": client.get_orders_totals(),
            "products": client.get_products_totals(),
            "customers": client.get_customers_totals()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Sync Endpoint
@router.post("/sync/products")
def sync_products(
    page: int = Query(1, ge=1),
    per_page: int = Query(100, ge=1, le=100),
    client: WooCommerceClient = Depends(get_woocommerce_client),
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    """Sync products from WooCommerce to local database"""
    try:
        # Fetch products from WooCommerce
        products = client.get_products(page=page, per_page=per_page)
        
        synced_count = 0
        updated_count = 0
        
        for product_data in products:
            # Check if product already exists
            existing_product = db.query(WooCommerceProduct).filter(
                WooCommerceProduct.woo_id == product_data['id']
            ).first()
            
            # Prepare product data
            product_dict = {
                'woo_id': product_data['id'],
                'name': product_data['name'],
                'slug': product_data['slug'],
                'permalink': product_data['permalink'],
                'type': product_data['type'],
                'status': product_data['status'],
                'featured': product_data.get('featured', False),
                'catalog_visibility': product_data.get('catalog_visibility', 'visible'),
                'description': product_data.get('description', ''),
                'short_description': product_data.get('short_description', ''),
                'sku': product_data.get('sku', ''),
                'price': float(product_data.get('price', 0) or 0),
                'regular_price': float(product_data.get('regular_price', 0) or 0),
                'sale_price': float(product_data.get('sale_price', 0) or 0) if product_data.get('sale_price') else None,
                'manage_stock': product_data.get('manage_stock', False),
                'stock_quantity': product_data.get('stock_quantity'),
                'stock_status': product_data.get('stock_status', 'instock'),
                'image_url': product_data['images'][0]['src'] if product_data.get('images') else None,
                'category_ids': ','.join([str(cat['id']) for cat in product_data.get('categories', [])]),
                'date_created': datetime.fromisoformat(product_data['date_created'].replace('Z', '+00:00')) if product_data.get('date_created') else None,
                'date_modified': datetime.fromisoformat(product_data['date_modified'].replace('Z', '+00:00')) if product_data.get('date_modified') else None,
                'raw_data': json.dumps(product_data)
            }
            
            if existing_product:
                # Update existing product
                for key, value in product_dict.items():
                    setattr(existing_product, key, value)
                updated_count += 1
            else:
                # Create new product
                new_product = WooCommerceProduct(**product_dict)
                db.add(new_product)
                synced_count += 1
        
        db.commit()
        
        return {
            "success": True,
            "synced": synced_count,
            "updated": updated_count,
            "total": synced_count + updated_count,
            "page": page,
            "per_page": per_page
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/local/products")
def get_local_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
):
    """Get products from local database"""
    try:
        query = db.query(WooCommerceProduct)
        
        if search:
            query = query.filter(
                (WooCommerceProduct.name.ilike(f"%{search}%")) |
                (WooCommerceProduct.sku.ilike(f"%{search}%"))
            )
        
        total = query.count()
        products = query.offset(skip).limit(limit).all()
        
        return {
            "total": total,
            "products": products
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
