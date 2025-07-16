#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de conversion pour adapter le fichier JSON existant
au format attendu par l'application web Flask.
"""

import json
import os
from datetime import datetime

def convert_nouakchott_data(input_file: str, output_file: str = "places.json"):
    """
    Convertir le fichier JSON de Nouakchott au format standard.
    
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
            # Essayer avec un autre encodage
            with open(input_file, 'r', encoding='latin-1') as f:
                data = json.load(f)
        
        print(f"📊 Données lues: {len(data)} entrées")
        
        # Analyser la structure des données
        if isinstance(data, list) and len(data) > 0:
            sample = data[0]
            print(f"📋 Structure détectée: {list(sample.keys())}")
            
            # Convertir les données
            converted_data = []
            
            for i, item in enumerate(data):
                # Créer un nouvel objet avec la structure attendue
                converted_item = {
                    "id": i + 1,  # ID auto-incrémenté
                    "name": item.get("name", item.get("nom", f"Lieu {i+1}")),
                    "type": item.get("type", "Autre"),
                    "lat": float(item.get("lat", item.get("latitude", 18.0799))),
                    "lng": float(item.get("lng", item.get("longitude", -15.9653))),
                    "quartier": item.get("quartier", item.get("neighborhood", "Non spécifié")),
                    "created_at": datetime.now().isoformat()
                }
                
                # Validation des coordonnées
                if not (-90 <= converted_item["lat"] <= 90):
                    print(f"⚠️  Latitude invalide pour {converted_item['name']}: {converted_item['lat']}")
                    converted_item["lat"] = 18.0799  # Coordonnées par défaut de Nouakchott
                
                if not (-180 <= converted_item["lng"] <= 180):
                    print(f"⚠️  Longitude invalide pour {converted_item['name']}: {converted_item['lng']}")
                    converted_item["lng"] = -15.9653  # Coordonnées par défaut de Nouakchott
                
                converted_data.append(converted_item)
            
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
            print(f"Quartiers: {len(quartiers)}")
            
            return True
            
        else:
            print("❌ Format de données non reconnu")
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
    
    print("🗺️ Convertisseur de données - Application Web")
    print("=" * 50)
    
    # Chercher le fichier existant
    input_file = "allplaces_nouakchott_renamed4.json"
    
    if not os.path.exists(input_file):
        print(f"❌ Fichier {input_file} non trouvé")
        print("Veuillez placer votre fichier JSON dans le même dossier que ce script.")
        return
    
    # Convertir directement
    if convert_nouakchott_data(input_file):
        print(f"\n🎉 Conversion réussie!")
        print(f"Vous pouvez maintenant lancer l'application web avec: python app.py")
        print(f"Puis ouvrir votre navigateur sur: http://localhost:5000")
    else:
        print(f"\n❌ Échec de la conversion")

if __name__ == "__main__":
    main() 