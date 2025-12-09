from flask import Blueprint, jsonify, request
from flask_security import auth_required, current_user
from models import db, Deck, Card

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
