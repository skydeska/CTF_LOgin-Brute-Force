from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from functools import wraps
from utils.otp_manager import otp_manager
from utils.rate_limiter import rate_limiter
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
    """Page principale du panel admin caché"""
    return render_template('hidden_admin/login.html')

@hidden_admin_bp.route('/_hidden_panel_admin/login', methods=['POST'])
def admin_login():
    """Connexion au panel admin"""
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Récupérer l'IP du client
    client_ip = rate_limiter.get_client_ip(request)
    
    # Vérifier si l'IP est bloquée
    if rate_limiter.is_ip_blocked(client_ip):
        remaining_time = rate_limiter.get_block_time_remaining(client_ip, username)
        flash(f'IP bloquée pour {int(remaining_time["ip"]/60)} minutes. Utilisez X-Forwarded-For pour contourner.', 'error')
        return redirect(url_for('hidden_admin.admin_panel'))
    
    # Vérifier les credentials
    user = find_admin_user(username)
    if not user:
        rate_limiter.record_attempt(client_ip, username, success=False)
        flash('Nom d\'utilisateur ou mot de passe incorrect.', 'error')
        return redirect(url_for('hidden_admin.admin_panel'))
    
    if user['password'] == password:
        # Connexion réussie
        rate_limiter.record_attempt(client_ip, username, success=True)
        session['admin_username'] = username
        session['admin_logged_in'] = True
        session['admin_email'] = user.get('email', '')
        flash(f'Connexion admin réussie ! Bienvenue {username}', 'success')
        return redirect(url_for('hidden_admin.admin_dashboard'))
    else:
        # Mot de passe incorrect
        result = rate_limiter.record_attempt(client_ip, username, success=False)
        remaining = rate_limiter.get_remaining_attempts(client_ip, username)
        
        if result == "ip_blocked":
            flash(f'IP bloquée pour 10 minutes. Utilisez X-Forwarded-For pour contourner.', 'error')
        elif result == "username_blocked":
            flash(f'Compte bloqué pour 10 minutes.', 'error')
        else:
            flash(f'Mot de passe incorrect. {remaining["username"]} tentatives restantes.', 'error')
        
        return redirect(url_for('hidden_admin.admin_panel'))

@hidden_admin_bp.route('/_hidden_panel_admin/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    """Fonctionnalité Forgot Password"""
    if request.method == 'POST':
        email = request.form.get('email')
        
        if not email:
            flash('Veuillez saisir une adresse email.', 'error')
            return render_template('hidden_admin/forgot_password.html')
        
        # Récupérer l'IP du client
        client_ip = rate_limiter.get_client_ip(request)
        
        # Vérifier si l'email existe dans les utilisateurs
        users = load_admin_users()
        user_exists = any(user.get('email') == email for user in users)
        
        if user_exists:
            # Générer un OTP
            otp = otp_manager.create_otp(email, client_ip)
            
            # Générer le lien de reset (pour le challenge CTF)
            base_url = request.url_root.rstrip('/')
            reset_link = otp_manager.get_reset_link(email, base_url)
            
            flash(f'Un lien de réinitialisation a été envoyé à {email}', 'success')
            flash(f'Lien de reset: {reset_link}', 'info')
            flash(f'OTP: {otp} (valide 20 minutes)', 'info')
            
            return render_template('hidden_admin/forgot_password.html', 
                                reset_link=reset_link, 
                                otp=otp,
                                email=email)
        else:
            flash('Aucun compte associé à cette adresse email.', 'error')
    
    return render_template('hidden_admin/forgot_password.html')

@hidden_admin_bp.route('/_hidden_panel_admin/reset_password', methods=['GET', 'POST'])
def reset_password():
    """Réinitialisation du mot de passe avec OTP"""
    if request.method == 'POST':
        email = request.form.get('email')
        otp = request.form.get('otp')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not all([email, otp, new_password, confirm_password]):
            flash('Tous les champs sont requis.', 'error')
            return render_template('hidden_admin/reset_password.html')
        
        if new_password != confirm_password:
            flash('Les mots de passe ne correspondent pas.', 'error')
            return render_template('hidden_admin/reset_password.html')
        
        # Récupérer l'IP du client
        client_ip = rate_limiter.get_client_ip(request)
        
        # Vérifier l'OTP
        is_valid, message = otp_manager.verify_otp(email, otp, client_ip)
        
        if is_valid:
            # OTP valide, mettre à jour le mot de passe
            users = load_admin_users()
            for user in users:
                if user.get('email') == email:
                    user['password'] = new_password
                    break
            
            # Sauvegarder les modifications
            try:
                with open('users.json', 'w') as f:
                    json.dump({'users': users}, f, indent=2)
                flash('Mot de passe mis à jour avec succès !', 'success')
                return redirect(url_for('hidden_admin.admin_panel'))
            except Exception as e:
                flash(f'Erreur lors de la sauvegarde: {e}', 'error')
        else:
            flash(f'OTP invalide: {message}', 'error')
    
    return render_template('hidden_admin/reset_password.html')

@hidden_admin_bp.route('/_hidden_panel_admin/dashboard')
def admin_dashboard():
    """Dashboard admin après connexion réussie"""
    if not session.get('admin_logged_in'):
        flash('Veuillez vous connecter pour accéder au dashboard admin.', 'error')
        return redirect(url_for('hidden_admin.admin_panel'))
    
    username = session.get('admin_username')
    email = session.get('admin_email')
    
    # FLAG CTF - Informations sensibles
    flag_info = {
        'flag': 'CTF{Brut3F0rc3_0TP_4dm1n_P4n3l_2024}',
        'username': username,
        'email': email,
        'role': 'Administrator',
        'access_level': 'root',
        'internal_notes': [
            'Système de gestion des utilisateurs',
            'Configuration des serveurs de production',
            'Accès aux bases de données critiques',
            'Logs de sécurité et monitoring'
        ]
    }
    
    return render_template('hidden_admin/dashboard.html', 
                         username=username, 
                         email=email,
                         flag_info=flag_info)

@hidden_admin_bp.route('/_hidden_panel_admin/logout')
def admin_logout():
    """Déconnexion du panel admin"""
    session.pop('admin_username', None)
    session.pop('admin_logged_in', None)
    session.pop('admin_email', None)
    flash('Vous avez été déconnecté du panel admin.', 'success')
    return redirect(url_for('hidden_admin.admin_panel')) 