# 🚀 Pentest Recruit - Site Web de Simulation

Un site web complet simulant une plateforme de recrutement de pentesters, développé avec **Python Flask**, **Tailwind CSS** et une architecture en **Blueprints**.

## 🎯 Objectif

Ce projet est une **simulation** destinée à l'entraînement, aux CTF (Capture The Flag) et à l'apprentissage. Il n'est **PAS** un vrai site de recrutement.

## ✨ Fonctionnalités

### 🔐 Authentification
- Système de connexion/déconnexion
- Gestion des sessions Flask
- Protection des routes avec décorateur `@login_required`
- Utilisateurs stockés dans `users.json`

### 🏠 Pages Publiques
- **Accueil** : Présentation de la plateforme avec statistiques
- **À propos** : Informations sur l'entreprise et le pentesting
- **Contact** : Formulaire de contact avec validation

### 📊 Dashboard (Après connexion)
- **Navbar verticale** avec navigation Dashboard/Logout
- **Statistiques personnelles** chargées via AJAX
- **Liste des missions** disponibles avec statuts
- **Profil utilisateur** avec spécialités
- **Actions rapides** pour navigation

### 🎨 Interface
- Design moderne avec **Tailwind CSS**
- **Responsive** (mobile-first)
- **Animations** et transitions fluides
- **Messages flash** pour feedback utilisateur

## 🛠️ Technologies Utilisées

- **Backend** : Python Flask 2.3.3
- **Frontend** : HTML5, JavaScript (ES6+), Tailwind CSS
- **Sessions** : Flask-Session
- **Architecture** : Flask Blueprints
- **Styling** : Tailwind CSS (CDN)

## 📁 Structure du Projet

```
pentest/
├── app.py                 # Point d'entrée Flask
├── requirements.txt       # Dépendances Python
├── users.json            # Base d'utilisateurs de test
├── README.md             # Ce fichier
├── blueprints/           # Modules Flask
│   ├── __init__.py
│   ├── main.py          # Routes publiques (Home, About, Contact)
│   ├── auth.py          # Authentification (Login, Logout)
│   └── dashboard.py     # Dashboard protégé
└── templates/            # Templates HTML
    ├── base.html         # Template de base
    ├── main/             # Pages publiques
    │   ├── home.html
    │   ├── about.html
    │   └── contact.html
    ├── auth/             # Pages d'authentification
    │   └── login.html
    └── dashboard/        # Pages du dashboard
        └── index.html
```

## 🚀 Installation et Lancement

### Prérequis
- Python 3.7+
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner le projet**
   ```bash
   git clone <repository-url>
   cd pentest
   ```

2. **Créer un environnement virtuel (recommandé)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Lancer l'application**
   ```bash
   python app.py
   ```

5. **Accéder au site**
   - Ouvrir votre navigateur
   - Aller sur `http://localhost:5000`

## 🔑 Comptes de Test

Le système inclut plusieurs comptes de démonstration :

| Utilisateur | Mot de passe | Description |
|-------------|--------------|-------------|
| `adminroot` | `supersecret` | Administrateur principal |
| `pentester1` | `password123` | Pentester junior |
| `hacker2024` | `ctf_master` | Expert CTF |
| `security_expert` | `secure_pass` | Expert en sécurité |

## 🔧 Configuration

### Variables d'environnement
- `SECRET_KEY` : Clé secrète Flask (définie dans `app.py`)
- `SESSION_TYPE` : Type de session (fichiers)
- `DEBUG` : Mode debug (activé par défaut)

### Personnalisation
- **Utilisateurs** : Modifier `users.json`
- **Missions** : Éditer la fonction `get_missions()` dans `dashboard.py`
- **Styles** : Personnaliser Tailwind dans `base.html`

## 📱 Fonctionnalités AJAX

Le dashboard utilise AJAX pour :
- Charger les **missions** dynamiquement
- Récupérer le **profil utilisateur**
- Actualiser les **statistiques** en temps réel

## 🎨 Personnalisation du Design

### Couleurs Tailwind
```javascript
tailwind.config = {
    theme: {
        extend: {
            colors: {
                'pentest': {
                    50: '#f0f9ff',
                    500: '#3b82f6',
                    600: '#2563eb',
                    700: '#1d4ed8',
                    900: '#0f172a'
                }
            }
        }
    }
}
```

### Composants réutilisables
- **Cards** avec ombres et hover effects
- **Boutons** avec états hover et focus
- **Formulaires** avec validation et feedback
- **Navigation** responsive

## 🔒 Sécurité

### Fonctionnalités implémentées
- **Protection des routes** avec décorateur `@login_required`
- **Gestion des sessions** sécurisée
- **Validation côté serveur** des formulaires
- **Messages flash** pour feedback utilisateur

### Bonnes pratiques
- Pas de stockage de mots de passe en clair
- Sessions temporaires
- Protection CSRF implicite (Flask)
- Validation des entrées utilisateur

## 🧪 Tests et Développement

### Mode debug
L'application est lancée en mode debug par défaut :
- Rechargement automatique des fichiers
- Messages d'erreur détaillés
- Console de débogage

### Logs
- Erreurs affichées dans la console
- Messages flash pour l'utilisateur
- Validation des formulaires

## 🚨 Limitations et Avertissements

⚠️ **IMPORTANT** : Ce projet est une **SIMULATION** pour :
- **Entraînement** et apprentissage
- **CTF** et challenges de sécurité
- **Démonstration** de concepts Flask

❌ **NE PAS UTILISER** pour :
- Production réelle
- Recrutement effectif
- Stockage de vraies données

## 🤝 Contribution

Ce projet est ouvert aux contributions pour :
- Amélioration de l'interface
- Nouvelles fonctionnalités
- Correction de bugs
- Documentation

## 📄 Licence

Ce projet est fourni à des fins éducatives uniquement.

## 🆘 Support

Pour toute question ou problème :
1. Vérifier la console Flask pour les erreurs
2. Contrôler les logs du navigateur
3. Vérifier la configuration des sessions

---

**Développé avec ❤️ pour l'apprentissage de Flask et de la cybersécurité** 