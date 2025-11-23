from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics  # <-- IMPORTANTE
from db import db
import os

from routes.clientes import clientes_bp

load_dotenv()

# Configuração da aplicação Flask
app = Flask(__name__)

# Habilitar CORS
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "http://127.0.0.1:5000"}})

# Banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
db.init_app(app)

# Prometheus - cria automaticamente o endpoint /metrics
metrics = PrometheusMetrics(app) 

with app.app_context():
    db.create_all()

# Registro das Blueprints
app.register_blueprint(clientes_bp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
