// LinguaMeet - Intégration vidéo dans la salle de conférence

// Extension de la classe ConferenceRoom pour intégrer la vidéo
(function() {
    // Attendre que ConferenceRoom soit définie
    if (typeof ConferenceRoom !== 'undefined') {
        const originalInit = ConferenceRoom.prototype.init;
        const originalHandleWebSocketMessage = ConferenceRoom.prototype.handleWebSocketMessage;
        const originalHandleParticipantJoined = ConferenceRoom.prototype.handleParticipantJoined;
        const originalLeaveRoom = ConferenceRoom.prototype.leaveRoom;
        const originalSetupEventListeners = ConferenceRoom.prototype.setupEventListeners;

        // Surcharger init pour ajouter le manager vidéo
        ConferenceRoom.prototype.init = async function() {
            // Initialiser le manager vidéo
            this.videoManager = new VideoConferenceManager(this);
            const videoInitialized = await this.videoManager.initialize();
            
            if (videoInitialized) {
                this.audioStream = this.videoManager.getLocalStream();
            } else {
                // Fallback vers audio seul
                const permissionResult = await LinguaMeet.requestMicrophonePermission();
                if (permissionResult.success) {
                    this.audioStream = permissionResult.stream;
                }
            }

            this.setupAudioContext();
            this.setupWebSocket();
            this.setupEventListeners();
            
            LinguaMeet.log('Salle de conférence initialisée avec vidéo');
        };

        // Surcharger setupEventListeners pour ajouter les boutons vidéo et partage d'écran
        ConferenceRoom.prototype.setupEventListeners = function() {
            originalSetupEventListeners.call(this);
            
            // Bouton vidéo
            const videoButton = document.getElementById('video-btn');
            if (videoButton && this.videoManager) {
                videoButton.addEventListener('click', () => {
                    this.videoManager.toggleVideo();
                });
            }
            
            // Bouton partage d'écran
            const screenShareButton = document.getElementById('screen-share-btn');
            if (screenShareButton && this.videoManager) {
                screenShareButton.addEventListener('click', () => {
                    this.videoManager.toggleScreenShare();
                });
            }
        };

        // Surcharger handleWebSocketMessage pour gérer les messages WebRTC
        ConferenceRoom.prototype.handleWebSocketMessage = function(data) {
            originalHandleWebSocketMessage.call(this, data);
            
            try {
                const message = JSON.parse(data);
                
                if (this.videoManager) {
                    switch (message.type) {
                        case 'participants_list':
                            this.videoManager.handleParticipantsList(message.participants || []);
                            break;
                        case 'webrtc_offer':
                            this.videoManager.handleWebRTCOffer(message.from_id, message.offer);
                            break;
                        case 'webrtc_answer':
                            this.videoManager.handleWebRTCAnswer(message.from_id, message.answer);
                            break;
                        case 'webrtc_ice_candidate':
                            this.videoManager.handleWebRTCIceCandidate(message.from_id, message.candidate);
                            break;
                        case 'screen_share_started':
                            if (message.participant_id !== this.participantId) {
                                LinguaMeet.showSystemMessage(
                                    `Un participant partage son écran`,
                                    'info'
                                );
                            }
                            break;
                        case 'screen_share_stopped':
                            if (message.participant_id !== this.participantId) {
                                LinguaMeet.showSystemMessage(
                                    `Le partage d'écran s'est arrêté`,
                                    'info'
                                );
                            }
                            break;
                    }
                }
            } catch (error) {
                // Message déjà parsé dans la méthode originale
            }
        };

        // Surcharger handleParticipantJoined pour la vidéo
        ConferenceRoom.prototype.handleParticipantJoined = function(message) {
            originalHandleParticipantJoined.call(this, message);
            
            // Créer une connexion vidéo avec le nouveau participant
            if (this.videoManager) {
                this.videoManager.handleParticipantJoined(message.participant_id);
            }
        };

        // Surcharger leaveRoom pour nettoyer le manager vidéo
        ConferenceRoom.prototype.leaveRoom = function() {
            if (this.videoManager) {
                this.videoManager.cleanup();
            }
            originalLeaveRoom.call(this);
        };
    }
})();
