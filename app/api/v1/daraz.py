from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional, List
from datetime import datetime, timedelta
from app.integrations.daraz_client import DarazAPIClient
from app.api import deps

router = APIRouter()

def get_daraz_client():
    """Dependency to get Daraz API client"""
    return DarazAPIClient()

# Product Endpoints
@router.get("/products")
def get_products(
    filter_type: str = Query("all", description="Filter type: all, live, inactive, deleted, image-missing, pending, rejected, sold-out"),
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    client: DarazAPIClient = Depends(get_daraz_client),
    current_user = Depends(deps.get_current_active_user)
):
    """Get list of products from Daraz"""
    try:
        return client.get_products(filter_type=filter_type, offset=offset, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/products/{item_id}")
def get_product(
    item_id: str,
    client: DarazAPIClient = Depends(get_daraz_client),
    current_user = Depends(deps.get_current_active_user)
):
    """Get single product details"""
    try:
        return client.get_product(item_id=item_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/products/price-quantity")
def update_price_quantity(
    seller_sku: str,
    quantity: int,
    price: float,
    client: DarazAPIClient = Depends(get_daraz_client),
    current_user = Depends(deps.get_current_active_user)
):
    """Update product price and quantity"""
    try:
        return client.update_price_quantity(seller_sku=seller_sku, quantity=quantity, price=price)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Order Endpoints
@router.get("/orders")
def get_orders(
    created_after: Optional[str] = Query(None, description="ISO format datetime"),
    created_before: Optional[str] = Query(None, description="ISO format datetime"),
    status: str = Query("pending", description="Order status: pending, ready_to_ship, shipped, delivered, canceled, returned"),
    client: DarazAPIClient = Depends(get_daraz_client),
    current_user = Depends(deps.get_current_active_user)
):
    """Get list of orders"""
    try:
        # Default to last 7 days if not specified
        if not created_after:
            created_after = (datetime.now() - timedelta(days=7)).isoformat()
        if not created_before:
            created_before = datetime.now().isoformat()
            
        return client.get_orders(created_after=created_after, created_before=created_before, status=status)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/orders/{order_id}")
def get_order(
    order_id: str,
    client: DarazAPIClient = Depends(get_daraz_client),
    current_user = Depends(deps.get_current_active_user)
):
    """Get single order details"""
    try:
        return client.get_order(order_id=order_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/orders/{order_id}/items")
def get_order_items(
    order_id: str,
    client: DarazAPIClient = Depends(get_daraz_client),
    current_user = Depends(deps.get_current_active_user)
):
    """Get order items"""
    try:
        return client.get_order_items(order_id=order_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/orders/ready-to-ship")
def set_ready_to_ship(
    order_item_ids: List[str],
    shipment_provider: str,
    tracking_number: str,
    client: DarazAPIClient = Depends(get_daraz_client),
    current_user = Depends(deps.get_current_active_user)
):
    """Set order status to ready to ship"""
    try:
        return client.set_status_to_ready_to_ship(
            order_item_ids=order_item_ids,
            shipment_provider=shipment_provider,
            tracking_number=tracking_number
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Category Endpoints
@router.get("/categories/tree")
def get_category_tree(
    client: DarazAPIClient = Depends(get_daraz_client),
    current_user = Depends(deps.get_current_active_user)
):
    """Get category tree"""
    try:
        return client.get_category_tree()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/categories/{category_id}/attributes")
def get_category_attributes(
    category_id: int,
    client: DarazAPIClient = Depends(get_daraz_client),
    current_user = Depends(deps.get_current_active_user)
):
    """Get category attributes"""
    try:
        return client.get_category_attributes(primary_category_id=category_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/categories/{category_id}/brands")
def get_category_brands(
    category_id: int,
    client: DarazAPIClient = Depends(get_daraz_client),
    current_user = Depends(deps.get_current_active_user)
):
    """Get brands for category"""
    try:
        return client.get_category_brands(primary_category_id=category_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Seller Endpoints
@router.get("/seller/info")
def get_seller_info(
    client: DarazAPIClient = Depends(get_daraz_client),
    current_user = Depends(deps.get_current_active_user)
):
    """Get seller information"""
    try:
        return client.get_seller_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/seller/performance")
def get_seller_performance(
    client: DarazAPIClient = Depends(get_daraz_client),
    current_user = Depends(deps.get_current_active_user)
):
    """Get seller performance metrics"""
    try:
        return client.get_seller_performance()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Logistics Endpoints
@router.get("/logistics/shipment-providers")
def get_shipment_providers(
    client: DarazAPIClient = Depends(get_daraz_client),
    current_user = Depends(deps.get_current_active_user)
):
    """Get available shipment providers"""
    try:
        return client.get_shipment_providers()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Finance Endpoints
@router.get("/finance/transactions")
def get_transaction_details(
    start_time: str = Query(..., description="ISO format datetime"),
    end_time: str = Query(..., description="ISO format datetime"),
    client: DarazAPIClient = Depends(get_daraz_client),
    current_user = Depends(deps.get_current_active_user)
):
    """Get transaction details"""
    try:
        return client.get_transaction_details(start_time=start_time, end_time=end_time)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
