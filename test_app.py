#!/usr/bin/env python3
"""
Script de test rapide pour Pentest Recruit
Vérifie que l'application Flask se lance correctement
"""

import sys
import os

def test_imports():
    """Teste l'import des modules principaux"""
    try:
        from app import create_app
        print("✅ Import de l'application Flask réussi")
        return True
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False

def test_config():
    """Teste la configuration Flask"""
    try:
        from config import config
        print("✅ Configuration Flask chargée")
        return True
    except ImportError as e:
        print(f"❌ Erreur de configuration: {e}")
        return False

def test_blueprints():
    """Teste l'import des blueprints"""
    try:
        from blueprints.main import main_bp
        from blueprints.auth import auth_bp
        from blueprints.dashboard import dashboard_bp
        print("✅ Tous les blueprints importés")
        return True
    except ImportError as e:
        print(f"❌ Erreur des blueprints: {e}")
        return False

def test_app_creation():
    """Teste la création de l'application Flask"""
    try:
        from app import create_app
        app = create_app()
        print("✅ Application Flask créée avec succès")
        return True
    except Exception as e:
        print(f"❌ Erreur de création de l'app: {e}")
        return False

def test_files_exist():
    """Vérifie l'existence des fichiers essentiels"""
    required_files = [
        'app.py',
        'config.py',
        'requirements.txt',
        'users.json',
        'README.md'
    ]
    
    required_dirs = [
        'blueprints',
        'templates',
        'static'
    ]
    
    all_good = True
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} existe")
        else:
            print(f"❌ {file} manquant")
            all_good = False
    
    for dir in required_dirs:
        if os.path.exists(dir):
            print(f"✅ Dossier {dir}/ existe")
        else:
            print(f"❌ Dossier {dir}/ manquant")
            all_good = False
    
    return all_good

def main():
    """Fonction principale de test"""
    print("🧪 Test de l'application Pentest Recruit")
    print("=" * 50)
    
    tests = [
        ("Vérification des fichiers", test_files_exist),
        ("Test des imports", test_imports),
        ("Test de la configuration", test_config),
        ("Test des blueprints", test_blueprints),
        ("Test de création de l'app", test_app_creation),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"⚠️  {test_name} a échoué")
    
    print("\n" + "=" * 50)
    print(f"📊 Résultats: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont passés ! L'application est prête.")
        print("\n🚀 Pour lancer l'application:")
        print("   python app.py")
        print("   ou")
        print("   start.bat (Windows)")
        print("   ./start.sh (Linux/Mac)")
        return 0
    else:
        print("❌ Certains tests ont échoué. Vérifiez la configuration.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 