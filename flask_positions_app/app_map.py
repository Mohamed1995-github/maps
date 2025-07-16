import os
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_paginate import Pagination, get_page_args

app = Flask(__name__)

# Configuration
DATA_FILE = os.path.join('data', 'places.json')


# Fonctions utilitaires
def load_data():
    """Charge les données depuis le fichier JSON"""
    if not os.path.exists(DATA_FILE):
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)
        return []

    with open(DATA_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_data(data):
    """Sauvegarde les données dans le fichier JSON"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def get_next_id(data):
    """Génère un nouvel ID"""
    return max([item['id'] for item in data] or [0]) + 1


# Routes principales
@app.route('/')
def index():
    # Charger toutes les données
    positions = load_data()

    # Récupérer les paramètres de pagination
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')

    # Filtrer par catégorie si spécifié
    category = request.args.get('category')
    if category:
        filtered_positions = [p for p in positions if p['type'] == category]
    else:
        filtered_positions = positions

    # Pagination
    paginated_positions = filtered_positions[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page, total=len(filtered_positions),
                            css_framework='bootstrap5')

    # Récupérer toutes les catégories uniques
    categories = sorted(set(p['type'] for p in positions))

    return render_template('index.html',
                           positions=paginated_positions,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           categories=categories,
                           current_category=category)


@app.route('/map')
def show_map():
    positions = load_data()
    return render_template('map.html', positions=positions)


# API CRUD
@app.route('/api/positions', methods=['GET'])
def get_positions():
    positions = load_data()
    return jsonify(positions)


@app.route('/api/positions/<int:position_id>', methods=['GET'])
def get_position(position_id):
    positions = load_data()
    position = next((p for p in positions if p['id'] == position_id), None)
    if position:
        return jsonify(position)
    return jsonify({"error": "Position not found"}), 404


@app.route('/api/positions', methods=['POST'])
def create_position():
    data = request.get_json()
    positions = load_data()

    # Validation des données
    required_fields = ['name', 'type', 'lat', 'lng']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    # Création de la nouvelle position
    new_position = {
        "id": get_next_id(positions),
        "name": data['name'],
        "type": data['type'],
        "lat": float(data['lat']),
        "lng": float(data['lng']),
        "quartier": data.get('quartier', ''),
        "created_at": datetime.now().isoformat(),
        "google_place_id": data.get('google_place_id', ''),
        "rating": data.get('rating'),
        "address": data.get('address', '')
    }

    positions.append(new_position)
    save_data(positions)

    return jsonify(new_position), 201


@app.route('/api/positions/<int:position_id>', methods=['PUT'])
def update_position(position_id):
    data = request.get_json()
    positions = load_data()

    position = next((p for p in positions if p['id'] == position_id), None)
    if not position:
        return jsonify({"error": "Position not found"}), 404

    # Mise à jour des champs
    if 'name' in data:
        position['name'] = data['name']
    if 'type' in data:
        position['type'] = data['type']
    if 'lat' in data:
        position['lat'] = float(data['lat'])
    if 'lng' in data:
        position['lng'] = float(data['lng'])
    if 'quartier' in data:
        position['quartier'] = data['quartier']
    if 'commune' in data:
        position['commune'] = data['commune']

    save_data(positions)
    return jsonify(position)


@app.route('/api/positions/<int:position_id>', methods=['DELETE'])
def delete_position(position_id):
    positions = load_data()

    position = next((p for p in positions if p['id'] == position_id), None)
    if not position:
        return jsonify({"error": "Position not found"}), 404

    positions = [p for p in positions if p['id'] != position_id]
    save_data(positions)
    return jsonify({"message": "Position deleted"}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5010)