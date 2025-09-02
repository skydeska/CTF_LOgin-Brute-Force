import time
from collections import defaultdict
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self):
        # Stockage des tentatives par IP seulement
        self.ip_attempts = defaultdict(list)
        self.blocked_ips = {}  # IP -> timestamp de blocage
        
        # Configuration
        self.max_attempts = 3
        self.block_duration = 600  # 10 minutes en secondes
        
    def get_client_ip(self, request):
        """Récupère l'IP du client en tenant compte de X-Forwarded-For"""
        # Pour le challenge CTF, on fait confiance à X-Forwarded-For
        forwarded_for = request.headers.get('X-Forwarded-For')
        if forwarded_for:
            # Prendre la première IP de la chaîne
            return forwarded_for.split(',')[0].strip()
        
        # Fallback sur l'IP réelle
        return request.remote_addr
    
    def is_ip_blocked(self, ip):
        """Vérifie si une IP est bloquée"""
        if ip in self.blocked_ips:
            block_time = self.blocked_ips[ip]
            if time.time() - block_time < self.block_duration:
                return True
            else:
                # Débloquer si le temps est écoulé
                del self.blocked_ips[ip]
        return False
    

    def record_attempt(self, ip, username, success=False):
        """Enregistre une tentative de connexion (rate-limiting par IP uniquement)"""
        current_time = time.time()
        
        # Enregistrer la tentative pour l'IP seulement
        self.ip_attempts[ip].append((current_time, success))
        # Garder seulement les 10 dernières tentatives
        self.ip_attempts[ip] = self.ip_attempts[ip][-10:]
        
        # Vérifier si on doit bloquer l'IP (uniquement pour les tentatives échouées)
        if not success:
            # Bloquer l'IP si trop de tentatives échouées
            failed_attempts = [t for t in self.ip_attempts[ip] if not t[1]]
            if len(failed_attempts) >= self.max_attempts:
                self.blocked_ips[ip] = current_time
                return "ip_blocked"
        
        return "success"
    
    def get_remaining_attempts(self, ip):
        """Retourne le nombre de tentatives restantes pour l'IP"""
        failed_ip = len([t for t in self.ip_attempts[ip] if not t[1]])
        return max(0, self.max_attempts - failed_ip)
    
    def get_block_time_remaining(self, ip):
        """Retourne le temps restant avant déblocage de l'IP"""
        current_time = time.time()
        
        if ip in self.blocked_ips:
            block_time = self.blocked_ips[ip]
            return max(0, self.block_duration - (current_time - block_time))
        
        return 0
    
    def cleanup_old_attempts(self):
        """Nettoie les anciennes tentatives"""
        current_time = time.time()
        cutoff_time = current_time - 3600  # 1 heure
        
        # Nettoyer les tentatives IP
        for ip in list(self.ip_attempts.keys()):
            self.ip_attempts[ip] = [t for t in self.ip_attempts[ip] if t[0] > cutoff_time]
            if not self.ip_attempts[ip]:
                del self.ip_attempts[ip]

# Instance globale du rate limiter
rate_limiter = RateLimiter() 