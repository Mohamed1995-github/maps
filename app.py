from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)

# Fichier JSON pour stocker les données
DATA_FILE = 'places.json'

def load_places():
    """Charger les lieux depuis le fichier JSON"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_places(places):
    """Sauvegarder les lieux dans le fichier JSON"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(places, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    """Page principale avec la carte"""
    places = load_places()
    return render_template('index.html', places=places)

@app.route('/api/places')
def get_places():
    """API pour récupérer tous les lieux"""
    places = load_places()
    return jsonify(places)

@app.route('/api/places', methods=['POST'])
def add_place():
    """API pour ajouter un nouveau lieu"""
    data = request.json
    
    if not data:
        return jsonify({'error': 'Données JSON manquantes'}), 400
    
    # Validation des données
    required_fields = ['name', 'type', 'lat', 'lng', 'quartier']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'Le champ {field} est obligatoire'}), 400
    
    try:
        lat = float(data['lat'])
        lng = float(data['lng'])
        if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
            return jsonify({'error': 'Coordonnées invalides'}), 400
    except ValueError:
        return jsonify({'error': 'Les coordonnées doivent être des nombres'}), 400
    
    # Charger les lieux existants
    places = load_places()
    
    # Générer un nouvel ID
    new_id = max([place.get('id', 0) for place in places], default=0) + 1
    
    # Créer le nouveau lieu
    new_place = {
        'id': new_id,
        'name': data['name'].strip(),
        'type': data['type'].strip(),
        'quartier': data['quartier'].strip(),
        'lat': lat,
        'lng': lng,
        'created_at': datetime.now().isoformat()
    }
    
    # Ajouter et sauvegarder
    places.append(new_place)
    save_places(places)
    
    return jsonify(new_place), 201

@app.route('/api/places/<int:place_id>', methods=['DELETE'])
def delete_place(place_id):
    """API pour supprimer un lieu"""
    places = load_places()
    
    # Trouver et supprimer le lieu
    for i, place in enumerate(places):
        if place.get('id') == place_id:
            deleted_place = places.pop(i)
            save_places(places)
            return jsonify({'message': 'Lieu supprimé avec succès'})
    
    return jsonify({'error': 'Lieu non trouvé'}), 404

@app.route('/api/places/<int:place_id>', methods=['PUT'])
def update_place(place_id):
    """API pour modifier un lieu"""
    data = request.json
    
    # Debug: afficher les données reçues
    print(f"🔍 Données reçues pour lieu {place_id}: {data}")
    
    if not data:
        return jsonify({'error': 'Données JSON manquantes'}), 400
    
    places = load_places()
    
    # Validation des données
    required_fields = ['name', 'type', 'lat', 'lng', 'quartier']
    for field in required_fields:
        if field not in data or not data[field]:
            print(f"❌ Champ manquant ou vide: {field}")
            return jsonify({'error': f'Le champ {field} est obligatoire'}), 400
    
    try:
        lat = float(data['lat'])
        lng = float(data['lng'])
        if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
            return jsonify({'error': 'Coordonnées invalides'}), 400
    except ValueError:
        return jsonify({'error': 'Les coordonnées doivent être des nombres'}), 400
    
    # Trouver le lieu à modifier
    for place in places:
        if place.get('id') == place_id:
            # Sauvegarder l'ancienne version pour l'historique
            old_data = place.copy()
            
            # Mettre à jour les champs
            place.update({
                'name': data['name'].strip(),
                'type': data['type'].strip(),
                'quartier': data['quartier'].strip(),
                'lat': lat,
                'lng': lng,
                'updated_at': datetime.now().isoformat(),
                'last_modified': datetime.now().isoformat()
            })
            
            # Sauvegarder immédiatement
            save_places(places)
            
            # Log de la modification
            print(f"✅ Lieu modifié: {old_data.get('name')} -> {place['name']}")
            
            return jsonify(place)
    
    return jsonify({'error': 'Lieu non trouvé'}), 404

@app.route('/api/save', methods=['POST'])
def save_data():
    """API pour sauvegarder manuellement les données"""
    try:
        places = load_places()
        save_places(places)
        return jsonify({
            'message': 'Données sauvegardées avec succès',
            'count': len(places),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': f'Erreur lors de la sauvegarde: {str(e)}'}), 500

@app.route('/api/export', methods=['GET'])
def export_data():
    """API pour exporter les données"""
    try:
        places = load_places()
        return jsonify({
            'places': places,
            'export_info': {
                'total_places': len(places),
                'export_date': datetime.now().isoformat(),
                'version': '1.0'
            }
        })
    except Exception as e:
        return jsonify({'error': f'Erreur lors de l\'export: {str(e)}'}), 500

@app.route('/api/backup', methods=['POST'])
def create_backup():
    """API pour créer une sauvegarde"""
    try:
        import shutil
        from datetime import datetime
        
        places = load_places()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'places_backup_{timestamp}.json'
        
        # Créer la sauvegarde
        with open(backup_filename, 'w', encoding='utf-8') as f:
            json.dump(places, f, ensure_ascii=False, indent=2)
        
        return jsonify({
            'message': 'Sauvegarde créée avec succès',
            'backup_file': backup_filename,
            'count': len(places),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': f'Erreur lors de la sauvegarde: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 