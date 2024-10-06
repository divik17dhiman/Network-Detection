from flask import Flask

def create_app():
    app = Flask(__name__)
    from app.reporter import create_routes
    create_routes(app)
    return app
