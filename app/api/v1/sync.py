from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.models.product import Product
from app.integrations.woocommerce_client import WooCommerceClient
from app.crud import crud_woocommerce_settings

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

@router.post("/woocommerce-to-inventory")
def sync_woocommerce_to_inventory(
    db: Session = Depends(deps.get_db),
    client: WooCommerceClient = Depends(get_woocommerce_client),
    current_user = Depends(deps.get_current_active_user)
):
    """Sync WooCommerce products to local inventory database"""
    try:
        # Fetch all products from WooCommerce (paginated)
        all_products = []
        page = 1
        per_page = 100
        
        while True:
            products = client.get_products(page=page, per_page=per_page)
            if not products:
                break
            all_products.extend(products)
            if len(products) < per_page:
                break
            page += 1
        
        synced_count = 0
        updated_count = 0
        skipped_count = 0
        
        for woo_product in all_products:
            try:
                # Skip products without essential data
                if not woo_product.get('name'):
                    skipped_count += 1
                    continue
                
                # Check if product already exists by SKU or name
                existing_product = None
                if woo_product.get('sku'):
                    existing_product = db.query(Product).filter(Product.barcode == woo_product['sku']).first()
                
                if not existing_product:
                    existing_product = db.query(Product).filter(Product.name == woo_product['name']).first()
                
                # Prepare product data
                # Generate a unique barcode if SKU is missing
                barcode = woo_product.get('sku')
                if not barcode:
                    # Generate random barcode: REON-{product_id}-{random_4_digits}
                    import random
                    barcode = f"REON-{woo_product['id']}-{random.randint(1000, 9999)}"
                
                product_data = {
                    'name': woo_product['name'],
                    'category': woo_product.get('categories', [{}])[0].get('name', 'Uncategorized') if woo_product.get('categories') else 'Uncategorized',
                    'price': float(woo_product.get('price') or woo_product.get('regular_price') or 0),
                    'stock': woo_product.get('stock_quantity') or 0,
                    'barcode': barcode,
                    'image': woo_product.get('images', [{}])[0].get('src', '') if woo_product.get('images') else '',
                    'status': 'In Stock' if woo_product.get('stock_status') == 'instock' else 'Out of Stock'
                }
                
                if existing_product:
                    # Update existing product
                    for key, value in product_data.items():
                        setattr(existing_product, key, value)
                    updated_count += 1
                else:
                    # Create new product
                    new_product = Product(**product_data)
                    db.add(new_product)
                    synced_count += 1
                
            except Exception as e:
                print(f"Error syncing product {woo_product.get('name', 'Unknown')}: {e}")
                skipped_count += 1
                continue
        
        db.commit()
        
        return {
            "success": True,
            "message": f"Sync completed successfully",
            "total_woocommerce_products": len(all_products),
            "synced": synced_count,
            "updated": updated_count,
            "skipped": skipped_count
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Sync failed: {str(e)}")
