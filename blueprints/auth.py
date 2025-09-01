from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import json
import os

auth_bp = Blueprint('auth', __name__)

def load_users():
    """Charge les utilisateurs depuis le fichier JSON"""
    try:
        with open('users.json', 'r') as f:
            data = json.load(f)
            return data.get('users', [])
    except FileNotFoundError:
        return []

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        users = load_users()
        
        # Vérifier les credentials
        for user in users:
            if user['username'] == username and user['password'] == password:
                session['username'] = username
                session['logged_in'] = True
                flash(f'Connexion réussie ! Bienvenue {username}', 'success')
                return redirect(url_for('dashboard.index'))
        
        flash('Nom d\'utilisateur ou mot de passe incorrect.', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Vous avez été déconnecté avec succès.', 'success')
    return redirect(url_for('main.home')) 