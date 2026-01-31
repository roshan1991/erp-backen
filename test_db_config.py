import os
from app.core.config import settings

print(f"DB_TYPE: {settings.DB_TYPE}")
print(f"URI: {settings.SQLALCHEMY_DATABASE_URI}")

# Test with env var change
os.environ["DB_TYPE"] = "mysql"
# Reload settings (since it's instantiated at module level, this might recall __init__ if I create a new instance, 
# but the 'settings' object is already created. I need to create a new instance of Settings)
from app.core.config import Settings
new_settings = Settings()
print(f"New DB_TYPE: {new_settings.DB_TYPE}")
print(f"New URI: {new_settings.SQLALCHEMY_DATABASE_URI}")
