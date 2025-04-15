from flask import Flask
from app.config import env
from app.app import create_app

app = create_app()


if __name__ == '__main__':
    if env == 'development':
        app.run(debug=True) 