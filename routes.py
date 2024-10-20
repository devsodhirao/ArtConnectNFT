from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from models import User, Artwork, Interaction, NFTTransaction
from blockchain_simulator import blockchain_simulator
from utils import get_engagement_metrics
import logging

main = Blueprint('main', __name__)
logger = logging.getLogger(__name__)

@main.route('/')
def index():
    artworks = Artwork.query.all()
    return render_template('index.html', artworks=artworks)

@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.user_type == 'admin':
        return admin_dashboard()
    elif current_user.user_type == 'artist':
        return artist_dashboard()
    else:
        return attendee_dashboard()

def admin_dashboard():
    total_users = User.query.count()
    total_artworks = Artwork.query.count()
    total_transactions = NFTTransaction.query.count()
    return render_template('admin_dashboard.html', total_users=total_users, total_artworks=total_artworks, total_transactions=total_transactions)

def artist_dashboard():
    user_artworks = Artwork.query.filter_by(artist_id=current_user.id).all()
    engagement_metrics = get_engagement_metrics(current_user.id)
    return render_template('artist_dashboard.html', user_artworks=user_artworks, engagement_metrics=engagement_metrics)

def attendee_dashboard():
    owned_artworks = Artwork.query.filter_by(owner_id=current_user.id).all()
    return render_template('attendee_dashboard.html', owned_artworks=owned_artworks)

@main.route('/artwork/<int:artwork_id>')
def artwork_detail(artwork_id):
    artwork = Artwork.query.get_or_404(artwork_id)
    return render_template('artwork.html', artwork=artwork)

@main.route('/mint', methods=['POST'])
@login_required
def mint_artwork():
    if current_user.user_type != 'artist':
        flash('Only artists can mint new artworks.', 'error')
        return redirect(url_for('main.dashboard'))

    title = request.form.get('title')
    description = request.form.get('description')
    image_url = request.form.get('image_url')

    new_artwork = Artwork(title=title, description=description, artist_id=current_user.id, owner_id=current_user.id, image_url=image_url)
    db.session.add(new_artwork)
    db.session.commit()
    
    flash('Artwork created successfully! Please use your wallet to mint the NFT.', 'success')
    return redirect(url_for('main.dashboard'))

@main.route('/transfer', methods=['POST'])
@login_required
def transfer_artwork():
    artwork_id = request.form.get('artwork_id')
    recipient_address = request.form.get('recipient_address')
    artwork = Artwork.query.get_or_404(artwork_id)

    if artwork.owner_id != current_user.id:
        flash('You do not own this artwork.', 'error')
        return redirect(url_for('main.dashboard'))

    flash('Please use your wallet to transfer the NFT.', 'info')
    return redirect(url_for('main.dashboard'))

@main.route('/get_contract_abi', methods=['GET'])
def get_contract_abi():
    abi = blockchain_simulator.get_contract_abi()
    return jsonify(abi)

@main.route('/get_contract_address', methods=['GET'])
def get_contract_address():
    address = blockchain_simulator.get_contract_address()
    return address

@main.route('/exclusive_content')
@login_required
def exclusive_content():
    if current_user.user_type == 'artist' or Artwork.query.filter_by(owner_id=current_user.id).first():
        return render_template('exclusive_content.html')
    else:
        flash('You need to own at least one NFT to access exclusive content.', 'error')
        return redirect(url_for('main.index'))

@main.route('/interact', methods=['POST'])
@login_required
def interact():
    artwork_id = request.form.get('artwork_id')
    interaction_type = request.form.get('interaction_type')
    new_interaction = Interaction(user_id=current_user.id, artwork_id=artwork_id, interaction_type=interaction_type)
    db.session.add(new_interaction)
    db.session.commit()
    flash('Interaction recorded!', 'success')
    return redirect(url_for('main.artwork_detail', artwork_id=artwork_id))

@main.route('/verify_ownership/<int:artwork_id>')
@login_required
def verify_ownership(artwork_id):
    artwork = Artwork.query.get_or_404(artwork_id)
    flash('Please use your wallet to verify ownership of this NFT.', 'info')
    return render_template('verify_ownership.html', artwork=artwork)

@main.route('/artwork_details/<int:artwork_id>')
def artwork_details(artwork_id):
    artwork = Artwork.query.get_or_404(artwork_id)
    return render_template('artwork_details.html', artwork=artwork)
