import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user
from sqlalchemy.orm import DeclarativeBase
import logging
from blockchain_simulator import blockchain_simulator

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

app = Flask(__name__, static_url_path='/static')
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

with app.app_context():
    import models
    db.drop_all()  # Drop all existing tables
    db.create_all()  # Create new tables with updated schema

    # Test Hardhat node connection
    try:
        network_id = blockchain_simulator.get_network_id()
        latest_block = blockchain_simulator.get_latest_block()
        logger.info(f"Connected to Hardhat node. Network ID: {network_id}")
        logger.info(f"Latest block number: {latest_block['number']}")
    except Exception as e:
        logger.error(f"Failed to connect to Hardhat node: {str(e)}")

from routes import main as main_blueprint
app.register_blueprint(main_blueprint)

from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
