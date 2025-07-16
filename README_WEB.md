# 🗺️ Application Web - Carte des Lieux de Nouakchott

Une application web moderne et interactive pour gérer et visualiser les lieux d'intérêt à Nouakchott, Mauritanie.

## ✨ Fonctionnalités

### 🌍 Carte interactive
- **Carte Leaflet** avec OpenStreetMap
- **Marqueurs cliquables** pour chaque lieu
- **Popups informatifs** avec détails des lieux
- **Cliquez sur la carte** pour ajouter de nouveaux lieux

### 📊 Interface moderne
- **Design responsive** qui s'adapte à tous les écrans
- **Interface intuitive** avec Bootstrap 5
- **Animations fluides** et transitions élégantes
- **Statistiques en temps réel**

### ➕ Gestion complète des lieux
- **Ajouter** de nouveaux lieux via formulaire
- **Modifier** les lieux existants
- **Supprimer** des lieux avec confirmation
- **Validation** automatique des données

### 📱 Fonctionnalités avancées
- **API REST** complète
- **Sauvegarde automatique** en JSON
- **Recherche et filtrage** en temps réel
- **Statistiques détaillées**

## 🚀 Installation et démarrage

### Prérequis
- Python 3.7 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

2. **Convertir vos données existantes** (optionnel)
   ```bash
   python convert_web_data.py
   ```

3. **Lancer l'application**
   ```bash
   python app.py
   ```

4. **Ouvrir votre navigateur**
   ```
   http://localhost:5000
   ```

## 📖 Utilisation

### Interface principale
L'application se compose de plusieurs sections :

1. **📊 Statistiques** : Vue d'ensemble des données
2. **🗺️ Carte** : Affichage interactif des lieux
3. **➕ Formulaire** : Ajout de nouveaux lieux
4. **📋 Liste** : Gestion des lieux existants

### Ajouter un lieu
1. **Cliquez sur la carte** pour définir les coordonnées
2. **Remplissez le formulaire** :
   - Nom du lieu
   - Type (Mosquée, Pharmacie, etc.)
   - Quartier
   - Coordonnées (remplies automatiquement)
3. **Cliquez sur "Ajouter le lieu"**

### Modifier un lieu
1. **Cliquez sur le bouton "Modifier"** dans la liste ou sur la carte
2. **Modifiez les informations** dans le modal
3. **Sauvegardez** les modifications

### Supprimer un lieu
1. **Cliquez sur le bouton "Supprimer"** 
2. **Confirmez** la suppression

## 🔧 API REST

L'application expose une API REST complète :

### Récupérer tous les lieux
```http
GET /api/places
```

### Ajouter un lieu
```http
POST /api/places
Content-Type: application/json

{
  "name": "Nom du lieu",
  "type": "Type de lieu",
  "quartier": "Nom du quartier",
  "lat": 18.0799,
  "lng": -15.9653
}
```

### Modifier un lieu
```http
PUT /api/places/{id}
Content-Type: application/json

{
  "name": "Nouveau nom",
  "type": "Nouveau type",
  "quartier": "Nouveau quartier",
  "lat": 18.0799,
  "lng": -15.9653
}
```

### Supprimer un lieu
```http
DELETE /api/places/{id}
```

## 📁 Structure des données

Le fichier `places.json` contient une liste d'objets avec cette structure :

```json
[
  {
    "id": 1,
    "name": "Nom du lieu",
    "type": "Type de lieu",
    "lat": 18.0799,
    "lng": -15.9653,
    "quartier": "Nom du quartier",
    "created_at": "2024-01-01T12:00:00"
  }
]
```

## 🛠️ Technologies utilisées

- **Backend** : Flask (Python)
- **Frontend** : HTML5, CSS3, JavaScript
- **Carte** : Leaflet.js avec OpenStreetMap
- **UI Framework** : Bootstrap 5
- **Icônes** : Font Awesome
- **Stockage** : JSON

## 🎨 Personnalisation

### Modifier les types de lieux
Éditez le fichier `templates/index.html` et modifiez la liste des options :

```html
<select class="form-select" id="type" required>
    <option value="">Choisir un type</option>
    <option value="Mosquée">Mosquée</option>
    <option value="Pharmacie">Pharmacie</option>
    <!-- Ajoutez vos types ici -->
</select>
```

### Changer le style
Modifiez les styles CSS dans la section `<style>` du fichier HTML.

### Ajouter de nouvelles fonctionnalités
L'API REST permet d'étendre facilement l'application avec de nouvelles fonctionnalités.

## 🐛 Dépannage

### Erreur "Module not found"
```bash
pip install Flask
```

### Port déjà utilisé
Modifiez le port dans `app.py` :
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Carte ne s'affiche pas
- Vérifiez votre connexion internet
- Les tuiles OpenStreetMap nécessitent une connexion

### Données non sauvegardées
- Vérifiez les permissions d'écriture dans le dossier
- Le fichier `places.json` doit être accessible en écriture

## 📱 Compatibilité

- ✅ **Desktop** : Chrome, Firefox, Safari, Edge
- ✅ **Mobile** : Responsive design
- ✅ **Tablette** : Interface adaptée

## 🔒 Sécurité

- Validation des données côté serveur
- Protection contre les injections
- Gestion des erreurs robuste

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer de nouvelles fonctionnalités
- Améliorer l'interface utilisateur
- Optimiser les performances

## 📄 Licence

Ce projet est sous licence MIT.

---

**Développé avec ❤️ pour la communauté de Nouakchott**

### 🚀 Démarrage rapide

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Convertir vos données (si vous en avez)
python convert_web_data.py

# 3. Lancer l'application
python app.py

# 4. Ouvrir http://localhost:5000
``` 