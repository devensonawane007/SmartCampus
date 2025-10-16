import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from app.firebase_config import db_ref  # Firebase initialization
from dotenv import load_dotenv

# -------------------- Load environment variables --------------------
basedir = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.abspath(os.path.join(basedir, ".."))
load_dotenv(os.path.join(project_root, ".env"))

# -------------------- Flask app --------------------
app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Change to a secure key
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Enable CSRF for forms
csrf = CSRFProtect(app)

# -------------------- Expose Firebase --------------------
# db_ref will be imported in routes safely
# Do NOT import routes yet

# Import routes at the end to avoid circular imports
from app import routes
