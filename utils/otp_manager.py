import random
import time
from datetime import datetime, timedelta
from collections import defaultdict

class OTPManager:
    def __init__(self):
        # Stockage des OTP par email et par IP
        self.otps = {}  # email -> (otp, timestamp, ip)
        self.otp_attempts = defaultdict(list)  # email -> [(timestamp, ip, success)]
        
        # Configuration
        self.otp_length = 4
        self.otp_validity = 1200  # 20 minutes en secondes
        self.max_otp_attempts = 10  # Max tentatives par email/IP
        
    def generate_otp(self):
        """Génère un OTP à 4 chiffres"""
        return ''.join([str(random.randint(0, 9)) for _ in range(self.otp_length)])
    
    def create_otp(self, email, ip):
        """Crée un nouvel OTP pour un email et une IP"""
        # Supprimer l'ancien OTP s'il existe
        if email in self.otps:
            del self.otps[email]
        
        # Générer un nouvel OTP
        otp = self.generate_otp()
        timestamp = time.time()
        
        # Stocker l'OTP
        self.otps[email] = (otp, timestamp, ip)
        
        return otp
    
    def verify_otp(self, email, otp, ip):
        """Vérifie un OTP"""
        if email not in self.otps:
            return False, "OTP invalide ou expiré"
        
        stored_otp, timestamp, stored_ip = self.otps[email]
        current_time = time.time()
        
        # Vérifier l'expiration
        if current_time - timestamp > self.otp_validity:
            del self.otps[email]
            return False, "OTP expiré"
        
        # Vérifier l'IP (pour le challenge CTF)
        if stored_ip != ip:
            return False, "OTP invalide pour cette IP"
        
        # Vérifier l'OTP
        if stored_otp == otp:
            # OTP valide, le supprimer
            del self.otps[email]
            return True, "OTP valide"
        else:
            return False, "OTP incorrect"
    
    def get_otp_info(self, email):
        """Retourne les informations d'un OTP (pour debug)"""
        if email in self.otps:
            otp, timestamp, ip = self.otps[email]
            remaining_time = max(0, self.otp_validity - (time.time() - timestamp))
            return {
                'otp': otp,
                'timestamp': timestamp,
                'ip': ip,
                'remaining_time': remaining_time,
                'expires_at': datetime.fromtimestamp(timestamp + self.otp_validity).strftime('%H:%M:%S')
            }
        return None
    
    def is_otp_expired(self, email):
        """Vérifie si un OTP est expiré"""
        if email in self.otps:
            _, timestamp, _ = self.otps[email]
            return time.time() - timestamp > self.otp_validity
        return True
    
    def cleanup_expired_otps(self):
        """Nettoie les OTP expirés"""
        current_time = time.time()
        expired_emails = []
        
        for email, (_, timestamp, _) in self.otps.items():
            if current_time - timestamp > self.otp_validity:
                expired_emails.append(email)
        
        for email in expired_emails:
            del self.otps[email]
    
    def get_reset_link(self, email, base_url):
        """Génère un lien de reset pour le challenge CTF"""
        if email in self.otps:
            otp, _, _ = self.otps[email]
            return f"{base_url}/_hidden_panel_admin/forgot_password?token={otp}"
        return None

# Instance globale du gestionnaire OTP
otp_manager = OTPManager() 