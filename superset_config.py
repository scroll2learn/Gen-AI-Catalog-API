from flask import Flask
from flask_cors import CORS

SESSION_COOKIE_SAMESITE = None
ENABLE_PROXY_FIX = True
PUBLIC_ROLE_LIKE_GAMMA = True
FEATURE_FLAGS = {
    "EMBEDDED_SUPERSET": True
}
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@catalog-db:5432/bighammer_db'

CORS_OPTIONS = {
    'supports_credentials': True,
    'allow_headers': ['*'],
    'resources': ['*'],
    'origins': ['http://localhost:8088', 'http://localhost:5000']
}

def custom_cors(app: Flask):
    CORS(app, **CORS_OPTIONS)
    print("CORS applied with options:", CORS_OPTIONS)

def create_app():
    app = Flask(__name__)
    custom_cors(app)
    return app
