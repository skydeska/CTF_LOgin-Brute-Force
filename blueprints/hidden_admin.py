from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from functools import wraps
from utils.otp_manager import otp_manager
from utils.rate_limiter import rate_limiter  # Gardé pour get_client_ip() seulement
import json

hidden_admin_bp = Blueprint('hidden_admin', __name__)

def load_admin_users():
    """Charge les utilisateurs admin depuis le fichier JSON"""
    try:
        with open('users.json', 'r') as f:
            data = json.load(f)
            return data.get('users', [])
    except FileNotFoundError:
        return []

def find_admin_user(username):
    """Trouve un utilisateur admin par son username"""
    users = load_admin_users()
    for user in users:
        if user['username'] == username:
            return user
    return None

@hidden_admin_bp.route('/_hidden_panel_admin')
def admin_panel():
    """Page principale du panel admin caché - Nettoie les flash messages du dashboard normal"""
    # NE PAS nettoyer les flash messages si on vient du reset password OU de la page de succès
    # Pour permettre l'affichage des messages de succès du reset
    referrer = request.headers.get('Referer', '')
    if 'reset_password' not in referrer and 'password_reset_success' not in referrer:
        # Nettoyer seulement les flash messages du dashboard normal
        session.pop('_flashes', None)
    
    return render_template('hidden_admin/login.html')

@hidden_admin_bp.route('/_hidden_panel_admin/login', methods=['POST'])
def admin_login():
    """Connexion au panel admin - UNIQUEMENT superadmin - SANS RATE LIMITING pour le CTF"""
    username = request.form.get('username')
    password = request.form.get('password')
    
    # PAS de rate limiting pour le hidden panel - permet le brute force CTF
    
    # SEUL superadmin peut se connecter au hidden panel
    if username != 'superadmin':
        flash('Accès refusé.', 'error')
        return redirect(url_for('hidden_admin.admin_panel'))
    
    # Vérifier les credentials pour superadmin uniquement
    user = find_admin_user(username)
    if not user:
        flash('Nom d\'utilisateur ou mot de passe incorrect.', 'error')
        return redirect(url_for('hidden_admin.admin_panel'))
    
    if user['password'] == password:
        # Connexion réussie - Sessions séparées avec préfixe "hidden_"
        session['hidden_admin_username'] = username
        session['hidden_admin_logged_in'] = True
        session['hidden_admin_email'] = user.get('email', '')
        
        # Messages de bienvenue pour superadmin
        flash(f'🎉 Connexion admin réussie ! Bienvenue {username}', 'success')
        flash('🔒 Accès au dashboard administrateur débloqué', 'info')
        
        return redirect(url_for('hidden_admin.admin_dashboard'))
    else:
        # Mot de passe incorrect - PAS de rate limiting
        flash('Mot de passe incorrect.', 'error')
        return redirect(url_for('hidden_admin.admin_panel'))

