from flask import Blueprint, render_template, session, flash, redirect, url_for, jsonify
from functools import wraps

dashboard_bp = Blueprint('dashboard', __name__)

def login_required(f):
    """Décorateur pour protéger les routes nécessitant une connexion"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Veuillez vous connecter pour accéder à cette page.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@dashboard_bp.route('/dashboard')
@login_required
def index():
    username = session.get('username')
    return render_template('dashboard/index.html', username=username)

@dashboard_bp.route('/api/missions')
@login_required
def get_missions():
    """API pour récupérer les missions (AJAX)"""
    missions = [
        {
            'id': 1,
            'title': 'Test de pénétration Web',
            'description': 'Audit de sécurité d\'une application web e-commerce',
            'difficulty': 'Intermédiaire',
            'reward': '500€',
            'status': 'Disponible'
        },
        {
            'id': 2,
            'title': 'Audit d\'infrastructure',
            'description': 'Test de vulnérabilités sur serveurs et réseaux',
            'difficulty': 'Avancé',
            'reward': '800€',
            'status': 'En cours'
        },
        {
            'id': 3,
            'title': 'Test d\'ingénierie sociale',
            'description': 'Simulation d\'attaques par phishing et manipulation',
            'difficulty': 'Débutant',
            'reward': '300€',
            'status': 'Disponible'
        },
        {
            'id': 4,
            'title': 'Audit de code source',
            'description': 'Analyse statique de sécurité du code',
            'difficulty': 'Expert',
            'reward': '1200€',
            'status': 'Disponible'
        }
    ]
    return jsonify(missions)

@dashboard_bp.route('/api/profile')
@login_required
def get_profile():
    """API pour récupérer le profil utilisateur (AJAX)"""
    username = session.get('username')
    profile = {
        'username': username,
        'level': 'Pentester Senior',
        'missions_completed': 15,
        'success_rate': '94%',
        'specialties': ['Web Security', 'Network Security', 'Social Engineering'],
        'rating': 4.8
    }
    return jsonify(profile) 