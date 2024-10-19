from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from models import User
from app import db, login_manager
import requests
import os

auth = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Please check your login details and try again.')
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.')
            return redirect(url_for('auth.register'))
        
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/sign_auth', methods=['POST'])
def sign_auth():
    sign_token = request.json.get('sign_token')
    
    # Verify the Sign token (implementation to be added)
    # For now, we'll assume the token is valid
    if sign_token:
        # Create a new user if not exists
        user = User.query.filter_by(sign_id=sign_token[:8]).first()
        if not user:
            user = User(username=f"sign_{sign_token[:8]}", sign_id=sign_token[:8])
            db.session.add(user)
            db.session.commit()
        
        login_user(user)
        return {'success': True}
    else:
        return {'success': False, 'error': 'Invalid Sign token'}, 400
