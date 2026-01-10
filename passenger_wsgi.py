import os
import sys

# Add the app directory to the sys.path
sys.path.insert(0, os.path.dirname(__file__))

# Import the FastAPI app
# 'app.main' refers to the module 'app/main.py'
# 'app' refers to the FastAPI instance created in 'app/main.py'
from app.main import app as application
