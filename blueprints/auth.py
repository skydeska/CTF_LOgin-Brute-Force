from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
import json
import os
from utils.rate_limiter import rate_limiter
from utils.otp_manager import otp_manager

auth_bp = Blueprint('auth', __name__)

def load_users():
    """Charge les utilisateurs depuis le fichier JSON"""
    try:
        with open('users.json', 'r') as f:
            data = json.load(f)
            return data.get('users', [])
    except FileNotFoundError:
        return []

def find_user(username):
    """Trouve un utilisateur par son username"""
    users = load_users()
    for user in users:
        if user['username'] == username:
            return user
    return None

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Récupérer l'IP du client
        client_ip = rate_limiter.get_client_ip(request)
        
        # Vérifier si l'IP est bloquée (SEULE contrainte de rate-limiting)
        if rate_limiter.is_ip_blocked(client_ip):
            remaining_time = rate_limiter.get_block_time_remaining(client_ip)
            flash(f'Réessayer dans {int(remaining_time/60)} minutes.', 'error')
            return render_template('auth/login.html')
        
        # Vérifier si l'utilisateur existe
        user = find_user(username)
        if not user:
            # Username n'existe pas - PAS de rate-limiting ici
            flash('Le nom d\'utilisateur n\'existe pas.', 'error')
            return render_template('auth/login.html')
        
        # RESTRICTION: superadmin ne peut PAS se connecter au login principal
        if username == 'superadmin':
            flash('Compte non autorisé sur cette interface.', 'error')
            return render_template('auth/login.html')
        
        # Vérifier le mot de passe
        if user['password'] == password:
            # Connexion réussie
            rate_limiter.record_attempt(client_ip, username, success=True)
            session['username'] = username
            session['logged_in'] = True
            session['user_email'] = user.get('email', '')
            flash(f'Connexion réussie ! Bienvenue {username}', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            # Mot de passe incorrect - SEUL l'IP peut être bloquée
            result = rate_limiter.record_attempt(client_ip, username, success=False)
            remaining = rate_limiter.get_remaining_attempts(client_ip)
            
            if result == "ip_blocked":
                flash(f'Trop de tentatives. reessayer dans 10 minutes.', 'error')
            else:
                flash(f'Le mot de passe pour cet utilisateur est incorrect.', 'error')
            
            return render_template('auth/login.html')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Vous avez été déconnecté avec succès.', 'success')
    return redirect(url_for('main.home')) 