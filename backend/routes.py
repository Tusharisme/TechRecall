from flask import Blueprint, jsonify, request
from flask_security import auth_required, current_user
from models import db, Deck, Card, ReviewLog

api = Blueprint('api', __name__)

@api.route('/decks', methods=['GET'])
@auth_required()
def get_decks():
    decks = Deck.query.filter_by(user_id=current_user.id).all()
    result = []
    for deck in decks:
        result.append({
            'id': deck.id,
            'title': deck.title,
            'description': deck.description,
            'card_count': len(deck.cards)
        })
    return jsonify(result)

@api.route('/decks', methods=['POST'])
@auth_required()
def create_deck():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400
    
    deck = Deck(title=data['title'], description=data.get('description', ''), author=current_user)
    db.session.add(deck)
    db.session.commit()
    
    return jsonify({
        'id': deck.id,
        'title': deck.title,
        'description': deck.description
    }), 201

@api.route('/decks/<int:deck_id>', methods=['DELETE'])
@auth_required()
def delete_deck(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    if deck.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403
    
    db.session.delete(deck)
    db.session.commit()
    return jsonify({"message": "Deck deleted"}), 200

# --- Card Routes ---

@api.route('/decks/<int:deck_id>/cards', methods=['GET'])
@auth_required()
def get_cards(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    if deck.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403
    
    cards = Card.query.filter_by(deck_id=deck_id).all()
    result = []
    for card in cards:
        result.append({
            'id': card.id,
            'front': card.front,
            'back': card.back,
            'next_review': card.next_review.isoformat(),
            'repetition': card.repetition
        })
    return jsonify(result)

@api.route('/decks/<int:deck_id>/cards', methods=['POST'])
@auth_required()
def create_card(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    if deck.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403
    
    data = request.get_json()
    if not data or 'front' not in data or 'back' not in data:
        return jsonify({"error": "Front and Back are required"}), 400
    
    card = Card(front=data['front'], back=data['back'], deck=deck)
    db.session.add(card)
    db.session.commit()
    return jsonify({'id': card.id, 'front': card.front, 'back': card.back}), 201

# --- SRS Logic ---

from datetime import datetime, timedelta

@api.route('/cards/due', methods=['GET'])
@auth_required()
def get_due_cards():
    # Join Card with Deck to ensure user owns it
    due_cards = Card.query.join(Deck).filter(
        Deck.user_id == current_user.id,
        Card.next_review <= datetime.utcnow()
    ).all()
    
    result = []
    for card in due_cards:
        result.append({
            'id': card.id,
            'front': card.front,
            'back': card.back,
            'deck_title': card.deck.title
        })
    return jsonify(result)

@api.route('/cards/<int:card_id>/review', methods=['POST'])
@auth_required()
def review_card(card_id):
    card = Card.query.join(Deck).filter(Deck.user_id == current_user.id, Card.id == card_id).first_or_404()
    
    data = request.get_json()
    rating = data.get('rating') # 0 to 5
    if rating is None or rating < 0 or rating > 5:
        return jsonify({"error": "Invalid rating"}), 400

    # SuperMemo-2 Algorithm
    if rating >= 3:
        if card.repetition == 0:
            card.interval = 1
        elif card.repetition == 1:
            card.interval = 6
        else:
            card.interval = card.interval * card.ease_factor
        
        card.repetition += 1
        card.ease_factor = card.ease_factor + (0.1 - (5 - rating) * (0.08 + (5 - rating) * 0.02))
        if card.ease_factor < 1.3:
            card.ease_factor = 1.3
    else:
        card.repetition = 0
        card.interval = 0 # Review immediately
    
    from datetime import timedelta
    card.next_review = datetime.utcnow() + timedelta(days=card.interval)
    
    # Log review
    log = ReviewLog(card_id=card.id, rating=rating)
    db.session.add(log)
    db.session.commit()
    
    return jsonify({
        "message": "Review recorded",
        "next_review": card.next_review.isoformat(),
        "interval": card.interval
    })

@api.route('/stats/heatmap', methods=['GET'])
@auth_required()
def get_heatmap_data():
    # Aggregate reviews by date for the current user
    user_deck_ids = [d.id for d in current_user.decks]
    
    if not user_deck_ids:
        return jsonify([])
        
    logs = ReviewLog.query.join(Card).filter(Card.deck_id.in_(user_deck_ids)).all()
    
    from collections import defaultdict
    counts = defaultdict(int)
    
    for log in logs:
        # Date only (YYYY-MM-DD)
        date_str = log.reviewed_at.date().isoformat()
        counts[date_str] += 1
        
    result = [{'date': k, 'count': v} for k, v in counts.items()]
    return jsonify(result)
