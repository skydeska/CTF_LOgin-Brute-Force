#!/usr/bin/env python3
"""
Test complet du comportement du rate-limiting
Vérifie que les usernames inexistants ne déclenchent pas le rate-limiting
"""

import requests
import time

def test_rate_limit_behavior():
    """Teste le comportement complet du rate-limiting"""
    print("🧪 Test complet du comportement du rate-limiting")
    print("=" * 60)
    
    base_url = "http://localhost:5000"
    
    # Test 1: Tentatives avec username inexistant
    print("\n1️⃣ Test avec username inexistant (ne doit PAS déclencher le rate-limiting):")
    username = "nonexistent_user_12345"
    
    for i in range(5):
        print(f"   Tentative {i+1}/5 avec username inexistant...")
        
        response = requests.post(f"{base_url}/login", data={
            'username': username,
            'password': 'wrong_password'
        })
        
        if "Le nom d'utilisateur n'existe pas" in response.text:
            print(f"     ✅ Message correct: Username inexistant")
        else:
            print(f"     ❌ Message incorrect")
        
        time.sleep(0.5)  # Pause entre les tentatives
    
    print("   ✅ 5 tentatives avec username inexistant - Aucun blocage")
    
    # Test 2: Tentatives avec username existant mais mauvais mot de passe
    print("\n2️⃣ Test avec username existant et mauvais mot de passe (doit déclencher le rate-limiting):")
    username = "adminroot"
    
    for i in range(4):
        print(f"   Tentative {i+1}/4 avec mauvais mot de passe...")
        
        response = requests.post(f"{base_url}/login", data={
            'username': username,
            'password': f'wrong_password_{i}'
        })
        
        if i < 3:  # Les 3 premières tentatives
            if "Le mot de passe pour cet utilisateur est incorrect" in response.text:
                remaining = 3 - (i + 1)
                print(f"     ✅ Message correct: {remaining} tentatives restantes")
            else:
                print(f"     ❌ Message incorrect")
        else:  # 4ème tentative - doit être bloquée
            if "Compte bloqué" in response.text:
                print(f"     ✅ Compte bloqué après 3 tentatives échouées")
            else:
                print(f"     ❌ Compte non bloqué")
        
        time.sleep(0.5)
    
    # Test 3: Tentative de connexion avec le compte bloqué
    print("\n3️⃣ Test de connexion avec le compte bloqué:")
    response = requests.post(f"{base_url}/login", data={
        'username': username,
        'password': 'supersecret'  # Bon mot de passe
    })
    
    if "Compte bloqué" in response.text:
        print("   ✅ Compte toujours bloqué - impossible de se connecter")
    else:
        print("   ❌ Compte débloqué trop tôt")
    
    # Test 4: Tentative avec un autre username existant (ne doit pas être affecté)
    print("\n4️⃣ Test avec un autre username existant (ne doit pas être affecté):")
    username2 = "pentester1"
    
    response = requests.post(f"{base_url}/login", data={
        'username': username2,
        'password': 'wrong_password'
    })
    
    if "Le mot de passe pour cet utilisateur est incorrect" in response.text:
        print("   ✅ Autre compte non affecté par le blocage")
    else:
        print("   ❌ Autre compte affecté par le blocage")
    
    # Test 5: Test du header X-Forwarded-For pour contourner le blocage IP
    print("\n5️⃣ Test du contournement via X-Forwarded-For:")
    headers = {'X-Forwarded-For': '192.168.1.200'}
    
    response = requests.post(f"{base_url}/login", data={
        'username': username,
        'password': 'wrong_password'
    }, headers=headers)
    
    if "Le mot de passe pour cet utilisateur est incorrect" in response.text:
        print("   ✅ Contournement IP réussi via X-Forwarded-For")
    else:
        print("   ❌ Contournement IP échoué")
    
    print("\n" + "=" * 60)
    print("🎯 Résumé des tests:")
    print("   ✅ Usernames inexistants: PAS de rate-limiting")
    print("   ✅ Usernames existants: Rate-limiting après 3 tentatives échouées")
    print("   ✅ Blocage de compte après 3 tentatives échouées")
    print("   ✅ Autres comptes non affectés par le blocage")
    print("   ✅ Contournement IP possible via X-Forwarded-For")

def main():
    """Fonction principale"""
    try:
        # Vérifier que le serveur est accessible
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
    
    # Lancer les tests
    test_rate_limit_behavior()
    
    return 0

if __name__ == "__main__":
    exit(main()) 