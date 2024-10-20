from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(256))
    user_type = db.Column(db.String(20), nullable=False)
    ethereum_address = db.Column(db.String(42), unique=True, nullable=True)
    auth_token = db.Column(db.String(32), unique=True, nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Artwork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    token_id = db.Column(db.String(64), unique=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    artist = db.Column(db.String(100), nullable=False)  # Keep this for backward compatibility
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class Interaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    artwork_id = db.Column(db.Integer, db.ForeignKey('artwork.id'))
    interaction_type = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

class NFTTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artwork_id = db.Column(db.Integer, db.ForeignKey('artwork.id'))
    from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    transaction_hash = db.Column(db.String(66), unique=True)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
