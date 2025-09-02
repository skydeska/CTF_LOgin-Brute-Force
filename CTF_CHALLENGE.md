# 🏆 Challenge CTF - Pentest Recruit

## 🎯 Objectif du Challenge

Accéder au **panel d'administration caché** de l'application Pentest Recruit en utilisant des techniques de **pentesting web** avancées.

## 🚀 Étapes du Challenge

### 1️⃣ **Énumération et Découverte**
- Connectez-vous au site principal avec un compte valide
- Utilisez le dashboard pour énumérer les endpoints internes
- Découvrez l'existence de `/_hidden_panel_admin`

### 2️⃣ **Accès au Panel Caché**
- Accédez à `/_hidden_panel_admin`
- **SEUL superadmin** peut utiliser ce panel
- Utilisez la fonctionnalité "Mot de passe oublié"
- Saisissez l'email: `superadmin@internal.pentest-recruit.fr`

### 3️⃣ **Brute-force OTP**
- L'application génère un **OTP à 4 chiffres** (affiché comme XXXX)
- L'OTP est valide **20 minutes** et lié à votre IP
- **AUCUN RATE-LIMITING** sur le hidden panel - brute-force libre
- **Brute-forcez** tous les codes 0000-9999 pour trouver le bon
- **Créez un nouveau mot de passe** superadmin une fois l'OTP trouvé

### 4️⃣ **Accès au Dashboard Admin**
- Connectez-vous avec superadmin + votre nouveau mot de passe
- Accédez au dashboard administrateur superadmin
- **Récupérez le flag CTF** !
- **Note**: Seul superadmin peut accéder au hidden panel

## 🔑 Comptes de Test

| Utilisateur | Mot de passe | Email |
|-------------|--------------|-------|
| `devroot` | `sup3rs3cr3tm3g4c0det0cr4ckf0ry0ubr0th34` | `admin@pentest-recruit.fr` |
| `pentester1` | `password123` | `pentester1@pentest-recruit.fr` |
| `hacker2024` | `ctf_master` | `hacker@ctf-master.com` |
| `security_expert` | `secure_pass` | `expert@security-consulting.fr` |
| **`superadmin`** | `admin_default_2024` | **`superadmin@internal.pentest-recruit.fr`** |

## 🛡️ Mécanismes de Sécurité

### **Rate-Limiting (Dashboard Normal Seulement)**
- **3 tentatives** de mauvais mot de passe par username **existant**
- **3 tentatives** de mauvais mot de passe par IP
- **Blocage de 10 minutes** après dépassement
- **Usernames inexistants** : Aucun rate-limiting (pas de blocage)
- **HIDDEN PANEL** : **AUCUN RATE-LIMITING** pour permettre le brute-force CTF

### **Contournement via X-Forwarded-For (Dashboard Seulement)**
- L'application fait **confiance** au header `X-Forwarded-For`
- Permet de **contourner** le blocage IP
- **Challenge CTF** : manipulation d'en-têtes HTTP
- **HIDDEN PANEL** : Pas de rate-limiting donc pas besoin de contournement

### **Système OTP Sécurisé**
- **OTP unique** par utilisateur et IP
- **Expiration** de 20 minutes
- **Liaison IP** pour empêcher le partage
- **AUCUNE LIMITATION** sur les tentatives OTP (vulnérabilité CTF)

## 🔍 Points d'Entrée

### **Routes Publiques**
- `/` - Page d'accueil
- `/about` - À propos
- `/contact` - Contact
- `/login` - Connexion principale

### **Routes Protégées (après connexion)**
- `/dashboard` - Dashboard utilisateur
- `/api/missions` - Liste des missions
- `/api/profile` - Profil utilisateur
- `/api/info` - **Énumération des endpoints** ⭐

