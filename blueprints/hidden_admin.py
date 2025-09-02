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
    # Nettoyer tous les flash messages du dashboard normal pour éviter la confusion
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
        flash(f'Connexion admin réussie ! Bienvenue {username}', 'success')
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
            
            # Générer le lien de reset (pour le challenge CTF)
            base_url = request.url_root.rstrip('/')
            reset_link = f"{base_url}/_hidden_panel_admin/reset_password"
            
            flash(f'Un lien de réinitialisation a été envoyé à {email}', 'success')
            flash(f'Lien de reset: {reset_link}', 'info')
            flash(f'OTP: XXXX (code à 4 chiffres - valide 20 minutes)', 'warning')
            flash(f'Trouvez le code OTP correct pour réinitialiser le mot de passe !', 'info')
            
            return render_template('hidden_admin/forgot_password.html', 
                                reset_link=reset_link, 
                                otp_generated=True,
                                email=email)
        else:
            flash('Aucun compte associé à cette adresse email.', 'error')
    
    return render_template('hidden_admin/forgot_password.html')

@hidden_admin_bp.route('/_hidden_panel_admin/reset_password', methods=['GET', 'POST'])
def reset_password():
    """Réinitialisation du mot de passe avec OTP - UNIQUEMENT superadmin - SANS RATE LIMITING pour le CTF"""
    if request.method == 'POST':
        email = request.form.get('email')
        otp = request.form.get('otp')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not all([email, otp, new_password, confirm_password]):
            flash('Tous les champs sont requis.', 'error')
            return render_template('hidden_admin/reset_password.html')
        
        # SEUL l'email superadmin est accepté
        if email != 'superadmin@internal.pentest-recruit.fr':
            flash('Email non autorisé.', 'error')
            return render_template('hidden_admin/reset_password.html')
        
        if new_password != confirm_password:
            flash('Les mots de passe ne correspondent pas.', 'error')
            return render_template('hidden_admin/reset_password.html')
        
        # Récupérer l'IP du client pour validation OTP
        client_ip = rate_limiter.get_client_ip(request)
        
        # Vérifier l'OTP - PAS de limitation de tentatives
        is_valid, message = otp_manager.verify_otp(email, otp, client_ip)
        
        if is_valid:
            # OTP valide, mettre à jour le mot de passe pour superadmin uniquement
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
                    flash('Mot de passe superadmin mis à jour avec succès !', 'success')
                    flash('Vous pouvez maintenant vous connecter avec votre nouveau mot de passe.', 'info')
                    return redirect(url_for('hidden_admin.admin_panel'))
                except Exception as e:
                    flash(f'Erreur lors de la sauvegarde: {e}', 'error')
            else:
                flash('Erreur: Utilisateur superadmin non trouvé.', 'error')
        else:
            # OTP invalide - PAS de blocage, juste un message d'erreur
            flash(f'OTP invalide: {message}', 'error')
            flash('Essayez un autre code à 4 chiffres. Temps restant avant expiration.', 'warning')
    
    return render_template('hidden_admin/reset_password.html')

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
            'Félicitations ! Vous avez réussi le challenge CTF !',
            'Techniques utilisées: Énumération API + Brute-force OTP',
            'Vulnérabilités exploitées: Information disclosure + OTP faible',
            'Accès aux systèmes critiques désormais disponible'
        ]
    }
    
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