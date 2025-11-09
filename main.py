from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
from db import db
import os

from routes.clientes import clientes_bp

load_dotenv()

# Configuração da aplicação Flask
app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "http://127.0.0.1:5000"}})
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
db.init_app(app)

with app.app_context():
    db.create_all()
    
# Registro das Blueprints
app.register_blueprint(clientes_bp)

if __name__ == "__main__":
    app.run(debug=True)