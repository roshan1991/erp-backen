import os
from urllib.parse import quote_plus
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "ERP System"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 # 8 days
    
    # Database
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "erp_db")
    SQLALCHEMY_DATABASE_URI: str | None = None
    
    # Daraz API
    DARAZ_APP_KEY: str = os.getenv("DARAZ_APP_KEY", "")
    DARAZ_APP_SECRET: str = os.getenv("DARAZ_APP_SECRET", "")
    DARAZ_API_URL: str = os.getenv("DARAZ_API_URL", "https://api.daraz.pk/rest")
    
    # Facebook/Instagram API
    FACEBOOK_APP_ID: str = os.getenv("FACEBOOK_APP_ID", "")
    FACEBOOK_APP_SECRET: str = os.getenv("FACEBOOK_APP_SECRET", "")
    FACEBOOK_PAGE_ACCESS_TOKEN: str = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN", "")
    FACEBOOK_PAGE_ID: str = os.getenv("FACEBOOK_PAGE_ID", "")
    INSTAGRAM_ACCOUNT_ID: str = os.getenv("INSTAGRAM_ACCOUNT_ID", "")
    
    # WhatsApp Business API
    WHATSAPP_PHONE_NUMBER_ID: str = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
    WHATSAPP_BUSINESS_ACCOUNT_ID: str = os.getenv("WHATSAPP_BUSINESS_ACCOUNT_ID", "")
    WHATSAPP_ACCESS_TOKEN: str = os.getenv("WHATSAPP_ACCESS_TOKEN", "")
    
    # Webhook Configuration
    WEBHOOK_VERIFY_TOKEN: str = os.getenv("WEBHOOK_VERIFY_TOKEN", "my_verify_token")
    WEBHOOK_BASE_URL: str = os.getenv("WEBHOOK_BASE_URL", "http://localhost:8000")
    
    # WooCommerce API
    WOOCOMMERCE_URL: str = os.getenv("WOOCOMMERCE_URL", "")
    WOOCOMMERCE_CONSUMER_KEY: str = os.getenv("WOOCOMMERCE_CONSUMER_KEY", "")
    WOOCOMMERCE_CONSUMER_SECRET: str = os.getenv("WOOCOMMERCE_CONSUMER_SECRET", "")


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.SQLALCHEMY_DATABASE_URI:
            encoded_user = quote_plus(self.POSTGRES_USER)
            encoded_password = quote_plus(self.POSTGRES_PASSWORD)
            self.SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{encoded_user}:{encoded_password}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
