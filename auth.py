from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from models import User
from app import db, login_manager
import secrets
from siwe import SiweMessage, generate_nonce
from web3 import Web3
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
        if user and user.user_type == 'admin' and check_password_hash(user.password_hash, password):
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
        user_type = request.form.get('user_type')
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.')
            return redirect(url_for('auth.register'))
        
        new_user = User(username=username, email=email, user_type=user_type)
        if user_type == 'admin':
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

@auth.route('/wallet_login', methods=['POST'])
def wallet_login():
    message = request.json.get('message')
    signature = request.json.get('signature')
    
    try:
        siwe = SiweMessage(message)
        is_valid = siwe.verify(signature)
        
        if is_valid:
            user = User.query.filter_by(ethereum_address=siwe.address).first()
            if not user:
                user = User(username=siwe.address[:10], ethereum_address=siwe.address, user_type='attendee')
                db.session.add(user)
                db.session.commit()
            
            login_user(user)
            return jsonify({'success': True, 'message': 'Logged in successfully'})
        else:
            return jsonify({'success': False, 'message': 'Invalid signature'}), 401
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@auth.route('/get_nonce', methods=['GET'])
def get_nonce():
    return jsonify({'nonce': generate_nonce()})

@auth.route('/verify_token', methods=['POST'])
def verify_token():
    token = request.json.get('token')
    user = User.query.filter_by(auth_token=token).first()
    if user:
        login_user(user)
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Invalid token'}), 401