@hidden_admin_bp.route('/_hidden_panel_admin/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    """Fonctionnalité Forgot Password - UNIQUEMENT superadmin - SANS RATE LIMITING pour le CTF"""
    if request.method == 'POST':
        email = request.form.get('email')
        
        if not email:
            flash('Veuillez saisir une adresse email.', 'error')
            return render_template('hidden_admin/forgot_password.html')
        
        # SEUL l'email superadmin est accepté
        if email != 'superadmin@internal.pentest-recruit.fr':
            flash('Aucun compte associé à cette adresse email.', 'error')
            return render_template('hidden_admin/forgot_password.html')
        
        # Récupérer l'IP du client pour l'OTP (mais pas de rate limiting)
        client_ip = rate_limiter.get_client_ip(request)
        
        # Vérifier si l'email existe dans les utilisateurs
        users = load_admin_users()
        user_exists = any(user.get('email') == email for user in users)
        
        if user_exists:
            # Générer un OTP - PAS de vérification de rate limiting
            otp = otp_manager.create_otp(email, client_ip)
            
            # Stocker l'email en session pour la validation OTP
            session['otp_email'] = email
            
            flash(f'Un code OTP a été envoyé à {email}', 'success')
            flash(f'OTP: XXXX (code à 4 chiffres - valide 20 minutes)', 'warning')
            flash(f'Trouvez le code OTP correct pour accéder à la réinitialisation !', 'info')
            
            # Rediriger vers la page de validation OTP
            return redirect(url_for('hidden_admin.validate_otp'))
        else:
            flash('Aucun compte associé à cette adresse email.', 'error')
    
    return render_template('hidden_admin/forgot_password.html')

@hidden_admin_bp.route('/_hidden_panel_admin/validate_otp', methods=['GET', 'POST'])
def validate_otp():
    """Validation du code OTP - SANS RATE LIMITING pour le CTF"""
    # Vérifier que l'email est en session (vient de forgot_password)
    email = session.get('otp_email')
    if not email:
        flash('Session expirée. Veuillez recommencer le processus.', 'error')
        return redirect(url_for('hidden_admin.forgot_password'))
    
    if request.method == 'POST':
        otp = request.form.get('otp')
        
        if not otp:
            flash('Veuillez saisir le code OTP.', 'error')
            return render_template('hidden_admin/validate_otp.html', email=email)
        
        # Récupérer l'IP du client pour validation OTP
        client_ip = rate_limiter.get_client_ip(request)
        
        # Vérifier l'OTP - PAS de limitation de tentatives - NE PAS CONSOMMER
        is_valid, message = otp_manager.verify_otp(email, otp, client_ip, consume=False)
        
        if is_valid:
            # OTP valide - Créer un cookie temporaire (5 minutes)
            from datetime import datetime, timedelta
            import time
            
            # Token temporaire pour accéder au reset password
            reset_token = f"{email}_{int(time.time())}"
            session['reset_token'] = reset_token
            session['reset_token_expiry'] = time.time() + 300  # 5 minutes
            
            # Nettoyer l'email de session OTP - MAIS NE PAS CONSOMMER L'OTP
            session.pop('otp_email', None)
            # L'OTP reste valide pour d'autres tentatives de brute-force
            
            flash('🎉 Code OTP validé avec succès !', 'success')
            flash('🔓 Vous avez maintenant accès à la réinitialisation du mot de passe.', 'info')
            flash('⏰ Accès valide pendant 5 minutes.', 'warning')
            
            # Rediriger vers la page de reset password
            return redirect(url_for('hidden_admin.reset_password'))
        else:
            # OTP invalide - PAS de blocage, juste un message d'erreur
            flash(f'Code OTP invalide: {message}', 'error')
            flash('Essayez un autre code à 4 chiffres. Temps restant avant expiration.', 'warning')
    
    return render_template('hidden_admin/validate_otp.html', email=email)

@hidden_admin_bp.route('/_hidden_panel_admin/reset_password', methods=['GET', 'POST'])
def reset_password():
    """Réinitialisation du mot de passe - Nécessite un token valide de validation OTP"""
    # Vérifier le token de reset
    reset_token = session.get('reset_token')
    reset_token_expiry = session.get('reset_token_expiry')
    
    if not reset_token or not reset_token_expiry:
        flash('Accès non autorisé. Veuillez valider le code OTP d\'abord.', 'error')
        return redirect(url_for('hidden_admin.forgot_password'))
    
    # Vérifier l'expiration du token (5 minutes)
    import time
    if time.time() > reset_token_expiry:
        # Token expiré
        session.pop('reset_token', None)
        session.pop('reset_token_expiry', None)
        flash('Session expirée (5 minutes). Veuillez recommencer le processus.', 'error')
        return redirect(url_for('hidden_admin.forgot_password'))
    
    # Extraire l'email du token
    email = reset_token.split('_')[0]
    
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not all([new_password, confirm_password]):
            flash('Tous les champs sont requis.', 'error')
            return render_template('hidden_admin/reset_password.html', email=email)
        
        if new_password != confirm_password:
            flash('Les mots de passe ne correspondent pas.', 'error')
            return render_template('hidden_admin/reset_password.html', email=email)
        
        # Mettre à jour le mot de passe pour superadmin uniquement
        users = load_admin_users()
        updated = False
        for user in users:
            if user.get('username') == 'superadmin' and user.get('email') == email:
                user['password'] = new_password
                updated = True
                break
        
        if updated:
            # Sauvegarder les modifications
            try:
                with open('users.json', 'w') as f:
                    json.dump({'users': users}, f, indent=2)
                
                # Nettoyer les tokens de session et consommer l'OTP maintenant
                session.pop('reset_token', None)
                session.pop('reset_token_expiry', None)
                
                # Maintenant on peut consommer l'OTP car le mot de passe a été changé
                otp_manager.consume_otp(email)
                
                # Messages de succès détaillés
                flash('🎉 Félicitations ! Mot de passe superadmin réinitialisé avec succès !', 'success')
                flash('🔑 Votre nouveau mot de passe a été sauvegardé.', 'info')
                flash('🚀 Vous pouvez maintenant vous connecter au panel admin avec vos nouveaux identifiants.', 'info')
                flash('Username: superadmin | Nouveau mot de passe: [celui que vous venez de créer]', 'warning')
                
                # Rediriger vers la page de succès
                return redirect(url_for('hidden_admin.password_reset_success'))
            except Exception as e:
                flash(f'Erreur lors de la sauvegarde: {e}', 'error')
        else:
            flash('Erreur: Utilisateur superadmin non trouvé.', 'error')
    
    # Calculer le temps restant
    remaining_time = int(reset_token_expiry - time.time())
    return render_template('hidden_admin/reset_password.html', email=email, remaining_time=remaining_time)

@hidden_admin_bp.route('/_hidden_panel_admin/password_reset_success')
def password_reset_success():
    """Page de succès après réinitialisation du mot de passe"""
    return render_template('hidden_admin/password_reset_success.html')

@hidden_admin_bp.route('/_hidden_panel_admin/dashboard')
def admin_dashboard():
    """Dashboard admin après connexion réussie - UNIQUEMENT superadmin - Sessions séparées"""
    if not session.get('hidden_admin_logged_in'):
        flash('Veuillez vous connecter pour accéder au dashboard admin.', 'error')
        return redirect(url_for('hidden_admin.admin_panel'))
    
    username = session.get('hidden_admin_username')
    email = session.get('hidden_admin_email')
    
    # Vérifier que c'est bien superadmin
    if username != 'superadmin':
        flash('Accès refusé. Seul superadmin peut accéder à ce dashboard.', 'error')
        return redirect(url_for('hidden_admin.admin_panel'))
    
    # FLAG CTF - Informations sensibles pour superadmin uniquement
    flag_info = {
        'flag': 'CTF{Brut3F0rc3_0TP_4dm1n_P4n3l_2024}',
        'username': username,
        'email': email,
        'role': 'System Administrator',
        'access_level': 'root',
        'challenge_completed': True,
        'internal_notes': [
            '🎆 Félicitations ! Challenge CTF réussi avec succès !',
            '🕵️ Techniques maîtrisées: Énumération + Brute-force OTP',
            '🔓 Vulnérabilités exploitées: Information disclosure + Authentification faible',
            '🚀 Statut: Accès administrateur complet obtenu',
            '🏆 Votre expertise en sécurité a été démontrée !'
        ]
    }
    
    # Ajouter un message de félicitations pour le challenge
    flash('🏆 CHALLENGE CTF TERMINÉ ! Vous avez réussi à accéder au panel administrateur !', 'success')
    flash('🛡️ Consultez le flag CTF ci-dessous pour valider votre réussite.', 'info')
    
    return render_template('hidden_admin/dashboard.html', 
                         username=username, 
                         email=email,
                         flag_info=flag_info)

@hidden_admin_bp.route('/_hidden_panel_admin/logout')
def admin_logout():
    """Déconnexion du panel admin - Sessions séparées"""
    session.pop('hidden_admin_username', None)
    session.pop('hidden_admin_logged_in', None)
    session.pop('hidden_admin_email', None)
    flash('Vous avez été déconnecté du panel admin.', 'success')
    return redirect(url_for('hidden_admin.admin_panel')) 