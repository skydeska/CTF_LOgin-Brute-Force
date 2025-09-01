import os

class Config:
    """Configuration de base pour l'application Flask"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'pentest_secret_key_2024'
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flask_session')
    
    # Configuration de sécurité
    SESSION_COOKIE_SECURE = False  # Mettre True en production avec HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Configuration de debug
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Configuration des sessions
    PERMANENT_SESSION_LIFETIME = 3600  # 1 heure en secondes

class DevelopmentConfig(Config):
    """Configuration pour le développement"""
    DEBUG = True
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    """Configuration pour la production"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)

class TestingConfig(Config):
    """Configuration pour les tests"""
    TESTING = True
    SESSION_TYPE = 'filesystem'
    WTF_CSRF_ENABLED = False

# Dictionnaire des configurations
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 