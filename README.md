# MonProjet - Gestion des Demandes et Mouvements Logistiques

Plateforme Django de gestion des demandes de biens et services, ainsi que des mouvements logistiques qui y sont associés. Conçu pour les entreprises afin de gérer leurs moyens généraux de façon centralisée et efficace.

## 🎯 Fonctionnalités

- **Gestion des Demandes** : Créer, suivre et valider les demandes de biens et services
- **Gestion des Fournisseurs** : Référencer et gérer les fournisseurs partenaires
- **Mouvements Logistiques** : Suivi des entrées/sorties et inventaire
- **Gestion du Catalogue** : Catalogue centralisé des articles disponibles
- **Comptabilité des Commandes** : Traçabilité complète des commandes
- **Comptes Utilisateurs** : Authentification et gestion des rôles

## 📋 Prérequis

- Python 3.10+
- Django 5.1.6
- SQLite (base de données intégrée)

## 🚀 Installation

1. **Cloner le repository**
   ```bash
   git clone <repo-url>
   cd Test
   ```

2. **Créer et activer l'environnement virtuel**
   ```bash
   python -m venv env
   env\Scripts\activate  # Windows
   source env/bin/activate  # Linux/Mac
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Appliquer les migrations**
   ```bash
   cd src
   python manage.py migrate
   ```

5. **Démarrer le serveur de développement**
   ```bash
   python manage.py runserver
   ```

Accédez à l'application sur `http://127.0.0.1:8000/`

## 📁 Structure du Projet

```
src/
├── monprojet/          # Configuration principale Django
├── accounts/           # Gestion des utilisateurs
├── Demande/            # Application de demandes
├── Fournisseur/        # Application fournisseurs
├── Commande/           # Application commandes
├── Inventaire/         # Gestion de l'inventaire
├── Catalogue/          # Catalogue des articles
├── templates/          # Templates HTML
├── static/             # Fichiers statiques (CSS, JS)
├── frontend/           # Frontend (Node.js/assets)
└── manage.py           # Utilitaire Django
```

## 🛠️ Tech Stack

**Backend :**
- Django 5.1.6
- Django Crispy Forms (formulaires)
- Django Select2 (sélection avancée)
- Gunicorn (serveur production)

**Frontend :**
- Bootstrap 5
- HTMX (interactions dynamiques)
- PostCSS
- Alpine js

**Déploiement :**
- WhiteNoise (fichiers statiques)
- Pillow (traitement d'images)

## 📖 Utilisation

### Créer un superutilisateur
```bash
python manage.py createsuperuser
```

### Accéder à l'administration Django
```
http://127.0.0.1:8000/admin/
```

## 🔧 Configuration

Les paramètres principaux se trouvent dans `src/monprojet/settings.py`

## 🤝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AméliorationX`)
3. Commit vos changements (`git commit -m 'Ajout de X'`)
4. Push vers la branche (`git push origin feature/AméliorationX`)
5. Ouvrir une Pull Request

## 📝 Licence

Ce projet est destiné à l'usage interne de l'entreprise NCA Re.

## 📞 Support

Pour toute question ou problème, veuillez contacter l'équipe de développement.

---

**Version actuelle :** Django 5.1.6 | **Dernière mise à jour :** Mai 2026
