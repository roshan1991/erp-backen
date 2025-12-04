from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.integrations.woocommerce_client import WooCommerceClient
from app.crud import crud_woocommerce_settings
from app.api import deps
import requests
from requests.auth import HTTPBasicAuth

router = APIRouter()

@router.get("/test-connection")
def test_woocommerce_connection(db: Session = Depends(deps.get_db)):
    """Test WooCommerce API connection and diagnose issues using database credentials"""
    try:
        # Get credentials from database
        settings = crud_woocommerce_settings.get_settings(db)
        
        if not settings:
            return {
                "success": False,
                "error": "WooCommerce settings not configured in database. Please configure them in the WooCommerce Settings page."
            }
        
        # Test 1: Check if URL is accessible
        base_url = settings.store_url.rstrip('/')
        api_url = f"{base_url}/wp-json/wc/v3"
        
        result = {
            "base_url": base_url,
            "api_url": api_url,
            "credentials_source": "database",
            "tests": []
        }
        
        # Test 2: Try to access WooCommerce API root
        try:
            response = requests.get(f"{base_url}/wp-json/wc/v3", timeout=10)
            result["tests"].append({
                "name": "API Root Access",
                "status": response.status_code,
                "success": response.status_code == 200,
                "message": f"Status: {response.status_code}"
            })
        except Exception as e:
            result["tests"].append({
                "name": "API Root Access",
                "success": False,
                "error": str(e)
            })
        
        # Test 3: Try authenticated request to products endpoint
        try:
            auth = HTTPBasicAuth(
                settings.consumer_key,
                settings.consumer_secret
            )
            response = requests.get(
                f"{api_url}/products",
                auth=auth,
                params={"per_page": 1},
                timeout=10
            )
            result["tests"].append({
                "name": "Authenticated Products Request (HTTP Basic Auth)",
                "status": response.status_code,
                "success": response.status_code == 200,
                "message": f"Status: {response.status_code}",
                "response_preview": response.text[:200] if response.text else None
            })
            
            if response.status_code != 200:
                result["tests"][-1]["full_response"] = response.text
                
        except Exception as e:
            result["tests"].append({
                "name": "Authenticated Products Request (HTTP Basic Auth)",
                "success": False,
                "error": str(e)
            })
        
        # Test 4: Try with query parameters (alternative for some servers)
        try:
            response = requests.get(
                f"{api_url}/products",
                params={
                    "consumer_key": settings.consumer_key,
                    "consumer_secret": settings.consumer_secret,
                    "per_page": 1
                },
                timeout=10
            )
            result["tests"].append({
                "name": "Query Parameter Auth",
                "status": response.status_code,
                "success": response.status_code == 200,
                "message": f"Status: {response.status_code}",
                "response_preview": response.text[:200] if response.text else None
            })
        except Exception as e:
            result["tests"].append({
                "name": "Query Parameter Auth",
                "success": False,
                "error": str(e)
            })
        
        # Test 5: Test using WooCommerceClient (the actual client used by the API)
        try:
            client = WooCommerceClient(
                url=settings.store_url,
                consumer_key=settings.consumer_key,
                consumer_secret=settings.consumer_secret
            )
            products = client.get_products(per_page=1)
            result["tests"].append({
                "name": "WooCommerceClient Test",
                "success": True,
                "message": f"Successfully fetched {len(products)} product(s)",
                "product_count": len(products)
            })
        except Exception as e:
            result["tests"].append({
                "name": "WooCommerceClient Test",
                "success": False,
                "error": str(e)
            })
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

