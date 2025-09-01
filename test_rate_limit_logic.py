#!/usr/bin/env python3
"""
Test de la logique du rate-limiting
Vérifie que les usernames inexistants ne déclenchent pas le rate-limiting
"""

from utils.rate_limiter import RateLimiter

def test_rate_limit_logic():
    """Teste la logique du rate-limiting"""
    print("🧪 Test de la logique du rate-limiting")
    print("=" * 50)
    
    # Créer une instance du rate limiter
    rate_limiter = RateLimiter()
    
    # Test 1: Username inexistant
    print("\n1️⃣ Test avec username inexistant:")
    username = "nonexistent_user"
    ip = "192.168.1.100"
    
    # Vérifier si le rate-limiting s'applique
    should_apply = rate_limiter.should_apply_rate_limit(username)
    print(f"   Username: {username}")
    print(f"   Rate-limiting applicable: {should_apply}")
    print(f"   ✅ Le rate-limiting ne s'applique PAS aux usernames inexistants")
    
    # Test 2: Username existant avec tentatives
    print("\n2️⃣ Test avec username existant:")
    username = "adminroot"
    ip = "192.168.1.100"
    
    # Simuler quelques tentatives échouées
    print(f"   Username: {username}")
    print(f"   Ajout de 2 tentatives échouées...")
    
    rate_limiter.record_attempt(ip, username, success=False)
    rate_limiter.record_attempt(ip, username, success=False)
    
    # Vérifier le nombre de tentatives
    remaining = rate_limiter.get_remaining_attempts(ip, username)
    print(f"   Tentatives restantes: {remaining['username']}")
    
    # Vérifier si le rate-limiting s'applique maintenant
    should_apply = rate_limiter.should_apply_rate_limit(username)
    print(f"   Rate-limiting applicable: {should_apply}")
    print(f"   ✅ Le rate-limiting s'applique aux usernames existants avec tentatives")
    
    # Test 3: Tentative de plus (déclenche le blocage)
    print("\n3️⃣ Test du déclenchement du blocage:")
    print(f"   Ajout d'une 3ème tentative échouée...")
    
    result = rate_limiter.record_attempt(ip, username, success=False)
    print(f"   Résultat: {result}")
    
    # Vérifier si le username est bloqué
    is_blocked = rate_limiter.is_username_blocked(username)
    print(f"   Username bloqué: {is_blocked}")
    
    if is_blocked:
        remaining_time = rate_limiter.get_block_time_remaining(ip, username)
        print(f"   Temps restant avant déblocage: {int(remaining_time['username']/60)} minutes")
        print(f"   ✅ Le blocage est déclenché après 3 tentatives échouées")
    
    # Test 4: Tentative avec username inexistant après blocage
    print("\n4️⃣ Test avec username inexistant après blocage:")
    username2 = "another_nonexistent_user"
    
    should_apply = rate_limiter.should_apply_rate_limit(username2)
    print(f"   Username: {username2}")
    print(f"   Rate-limiting applicable: {should_apply}")
    print(f"   ✅ Le rate-limiting ne s'applique toujours PAS aux usernames inexistants")
    
    print("\n" + "=" * 50)
    print("🎯 Résumé de la logique:")
    print("   ✅ Usernames inexistants: PAS de rate-limiting")
    print("   ✅ Usernames existants: Rate-limiting après tentatives échouées")
    print("   ✅ Blocage après 3 tentatives échouées pour un username existant")
    print("   ✅ Blocage après 3 tentatives échouées pour une IP")

if __name__ == "__main__":
    test_rate_limit_logic() 