from app.db.session import SessionLocal
from app.crud import crud_woocommerce_settings
from app.integrations.woocommerce_client import WooCommerceClient

# Get settings from database
db = SessionLocal()
settings = crud_woocommerce_settings.get_settings(db)

if settings:
    print(f"Settings found:")
    print(f"  Store URL: {settings.store_url}")
    print(f"  Consumer Key: {settings.consumer_key[:15]}...")
    print(f"  Consumer Secret: {settings.consumer_secret[:15]}...")
    
    # Create client with database credentials
    client = WooCommerceClient(
        url=settings.store_url,
        consumer_key=settings.consumer_key,
        consumer_secret=settings.consumer_secret
    )
    
    print(f"\nClient initialized:")
    print(f"  URL: {client.url}")
    print(f"  API Base: {client.api_base}")
    print(f"  Consumer Key: {client.consumer_key[:15]}...")
    
    # Try to fetch products
    try:
        print(f"\nFetching products...")
        products = client.get_products(per_page=1)
        print(f"Success! Got {len(products)} product(s)")
        if products:
            print(f"First product: {products[0].get('name', 'N/A')}")
    except Exception as e:
        print(f"Error: {e}")
else:
    print("No settings found in database")

db.close()
