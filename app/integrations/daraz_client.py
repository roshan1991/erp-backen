import hashlib
import hmac
import time
from typing import Dict, Any, Optional
import requests
from app.core.config import settings


class DarazAPIClient:
    """Client for interacting with Daraz Open Platform API"""
    
    def __init__(self):
        self.app_key = settings.DARAZ_APP_KEY
        self.app_secret = settings.DARAZ_APP_SECRET
        self.api_url = settings.DARAZ_API_URL
        
    def _generate_signature(self, params: Dict[str, Any]) -> str:
        """Generate HMAC-SHA256 signature for API request"""
        # Sort parameters by key
        sorted_params = sorted(params.items())
        
        # Concatenate parameters
        param_str = "".join([f"{k}{v}" for k, v in sorted_params])
        
        # Generate signature
        signature = hmac.new(
            self.app_secret.encode('utf-8'),
            param_str.encode('utf-8'),
            hashlib.sha256
        ).hexdigest().upper()
        
        return signature
    
    def _make_request(self, api_name: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make authenticated request to Daraz API"""
        if params is None:
            params = {}
        
        # Add common parameters
        common_params = {
            "app_key": self.app_key,
            "timestamp": str(int(time.time() * 1000)),
            "sign_method": "sha256",
            "format": "json",
            "v": "1.0",
        }
        
        # Merge with custom parameters
        all_params = {**common_params, **params}
        
        # Generate signature
        all_params["sign"] = self._generate_signature(all_params)
        
        # Make request
        url = f"{self.api_url}?method={api_name}"
        response = requests.get(url, params=all_params)
        response.raise_for_status()
        
        return response.json()
    
    # Product APIs
    def get_products(self, filter_type: str = "all", offset: int = 0, limit: int = 50) -> Dict[str, Any]:
        """Get list of products"""
        return self._make_request("/products/get", {
            "filter": filter_type,
            "offset": offset,
            "limit": limit
        })
    
    def get_product(self, item_id: str) -> Dict[str, Any]:
        """Get single product details"""
        return self._make_request("/product/item/get", {"item_id": item_id})
    
    def create_product(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Create new product"""
        return self._make_request("/product/create", payload)
    
    def update_product(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Update existing product"""
        return self._make_request("/product/update", payload)
    
    def update_price_quantity(self, seller_sku: str, quantity: int, price: float) -> Dict[str, Any]:
        """Update product price and quantity"""
        return self._make_request("/product/price_quantity/update", {
            "seller_sku": seller_sku,
            "quantity": quantity,
            "price": price
        })
    
    # Order APIs
    def get_orders(self, created_after: str, created_before: str, status: str = "pending") -> Dict[str, Any]:
        """Get list of orders"""
        return self._make_request("/orders/get", {
            "created_after": created_after,
            "created_before": created_before,
            "status": status
        })
    
    def get_order(self, order_id: str) -> Dict[str, Any]:
        """Get single order details"""
        return self._make_request("/order/get", {"order_id": order_id})
    
    def get_order_items(self, order_id: str) -> Dict[str, Any]:
        """Get order items"""
        return self._make_request("/order/items/get", {"order_id": order_id})
    
    def set_status_to_ready_to_ship(self, order_item_ids: list, shipment_provider: str, tracking_number: str) -> Dict[str, Any]:
        """Set order status to ready to ship"""
        return self._make_request("/order/rts", {
            "order_item_ids": order_item_ids,
            "shipment_provider": shipment_provider,
            "tracking_number": tracking_number
        })
    
    # Category APIs
    def get_category_tree(self) -> Dict[str, Any]:
        """Get category tree"""
        return self._make_request("/category/tree/get")
    
    def get_category_attributes(self, primary_category_id: int) -> Dict[str, Any]:
        """Get category attributes"""
        return self._make_request("/category/attributes/get", {
            "primary_category_id": primary_category_id
        })
    
    def get_category_brands(self, primary_category_id: int) -> Dict[str, Any]:
        """Get brands for category"""
        return self._make_request("/category/brands/query", {
            "primary_category_id": primary_category_id
        })
    
    # Seller APIs
    def get_seller_info(self) -> Dict[str, Any]:
        """Get seller information"""
        return self._make_request("/seller/get")
    
    def get_seller_performance(self) -> Dict[str, Any]:
        """Get seller performance metrics"""
        return self._make_request("/seller/performance/get")
    
    # Logistics APIs
    def get_shipment_providers(self) -> Dict[str, Any]:
        """Get available shipment providers"""
        return self._make_request("/shipment/providers/get")
    
    # Finance APIs
    def get_transaction_details(self, start_time: str, end_time: str) -> Dict[str, Any]:
        """Get transaction details"""
        return self._make_request("/finance/transaction/details/get", {
            "start_time": start_time,
            "end_time": end_time
        })