### **Routes Cachées (challenge)**
- `/_hidden_panel_admin` - **Panel admin caché** ⭐
- `/_hidden_panel_admin/forgot_password` - Mot de passe oublié
- `/_hidden_panel_admin/reset_password` - Réinitialisation
- `/_hidden_panel_admin/dashboard` - **Dashboard admin avec flag** 🏆

## 💡 Techniques Requises

### **Énumération**
- Découverte d'endpoints cachés
- Utilisation des APIs internes
- Analyse des réponses JSON
- Identification de l'email admin dans `/api/info`

### **Brute-Force**
- Attaque sur code à 4 chiffres (0000-9999)
- Gestion des sessions utilisateur
- Respect des limites de temps (20 min)
- **AUCUNE LIMITATION** de tentatives sur le hidden panel

### **Gestion des Sessions**
- **Sessions séparées** entre dashboard normal et hidden admin
- Utilisation de l'email révélé dans `/api/info`
- Pas de manipulation d'en-têtes nécessaire pour le hidden panel

## 🎮 Scénario de Jeu

### **Phase 1 : Reconnaissance**
1. Connectez-vous avec un compte valide
2. Explorez le dashboard utilisateur
3. Utilisez l'énumération pour découvrir les endpoints

### **Phase 2 : Découverte**
1. Identifiez l'existence du panel admin caché
2. Accédez à la page de connexion admin
3. Utilisez la fonctionnalité "Mot de passe oublié"

### **Phase 3 : Exploitation**
1. Recevez un OTP à 4 chiffres
2. Brute-forcez le code OTP
3. Réinitialisez le mot de passe admin

### **Phase 4 : Accès Final**
1. Connectez-vous au panel admin
2. Accédez au dashboard administrateur
3. **Récupérez le flag CTF !**

## 🏁 Flag CTF

Le flag est affiché dans le dashboard administrateur après connexion réussie :

```
CTF{Brut3F0rc3_0TP_4dm1n_P4n3l_2024}
```

## 🔧 Outils Recommandés

### **Navigateur Web**
- **Burp Suite** pour l'interception et manipulation
- **OWASP ZAP** pour l'analyse de sécurité
- **FoxyProxy** pour la gestion des en-têtes

### **Scripts de Brute-Force**
- **Python** avec `requests` et `itertools`
- **Bash** avec `curl` et boucles
- **Burp Suite Intruder** pour l'automatisation

## ⚠️ Notes Importantes

### **Simulation CTF**
- **Aucun vrai email** n'est envoyé
- **OTP affiché** pour le challenge
- **Données simulées** pour l'entraînement

### **Sécurité**
- **Vulnérabilités intentionnelles** pour le CTF
- **Ne pas reproduire** en production
- **Apprentissage et entraînement** uniquement

### **Déroulement**
- **Chaque utilisateur** a un OTP unique
- **Sessions séparées** pour chaque compte
- **Gestion des IP** pour le rate-limiting

## 🎓 Compétences Testées

- ✅ **Énumération** d'endpoints web
- ✅ **Brute-force** de codes d'authentification
- ✅ **Manipulation** d'en-têtes HTTP
- ✅ **Gestion** des sessions utilisateur
- ✅ **Contournement** des protections de sécurité
- ✅ **Analyse** des réponses d'API

## 🚀 Démarrage Rapide

1. **Lancez l'application** : `python app.py`
2. **Accédez au site** : `http://localhost:5000`
3. **Connectez-vous** avec un compte de test
4. **Commencez l'énumération** dans le dashboard
5. **Découvrez le panel caché** et lancez l'attaque !

## 🧪 Tests et Validation

### **Test de la Logique du Rate-Limiting**
```bash
# Test de la logique du rate-limiting
python test_rate_limit_logic.py

# Test complet du comportement
python test_rate_limit_complete.py
```

### **Test des Fonctionnalités CTF**
```bash
# Test des fonctionnalités CTF
python test_ctf_features.py

# Démonstration du brute-force OTP
python ctf_otp_bruteforce.py
```

---

**Bonne chance et amusez-vous bien ! 🎯🏆** 