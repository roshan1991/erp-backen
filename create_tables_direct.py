from app.db.session import engine
from app.db.base import Base

# Import all models to ensure they are registered with Base
from app.models.user import User
from app.models.finance import Account, JournalEntry, JournalEntryLine, APInvoice, ARInvoice, BankStatement
from app.models.supply_chain import Supplier, InventoryProduct, PurchaseOrder, PurchaseOrderItem
from app.models.hr import Department, Employee, Payroll
from app.models.crm import Customer, Lead, Interaction
from app.models.manufacturing import BillOfMaterials, BOMComponent, WorkOrder
from app.models.pos import POSSession, POSOrder, POSOrderItem, Payment
from app.models.woocommerce_settings import WooCommerceSettings
# Also import the ones found in base.py if they are distinct
from app.models.woocommerce_product import WooCommerceProduct
from app.models.product import Product
from app.models.coupon import Coupon
from app.models.loyalty_settings import LoyaltySettings

def create_tables():
    print("Creating all tables in the database...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")

if __name__ == "__main__":
    create_tables()
