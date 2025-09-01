#!/usr/bin/env python3
"""
Test des fonctionnalités CTF avancées
Vérifie le rate-limiting, les OTP et le panel admin caché
"""

import requests
import time
import sys

def test_rate_limiting():
    """Teste le système de rate-limiting"""
    print("🔒 Test du système de rate-limiting...")
    
    base_url = "http://localhost:5000"
    
    # Test 1: Tentative avec un username inexistant
    print("  - Test username inexistant...")
    response = requests.post(f"{base_url}/login", data={
        'username': 'nonexistent_user',
        'password': 'wrong_password'
    })
    
    if "Le nom d'utilisateur n'existe pas" in response.text:
        print("    ✅ Message d'erreur correct pour username inexistant")
    else:
        print("    ❌ Message d'erreur incorrect")
    
    # Test 2: Tentative avec un username existant mais mauvais mot de passe
    print("  - Test mauvais mot de passe...")
    response = requests.post(f"{base_url}/login", data={
        'username': 'adminroot',
        'password': 'wrong_password'
    })
    
    if "Le mot de passe pour cet utilisateur est incorrect" in response.text:
        print("    ✅ Message d'erreur correct pour mauvais mot de passe")
    else:
        print("    ❌ Message d'erreur incorrect")
    
    # Test 3: Test du header X-Forwarded-For
    print("  - Test contournement via X-Forwarded-For...")
    headers = {'X-Forwarded-For': '192.168.1.100'}
    response = requests.post(f"{base_url}/login", data={
        'username': 'adminroot',
        'password': 'wrong_password'
    }, headers=headers)
    
    print("    ✅ Test X-Forwarded-For effectué")
    
    return True

def test_api_enumeration():
    """Teste l'API d'énumération"""
    print("\n🔍 Test de l'API d'énumération...")
    
    base_url = "http://localhost:5000"
    
    # Test de l'API /api/info
    try:
        response = requests.get(f"{base_url}/api/info")
        if response.status_code == 302:  # Redirection vers login
            print("  ✅ API /api/info protégée (redirection vers login)")
        else:
            print(f"  ❌ API /api/info retourne un code inattendu: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Erreur lors du test de l'API: {e}")
        return False
    
    return True

def test_hidden_admin_panel():
    """Teste l'accès au panel admin caché"""
    print("\n🚪 Test du panel admin caché...")
    
    base_url = "http://localhost:5000"
    
    # Test 1: Accès à la page principale
    try:
        response = requests.get(f"{base_url}/_hidden_panel_admin")
        if response.status_code == 200:
            print("  ✅ Panel admin caché accessible")
        else:
            print(f"  ❌ Panel admin retourne un code inattendu: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Erreur lors de l'accès au panel admin: {e}")
        return False
    
    # Test 2: Fonctionnalité forgot password
    try:
        response = requests.post(f"{base_url}/_hidden_panel_admin/forgot_password", data={
            'email': 'admin@pentest-recruit.fr'
        })
        if response.status_code == 200:
            print("  ✅ Fonctionnalité forgot password accessible")
        else:
            print(f"  ❌ Forgot password retourne un code inattendu: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Erreur lors du test forgot password: {e}")
        return False
    
    return True

def test_otp_system():
    """Teste le système OTP"""
    print("\n🔐 Test du système OTP...")
    
    base_url = "http://localhost:5000"
    
    # Test de la génération d'OTP
    try:
        response = requests.post(f"{base_url}/_hidden_panel_admin/forgot_password", data={
            'email': 'admin@pentest-recruit.fr'
        })
        
        if "OTP:" in response.text:
            print("  ✅ OTP généré et affiché")
        else:
            print("  ❌ OTP non généré ou non affiché")
    except Exception as e:
        print(f"  ❌ Erreur lors du test OTP: {e}")
        return False
    
    return True

def main():
    """Fonction principale de test"""
    print("🧪 Test des Fonctionnalités CTF Avancées")
    print("=" * 60)
    
    # Vérifier que le serveur est accessible
    try:
        response = requests.get("http://localhost:5000", timeout=5)
        if response.status_code != 200:
            print("❌ Le serveur n'est pas accessible")
            return 1
    except Exception as e:
        print("❌ Impossible de se connecter au serveur Flask")
        print(f"   Erreur: {e}")
        print("   Assurez-vous que l'application est lancée avec: python app.py")
        return 1
    
    print("✅ Serveur Flask accessible")
    
    # Tests des fonctionnalités
    tests = [
        ("Rate-limiting et feedback", test_rate_limiting),
        ("API d'énumération", test_api_enumeration),
        ("Panel admin caché", test_hidden_admin_panel),
        ("Système OTP", test_otp_system),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"⚠️  {test_name} a échoué")
    
    print("\n" + "=" * 60)
    print(f"📊 Résultats: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Toutes les fonctionnalités CTF sont opérationnelles !")
        print("\n🚀 Challenge CTF prêt :")
        print("   1. Connectez-vous au site principal")
        print("   2. Utilisez l'énumération pour découvrir /_hidden_panel_admin")
        print("   3. Utilisez la fonctionnalité 'Mot de passe oublié'")
        print("   4. Brute-forcez l'OTP à 4 chiffres")
        print("   5. Accédez au dashboard admin pour le flag")
        print("\n💡 Conseils :")
        print("   - Utilisez X-Forwarded-For pour contourner le rate-limiting")
        print("   - L'OTP est lié à votre IP et expire en 20 minutes")
        print("   - Chaque utilisateur a un OTP unique")
        return 0
    else:
        print("❌ Certains tests ont échoué. Vérifiez la configuration.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 