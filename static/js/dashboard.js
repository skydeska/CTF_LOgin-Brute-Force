/**
 * Dashboard JavaScript - Pentest Recruit
 * Gère les interactions AJAX et l'interface utilisateur
 */

class DashboardManager {
    constructor() {
        this.init();
    }

    init() {
        this.loadProfile();
        this.loadMissions();
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Bouton de rafraîchissement des missions
        const refreshBtn = document.getElementById('refresh-missions');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => this.loadMissions());
        }

        // Boutons de mission
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('mission-detail-btn')) {
                this.showMissionDetails(e.target.dataset.missionId);
            }
            if (e.target.classList.contains('mission-apply-btn')) {
                this.applyToMission(e.target.dataset.missionId);
            }
        });
    }

    async loadProfile() {
        try {
            const response = await fetch('/api/profile');
            if (!response.ok) throw new Error('Erreur réseau');
            
            const data = await response.json();
            this.updateProfileUI(data);
            this.updateStats(data);
        } catch (error) {
            console.error('Erreur lors du chargement du profil:', error);
            this.showError('Erreur lors du chargement du profil');
        }
    }

    async loadMissions() {
        try {
            const response = await fetch('/api/missions');
            if (!response.ok) throw new Error('Erreur réseau');
            
            const data = await response.json();
            this.updateMissionsUI(data);
        } catch (error) {
            console.error('Erreur lors du chargement des missions:', error);
            this.showError('Erreur lors du chargement des missions');
        }
    }

    updateProfileUI(profile) {
        const container = document.getElementById('profile-container');
        if (!container) return;

        container.innerHTML = `
            <div class="space-y-4">
                <div class="text-center">
                    <div class="w-20 h-20 bg-blue-100 rounded-full mx-auto mb-4 flex items-center justify-center">
                        <span class="text-2xl font-bold text-blue-600">${profile.username.charAt(0).toUpperCase()}</span>
                    </div>
                    <h3 class="text-lg font-semibold text-gray-900">${profile.username}</h3>
                    <p class="text-blue-600 font-medium">${profile.level}</p>
                </div>
                
                <div class="border-t pt-4">
                    <div class="flex justify-between items-center mb-2">
                        <span class="text-gray-600">Missions complétées</span>
                        <span class="font-semibold">${profile.missions_completed}</span>
                    </div>
                    <div class="flex justify-between items-center mb-2">
                        <span class="text-gray-600">Taux de succès</span>
                        <span class="font-semibold text-green-600">${profile.success_rate}</span>
                    </div>
                    <div class="flex justify-between items-center mb-2">
                        <span class="text-gray-600">Note moyenne</span>
                        <span class="font-semibold text-yellow-600">${profile.rating}/5</span>
                    </div>
                </div>
                
                <div class="border-t pt-4">
                    <h4 class="font-semibold text-gray-900 mb-2">Spécialités</h4>
                    <div class="flex flex-wrap gap-2">
                        ${profile.specialties.map(specialty => 
                            `<span class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">${specialty}</span>`
                        ).join('')}
                    </div>
                </div>
            </div>
        `;
    }

    updateStats(profile) {
        // Mettre à jour les statistiques dans les cartes
        const missionsCompleted = document.getElementById('missions-completed');
        const successRate = document.getElementById('success-rate');
        const rating = document.getElementById('rating');
        const earnings = document.getElementById('earnings');

        if (missionsCompleted) missionsCompleted.textContent = profile.missions_completed;
        if (successRate) successRate.textContent = profile.success_rate;
        if (rating) rating.textContent = profile.rating;
        if (earnings) earnings.textContent = '€' + (profile.missions_completed * 500);
    }

    updateMissionsUI(missions) {
        const container = document.getElementById('missions-container');
        if (!container) return;

        container.innerHTML = missions.map(mission => `
            <div class="mission-card bg-gray-50 p-6 rounded-lg border border-gray-200" data-mission-id="${mission.id}">
                <div class="flex items-start justify-between">
                    <div class="flex-1">
                        <h3 class="text-lg font-semibold text-gray-900 mb-2">${mission.title}</h3>
                        <p class="text-gray-600 mb-3">${mission.description}</p>
                        <div class="flex items-center space-x-4 text-sm">
                            <span class="bg-blue-100 text-blue-800 px-2 py-1 rounded-full">${mission.difficulty}</span>
                            <span class="text-green-600 font-semibold">${mission.reward}</span>
                        </div>
                    </div>
                    <div class="ml-4">
                        <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                            mission.status === 'Disponible' ? 'bg-green-100 text-green-800' : 
                            mission.status === 'En cours' ? 'bg-yellow-100 text-yellow-800' : 
                            'bg-gray-100 text-gray-800'
                        }">
                            ${mission.status}
                        </span>
                    </div>
                </div>
                <div class="mt-4 flex space-x-3">
                    <button class="mission-detail-btn bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm" 
                            data-mission-id="${mission.id}">
                        Voir détails
                    </button>
                    ${mission.status === 'Disponible' ? 
                        `<button class="mission-apply-btn bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors text-sm" 
                                 data-mission-id="${mission.id}">Postuler</button>` : 
                        ''
                    }
                </div>
            </div>
        `).join('');
    }

    showMissionDetails(missionId) {
        // Simuler l'affichage des détails d'une mission
        alert(`Détails de la mission ${missionId}\n\nCette fonctionnalité peut être étendue pour afficher plus d'informations.`);
    }

    applyToMission(missionId) {
        // Simuler une candidature
        if (confirm(`Voulez-vous vraiment postuler à la mission ${missionId} ?`)) {
            this.showSuccess('Candidature envoyée avec succès !');
            // Ici on pourrait faire un appel AJAX pour enregistrer la candidature
        }
    }

    showSuccess(message) {
        this.showNotification(message, 'success');
    }

    showError(message) {
        this.showNotification(message, 'error');
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 ${
            type === 'success' ? 'bg-green-500 text-white' : 
            type === 'error' ? 'bg-red-500 text-white' : 
            'bg-blue-500 text-white'
        }`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Auto-remove after 3 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 3000);
    }

    async loadSystemInfo() {
        try {
            const response = await fetch('/api/info');
            if (!response.ok) throw new Error('Erreur réseau');
            
            const data = await response.json();
            this.displaySystemInfo(data);
        } catch (error) {
            console.error('Erreur lors du chargement des infos système:', error);
            this.showError('Erreur lors du chargement des infos système');
        }
    }

    displaySystemInfo(info) {
        const container = document.getElementById('system-info');
        if (!container) return;

        container.innerHTML = `
            <div class="bg-white p-4 rounded-lg border border-yellow-300">
                <h4 class="font-semibold text-gray-900 mb-3">Informations Système</h4>
                <div class="space-y-2 text-sm">
                    <div><strong>Entreprise:</strong> ${info.company}</div>
                    <div><strong>Version:</strong> ${info.version}</div>
                    <div><strong>Environnement:</strong> ${info.environment}</div>
                    <div><strong>Statut:</strong> ${info.system_status}</div>
                </div>
                
                <div class="mt-4">
                    <h5 class="font-semibold text-gray-900 mb-2">Endpoints Internes:</h5>
                    <div class="space-y-1">
                        ${info.internal_endpoints.map(endpoint => 
                            `<div class="text-blue-600 font-mono text-xs">${endpoint}</div>`
                        ).join('')}
                    </div>
                </div>

                <div class="mt-4 p-3 bg-red-50 border border-red-200 rounded">
                    <h5 class="font-semibold text-red-800 mb-2">🔒 Informations Admin:</h5>
                    <div class="text-sm text-red-700">
                        <div><strong>Username:</strong> ${info.admin_info.username}</div>
                        <div><strong>Email:</strong> ${info.admin_info.email}</div>
                        <div><strong>Rôle:</strong> ${info.admin_info.role}</div>
                    </div>
                </div>

                <div class="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded">
                    <p class="text-xs text-yellow-700">
                        💡 <strong>Challenge CTF :</strong> Découvrez et accédez au panel admin caché !
                    </p>
                </div>
            </div>
        `;
        
        container.classList.remove('hidden');
        this.showSuccess('Informations système chargées avec succès !');
    }
}

// Initialiser le dashboard quand le DOM est chargé
document.addEventListener('DOMContentLoaded', () => {
    new DashboardManager();
}); 