from flask import Flask, Blueprint, jsonify
from .config import *

# ROUTES

from .routes.api.routes import api



def create_app ():
    
    app = Flask(__name__)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': "Oops! This page doesn't exist."}), 404

    app.register_blueprint(api)
    
    return app