#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de conversion pour adapter les données Google Places
au format attendu par l'application web.
"""

import json
import os
from datetime import datetime

def convert_google_places_data(input_file: str, output_file: str = "places.json"):
    """
    Convertir les données Google Places au format standard.
    
    Args:
        input_file: Chemin vers le fichier JSON source
        output_file: Chemin vers le fichier JSON de sortie
    """
    
    print(f"🔄 Conversion du fichier: {input_file}")
    
    try:
        # Lire le fichier source
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except UnicodeDecodeError:
            with open(input_file, 'r', encoding='latin-1') as f:
                data = json.load(f)
        
        print(f"📊 Structure détectée: {type(data)}")
        
        # Convertir les données
        converted_data = []
        place_id = 1
        
        # Si c'est un dictionnaire avec des types de lieux
        if isinstance(data, dict):
            print(f"📋 Types de lieux trouvés: {list(data.keys())}")
            
            for place_type, places_list in data.items():
                if isinstance(places_list, list):
                    for place in places_list:
                        if isinstance(place, dict) and 'geometry' in place:
                            # Extraire les coordonnées
                            lat = place['geometry']['location']['lat']
                            lng = place['geometry']['location']['lng']
                            
                            # Extraire le nom
                            name = place.get('name', f'Lieu {place_id}')
                            
                            # Extraire le quartier (vicinity)
                            quartier = place.get('vicinity', 'Non spécifié')
                            
                            # Créer l'objet converti
                            converted_item = {
                                "id": place_id,
                                "name": name,
                                "type": place_type.replace('_', ' ').title(),
                                "lat": lat,
                                "lng": lng,
                                "quartier": quartier,
                                "created_at": datetime.now().isoformat(),
                                "google_place_id": place.get('place_id', ''),
                                "rating": place.get('rating', None),
                                "address": place.get('vicinity', '')
                            }
                            
                            converted_data.append(converted_item)
                            place_id += 1
        
        # Si c'est une liste directe
        elif isinstance(data, list):
            print(f"📋 Liste de {len(data)} lieux")
            
            for place in data:
                if isinstance(place, dict):
                    # Essayer différents formats possibles
                    lat = None
                    lng = None
                    
                    # Format Google Places
                    if 'geometry' in place and 'location' in place['geometry']:
                        lat = place['geometry']['location']['lat']
                        lng = place['geometry']['location']['lng']
                    # Format simple avec lat/lng
                    elif 'lat' in place and 'lng' in place:
                        lat = place['lat']
                        lng = place['lng']
                    # Format avec latitude/longitude
                    elif 'latitude' in place and 'longitude' in place:
                        lat = place['latitude']
                        lng = place['longitude']
                    
                    if lat is not None and lng is not None:
                        name = place.get('name', place.get('nom', f'Lieu {place_id}'))
                        place_type = place.get('type', place.get('types', ['Autre'])[0] if isinstance(place.get('types'), list) else 'Autre')
                        quartier = place.get('vicinity', place.get('quartier', place.get('neighborhood', 'Non spécifié')))
                        
                        converted_item = {
                            "id": place_id,
                            "name": name,
                            "type": place_type.replace('_', ' ').title(),
                            "lat": float(lat),
                            "lng": float(lng),
                            "quartier": quartier,
                            "created_at": datetime.now().isoformat()
                        }
                        
                        converted_data.append(converted_item)
                        place_id += 1
        
        if converted_data:
            # Sauvegarder le fichier converti
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(converted_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Conversion terminée!")
            print(f"📁 Fichier sauvegardé: {output_file}")
            print(f"📊 {len(converted_data)} lieux convertis")
            
            # Afficher quelques statistiques
            types = {}
            quartiers = {}
            
            for item in converted_data:
                types[item["type"]] = types.get(item["type"], 0) + 1
                quartiers[item["quartier"]] = quartiers.get(item["quartier"], 0) + 1
            
            print(f"\n📈 Statistiques:")
            print(f"Types de lieux: {len(types)}")
            for type_name, count in sorted(types.items()):
                print(f"  • {type_name}: {count}")
            
            print(f"\nQuartiers: {len(quartiers)}")
            for quartier, count in sorted(quartiers.items())[:10]:  # Afficher les 10 premiers
                print(f"  • {quartier}: {count}")
            
            if len(quartiers) > 10:
                print(f"  ... et {len(quartiers) - 10} autres quartiers")
            
            return True
        else:
            print("❌ Aucun lieu valide trouvé dans les données")
            return False
            
    except FileNotFoundError:
        print(f"❌ Fichier non trouvé: {input_file}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Erreur de décodage JSON: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur lors de la conversion: {e}")
        return False

def main():
    """Fonction principale"""
    
    print("🗺️ Convertisseur Google Places - Application Web")
    print("=" * 50)
    
    # Chercher le fichier existant
    input_file = "allplaces_nouakchott_renamed4.json"
    
    if not os.path.exists(input_file):
        print(f"❌ Fichier {input_file} non trouvé")
        print("Veuillez placer votre fichier JSON dans le même dossier que ce script.")
        return
    
    # Convertir directement
    if convert_google_places_data(input_file):
        print(f"\n🎉 Conversion réussie!")
        print(f"Vous pouvez maintenant lancer l'application web avec: python app.py")
        print(f"Puis ouvrir votre navigateur sur: http://localhost:5000")
        print(f"Les points devraient maintenant être visibles sur la carte!")
    else:
        print(f"\n❌ Échec de la conversion")

if __name__ == "__main__":
    main() 