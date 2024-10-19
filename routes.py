from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from models import User, Artwork, Interaction
from blockchain_simulator import mint_token, transfer_token, get_token_owner, get_artwork_details
from utils import get_engagement_metrics
import logging

main = Blueprint('main', __name__)
logger = logging.getLogger(__name__)

@main.route('/')
def index():
    artworks = Artwork.query.all()
    logging.debug(f"Number of artworks: {len(artworks)}")
    return render_template('index.html', artworks=artworks)

@main.route('/dashboard')
@login_required
def dashboard():
    user_artworks = Artwork.query.filter_by(owner_id=current_user.id).all()
    engagement_metrics = get_engagement_metrics(current_user.id)
    return render_template('dashboard.html', user_artworks=user_artworks, engagement_metrics=engagement_metrics)

@main.route('/artwork/<int:artwork_id>')
def artwork_detail(artwork_id):
    artwork = Artwork.query.get_or_404(artwork_id)
    return render_template('artwork.html', artwork=artwork)

@main.route('/mint', methods=['POST'])
@login_required
def mint_artwork():
    title = request.form.get('title')
    description = request.form.get('description')
    try:
        token_id = mint_token(current_user.id, title, current_user.username, description)
        new_artwork = Artwork(title=title, artist=current_user.username, description=description, token_id=token_id, owner_id=current_user.id)
        db.session.add(new_artwork)
        db.session.commit()
        flash('Artwork minted successfully!', 'success')
    except Exception as e:
        logger.error(f"Error minting artwork: {str(e)}")
        flash('Failed to mint artwork. Please try again.', 'error')
    return redirect(url_for('main.dashboard'))

@main.route('/transfer', methods=['POST'])
@login_required
def transfer_artwork():
    artwork_id = request.form.get('artwork_id')
    recipient_username = request.form.get('recipient')
    artwork = Artwork.query.get_or_404(artwork_id)
    recipient = User.query.filter_by(username=recipient_username).first()
    if recipient and artwork.owner_id == current_user.id:
        try:
            if transfer_token(int(artwork.token_id), current_user.id, recipient.id):
                artwork.owner_id = recipient.id
                db.session.commit()
                flash('Artwork transferred successfully!', 'success')
            else:
                flash('Transfer failed. Please try again.', 'error')
        except Exception as e:
            logger.error(f"Error transferring artwork: {str(e)}")
            flash('Transfer failed. Please try again.', 'error')
    else:
        flash('Transfer failed. Please check the recipient username.', 'error')
    return redirect(url_for('main.dashboard'))

@main.route('/exclusive_content')
@login_required
def exclusive_content():
    if current_user.role == 'vip' or current_user.tokens >= 5:
        return render_template('exclusive_content.html')
    else:
        flash('You need to be a VIP or have at least 5 tokens to access exclusive content.', 'error')
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
    try:
        owner_address = get_token_owner(int(artwork.token_id))
        is_owner = owner_address.lower() == current_user.ethereum_address.lower()
        return render_template('verify_ownership.html', artwork=artwork, is_owner=is_owner)
    except Exception as e:
        logger.error(f"Error verifying ownership: {str(e)}")
        flash('Failed to verify ownership. Please try again.', 'error')
        return redirect(url_for('main.artwork_detail', artwork_id=artwork_id))

@main.route('/artwork_details/<int:artwork_id>')
def artwork_details(artwork_id):
    artwork = Artwork.query.get_or_404(artwork_id)
    try:
        title, artist, description = get_artwork_details(int(artwork.token_id))
        return render_template('artwork_details.html', artwork=artwork, blockchain_title=title, blockchain_artist=artist, blockchain_description=description)
    except Exception as e:
        logger.error(f"Error fetching artwork details: {str(e)}")
        flash('Failed to fetch artwork details from the blockchain. Please try again.', 'error')
        return redirect(url_for('main.artwork_detail', artwork_id=artwork_id))
