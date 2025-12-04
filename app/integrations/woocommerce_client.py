import requests
from requests.auth import HTTPBasicAuth
from typing import Dict, Any, List, Optional
from app.core.config import settings


class WooCommerceClient:
    """Client for WooCommerce REST API v3"""
    
    def __init__(self, url: str = None, consumer_key: str = None, consumer_secret: str = None):
        # Use provided credentials or fall back to environment variables
        self.url = (url or settings.WOOCOMMERCE_URL).rstrip('/')
        self.consumer_key = consumer_key or settings.WOOCOMMERCE_CONSUMER_KEY
        self.consumer_secret = consumer_secret or settings.WOOCOMMERCE_CONSUMER_SECRET
        self.api_base = f"{self.url}/wp-json/wc/v3"
        self.auth = HTTPBasicAuth(self.consumer_key, self.consumer_secret)
    
    def _make_request(self, endpoint: str, method: str = "GET", params: Optional[Dict] = None, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make authenticated request to WooCommerce API"""
        url = f"{self.api_base}/{endpoint}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Add consumer key and secret to params for query string auth
        # This is required for some server configurations
        if params is None:
            params = {}
        params["consumer_key"] = self.consumer_key
        params["consumer_secret"] = self.consumer_secret
        
        try:
            if method == "GET":
                response = requests.get(url, params=params, headers=headers, timeout=30)
            elif method == "POST":
                response = requests.post(url, params=params, json=data, headers=headers, timeout=30)
            elif method == "PUT":
                response = requests.put(url, params=params, json=data, headers=headers, timeout=30)
            elif method == "DELETE":
                response = requests.delete(url, params=params, headers=headers, timeout=30)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            # Log the request for debugging
            print(f"WooCommerce API Request: {method} {url}")
            print(f"Response Status: {response.status_code}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            print(f"Response Text: {response.text}")
            raise Exception(f"WooCommerce API Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Request Error: {e}")
            raise
    
    # Product APIs
    def get_products(self, page: int = 1, per_page: int = 10, search: Optional[str] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get list of products"""
        params = {"page": page, "per_page": per_page}
        if search:
            params["search"] = search
        if status:
            params["status"] = status
        return self._make_request("products", params=params)
    
    def get_product(self, product_id: int) -> Dict[str, Any]:
        """Get single product"""
        return self._make_request(f"products/{product_id}")
    
    def create_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new product"""
        return self._make_request("products", method="POST", data=product_data)
    
    def update_product(self, product_id: int, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a product"""
        return self._make_request(f"products/{product_id}", method="PUT", data=product_data)
    
    def delete_product(self, product_id: int, force: bool = False) -> Dict[str, Any]:
        """Delete a product"""
        params = {"force": force}
        return self._make_request(f"products/{product_id}", method="DELETE", params=params)
    
    # Order APIs
    def get_orders(self, page: int = 1, per_page: int = 10, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get list of orders"""
        params = {"page": page, "per_page": per_page}
        if status:
            params["status"] = status
        return self._make_request("orders", params=params)
    
    def get_order(self, order_id: int) -> Dict[str, Any]:
        """Get single order"""
        return self._make_request(f"orders/{order_id}")
    
    def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new order"""
        return self._make_request("orders", method="POST", data=order_data)
    
    def update_order(self, order_id: int, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an order"""
        return self._make_request(f"orders/{order_id}", method="PUT", data=order_data)
    
    # Customer APIs
    def get_customers(self, page: int = 1, per_page: int = 10, search: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get list of customers"""
        params = {"page": page, "per_page": per_page}
        if search:
            params["search"] = search
        return self._make_request("customers", params=params)
    
    def get_customer(self, customer_id: int) -> Dict[str, Any]:
        """Get single customer"""
        return self._make_request(f"customers/{customer_id}")
    
    def create_customer(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new customer"""
        return self._make_request("customers", method="POST", data=customer_data)
    
    def update_customer(self, customer_id: int, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a customer"""
        return self._make_request(f"customers/{customer_id}", method="PUT", data=customer_data)
    
    def delete_customer(self, customer_id: int, force: bool = False) -> Dict[str, Any]:
        """Delete a customer"""
        params = {"force": force}
        return self._make_request(f"customers/{customer_id}", method="DELETE", params=params)
    
    # Coupon APIs
    def get_coupons(self, page: int = 1, per_page: int = 10) -> List[Dict[str, Any]]:
        """Get list of coupons"""
        params = {"page": page, "per_page": per_page}
        return self._make_request("coupons", params=params)
    
    def get_coupon(self, coupon_id: int) -> Dict[str, Any]:
        """Get single coupon"""
        return self._make_request(f"coupons/{coupon_id}")
    
    def create_coupon(self, coupon_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new coupon"""
        return self._make_request("coupons", method="POST", data=coupon_data)
    
    def update_coupon(self, coupon_id: int, coupon_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a coupon"""
        return self._make_request(f"coupons/{coupon_id}", method="PUT", data=coupon_data)
    
    def delete_coupon(self, coupon_id: int, force: bool = False) -> Dict[str, Any]:
        """Delete a coupon"""
        params = {"force": force}
        return self._make_request(f"coupons/{coupon_id}", method="DELETE", params=params)
    
    # Category APIs
    def get_categories(self, page: int = 1, per_page: int = 10) -> List[Dict[str, Any]]:
        """Get list of product categories"""
        params = {"page": page, "per_page": per_page}
        return self._make_request("products/categories", params=params)
    
    def get_category(self, category_id: int) -> Dict[str, Any]:
        """Get single category"""
        return self._make_request(f"products/categories/{category_id}")
    
    # Reports APIs
    def get_sales_report(self, period: str = "week") -> Dict[str, Any]:
        """Get sales report"""
        params = {"period": period}
        return self._make_request("reports/sales", params=params)
    
    def get_top_sellers_report(self, period: str = "week") -> List[Dict[str, Any]]:
        """Get top sellers report"""
        params = {"period": period}
        return self._make_request("reports/top_sellers", params=params)
    
    def get_orders_totals(self) -> List[Dict[str, Any]]:
        """Get orders totals"""
        return self._make_request("reports/orders/totals")
    
    def get_products_totals(self) -> List[Dict[str, Any]]:
        """Get products totals"""
        return self._make_request("reports/products/totals")
    
    def get_customers_totals(self) -> List[Dict[str, Any]]:
        """Get customers totals"""
        return self._make_request("reports/customers/totals")
