// LinguaMeet - Gestion vidéo WebRTC

class VideoConferenceManager {
    constructor(conferenceRoom) {
        this.conferenceRoom = conferenceRoom;
        this.peerConnections = new Map();
        this.localStream = null;
        this.screenStream = null;
        this.isVideoActive = true;
        this.isScreenSharing = false;
        this.originalVideoTrack = null;
        
        this.iceServers = {
            iceServers: [
                { urls: 'stun:stun.l.google.com:19302' },
                { urls: 'stun:stun1.l.google.com:19302' }
            ]
        };
    }

    async initialize() {
        try {
            // Obtenir les permissions média (audio + vidéo)
            const permissionResult = await LinguaMeet.requestMediaPermissions(true, true);
            if (!permissionResult.success) {
                LinguaMeet.showSystemMessage(
                    `Erreur permissions média: ${permissionResult.error}`,
                    'warning'
                );
                // Fallback: essayer juste l'audio
                const audioOnly = await LinguaMeet.requestMicrophonePermission();
                if (audioOnly.success) {
                    this.localStream = audioOnly.stream;
                    this.isVideoActive = false;
                }
                return false;
            }

            this.localStream = permissionResult.stream;
            this.displayLocalVideo();
            LinguaMeet.log('Flux vidéo local initialisé');
            return true;
        } catch (error) {
            LinguaMeet.log(`Erreur initialisation vidéo: ${error.message}`, 'error');
            return false;
        }
    }

    displayLocalVideo() {
        const localVideoElement = document.getElementById(`video-${this.conferenceRoom.participantId}`);
        if (localVideoElement && this.localStream) {
            localVideoElement.srcObject = this.localStream;
            localVideoElement.muted = true; // Éviter l'écho
            LinguaMeet.log('Vidéo locale affichée');
        }
    }

    toggleVideo() {
        this.isVideoActive = !this.isVideoActive;
        
        // Activer/désactiver les pistes vidéo
        if (this.localStream) {
            this.localStream.getVideoTracks().forEach(track => {
                track.enabled = this.isVideoActive;
            });
        }
        
        const videoButton = document.getElementById('video-btn');
        
        if (this.isVideoActive) {
            videoButton.className = 'btn btn-lg btn-success';
            videoButton.innerHTML = '<i class="fas fa-video me-2"></i>Caméra ACTIVE';
            LinguaMeet.showSystemMessage('Caméra activée', 'success');
        } else {
            videoButton.className = 'btn btn-lg btn-danger';
            videoButton.innerHTML = '<i class="fas fa-video-slash me-2"></i>Caméra INACTIVE';
            LinguaMeet.showSystemMessage('Caméra désactivée', 'warning');
        }

        // Envoyer l'état au serveur
        this.conferenceRoom.sendMessage({
            type: 'video_toggle',
            active: this.isVideoActive
        });
    }

    async handleParticipantsList(participants) {
        // Créer une connexion WebRTC avec chaque participant existant
        for (const participant of participants) {
            await this.createPeerConnection(participant.id);
        }
    }

    async handleParticipantJoined(participantId) {
        // Créer une connexion avec le nouveau participant
        await this.createPeerConnection(participantId);
    }

    async createPeerConnection(participantId) {
        if (this.peerConnections.has(participantId)) {
            return this.peerConnections.get(participantId);
        }

        const peerConnection = new RTCPeerConnection(this.iceServers);
        this.peerConnections.set(participantId, peerConnection);

        // Ajouter les pistes locales à la connexion
        if (this.localStream) {
            this.localStream.getTracks().forEach(track => {
                peerConnection.addTrack(track, this.localStream);
            });
        }

        // Gérer les pistes distantes
        peerConnection.ontrack = (event) => {
            LinguaMeet.log(`Piste reçue de ${participantId}`);
            const remoteVideoElement = document.getElementById(`video-${participantId}`);
            if (remoteVideoElement && event.streams[0]) {
                remoteVideoElement.srcObject = event.streams[0];
            }
        };

        // Gérer les candidats ICE
        peerConnection.onicecandidate = (event) => {
            if (event.candidate) {
                this.conferenceRoom.sendMessage({
                    type: 'webrtc_ice_candidate',
                    target_id: participantId,
                    candidate: event.candidate
                });
            }
        };

        // Gérer l'état de la connexion
        peerConnection.onconnectionstatechange = () => {
            LinguaMeet.log(`État connexion avec ${participantId}: ${peerConnection.connectionState}`);
        };

        // Créer et envoyer une offre
        try {
            const offer = await peerConnection.createOffer({
                offerToReceiveAudio: true,
                offerToReceiveVideo: true
            });
            await peerConnection.setLocalDescription(offer);
            
            this.conferenceRoom.sendMessage({
                type: 'webrtc_offer',
                target_id: participantId,
                offer: offer
            });
        } catch (error) {
            LinguaMeet.log(`Erreur création offre pour ${participantId}: ${error}`, 'error');
        }

        return peerConnection;
    }

    async handleWebRTCOffer(fromId, offer) {
        LinguaMeet.log(`Offre WebRTC reçue de ${fromId}`);
        
        let peerConnection = this.peerConnections.get(fromId);
        if (!peerConnection) {
            peerConnection = new RTCPeerConnection(this.iceServers);
            this.peerConnections.set(fromId, peerConnection);

            // Ajouter les pistes locales
            if (this.localStream) {
                this.localStream.getTracks().forEach(track => {
                    peerConnection.addTrack(track, this.localStream);
                });
            }

            // Gérer les pistes distantes
            peerConnection.ontrack = (event) => {
                const remoteVideoElement = document.getElementById(`video-${fromId}`);
                if (remoteVideoElement && event.streams[0]) {
                    remoteVideoElement.srcObject = event.streams[0];
                }
            };

            // Gérer les candidats ICE
            peerConnection.onicecandidate = (event) => {
                if (event.candidate) {
                    this.conferenceRoom.sendMessage({
                        type: 'webrtc_ice_candidate',
                        target_id: fromId,
                        candidate: event.candidate
                    });
                }
            };
        }

        try {
            await peerConnection.setRemoteDescription(new RTCSessionDescription(offer));
            const answer = await peerConnection.createAnswer();
            await peerConnection.setLocalDescription(answer);

            this.conferenceRoom.sendMessage({
                type: 'webrtc_answer',
                target_id: fromId,
                answer: answer
            });
        } catch (error) {
            LinguaMeet.log(`Erreur traitement offre de ${fromId}: ${error}`, 'error');
        }
    }

    async handleWebRTCAnswer(fromId, answer) {
        LinguaMeet.log(`Réponse WebRTC reçue de ${fromId}`);
        const peerConnection = this.peerConnections.get(fromId);
        
        if (peerConnection) {
            try {
                await peerConnection.setRemoteDescription(new RTCSessionDescription(answer));
            } catch (error) {
                LinguaMeet.log(`Erreur traitement réponse de ${fromId}: ${error}`, 'error');
            }
        }
    }

    async handleWebRTCIceCandidate(fromId, candidate) {
        const peerConnection = this.peerConnections.get(fromId);
        
        if (peerConnection) {
            try {
                await peerConnection.addIceCandidate(new RTCIceCandidate(candidate));
            } catch (error) {
                LinguaMeet.log(`Erreur ajout candidat ICE de ${fromId}: ${error}`, 'error');
            }
        }
    }

    handleParticipantLeft(participantId) {
        const peerConnection = this.peerConnections.get(participantId);
        if (peerConnection) {
            peerConnection.close();
            this.peerConnections.delete(participantId);
            LinguaMeet.log(`Connexion fermée avec ${participantId}`);
        }
    }

    async toggleScreenShare() {
        if (this.isScreenSharing) {
            await this.stopScreenShare();
        } else {
            await this.startScreenShare();
        }
    }

    async startScreenShare() {
        try {
            // Demander le partage d'écran
            const screenStream = await navigator.mediaDevices.getDisplayMedia({
                video: {
                    cursor: "always"
                },
                audio: false
            });

            this.screenStream = screenStream;
            this.isScreenSharing = true;

            // Sauvegarder la piste vidéo originale
            const videoTrack = this.localStream.getVideoTracks()[0];
            if (videoTrack) {
                this.originalVideoTrack = videoTrack;
            }

            // Remplacer la piste vidéo par l'écran partagé
            const screenTrack = screenStream.getVideoTracks()[0];
            
            // Mettre à jour le flux local
            if (this.localStream) {
                // Retirer l'ancienne piste vidéo
                if (this.originalVideoTrack) {
                    this.localStream.removeTrack(this.originalVideoTrack);
                    this.originalVideoTrack.enabled = false;
                }
                // Ajouter la nouvelle piste d'écran
                this.localStream.addTrack(screenTrack);
            }

            // Mettre à jour toutes les connexions peer
            this.peerConnections.forEach((peerConnection, participantId) => {
                const sender = peerConnection.getSenders().find(s => s.track && s.track.kind === 'video');
                if (sender) {
                    sender.replaceTrack(screenTrack);
                }
            });

            // Afficher l'écran partagé localement
            const localVideoElement = document.getElementById(`video-${this.conferenceRoom.participantId}`);
            if (localVideoElement) {
                localVideoElement.srcObject = screenStream;
            }

            // Mettre à jour le bouton
            const screenShareButton = document.getElementById('screen-share-btn');
            if (screenShareButton) {
                screenShareButton.className = 'btn btn-lg btn-danger';
                screenShareButton.innerHTML = '<i class="fas fa-stop-circle me-2"></i>Arrêter le partage';
            }

            LinguaMeet.showSystemMessage('Partage d\'écran activé', 'success');

            // Gérer l'arrêt du partage par l'utilisateur
            screenTrack.onended = () => {
                this.stopScreenShare();
            };

            // Notifier les autres participants
            this.conferenceRoom.sendMessage({
                type: 'screen_share_started',
                participant_id: this.conferenceRoom.participantId
            });

        } catch (error) {
            LinguaMeet.log(`Erreur partage d'écran: ${error.message}`, 'error');
            LinguaMeet.showSystemMessage('Impossible de partager l\'écran', 'error');
            this.isScreenSharing = false;
        }
    }

    async stopScreenShare() {
        try {
            // Arrêter le flux d'écran
            if (this.screenStream) {
                this.screenStream.getTracks().forEach(track => track.stop());
                this.screenStream = null;
            }

            this.isScreenSharing = false;

            // Restaurer la piste vidéo originale
            if (this.originalVideoTrack && this.localStream) {
                const screenTrack = this.localStream.getVideoTracks()[0];
                if (screenTrack) {
                    this.localStream.removeTrack(screenTrack);
                }
                
                this.originalVideoTrack.enabled = this.isVideoActive;
                this.localStream.addTrack(this.originalVideoTrack);

                // Mettre à jour toutes les connexions peer
                this.peerConnections.forEach((peerConnection, participantId) => {
                    const sender = peerConnection.getSenders().find(s => s.track && s.track.kind === 'video');
                    if (sender) {
                        sender.replaceTrack(this.originalVideoTrack);
                    }
                });

                // Restaurer l'affichage local
                const localVideoElement = document.getElementById(`video-${this.conferenceRoom.participantId}`);
                if (localVideoElement) {
                    localVideoElement.srcObject = this.localStream;
                }
            }

            // Mettre à jour le bouton
            const screenShareButton = document.getElementById('screen-share-btn');
            if (screenShareButton) {
                screenShareButton.className = 'btn btn-lg btn-info';
                screenShareButton.innerHTML = '<i class="fas fa-desktop me-2"></i>Partager l\'écran';
            }

            LinguaMeet.showSystemMessage('Partage d\'écran arrêté', 'info');

            // Notifier les autres participants
            this.conferenceRoom.sendMessage({
                type: 'screen_share_stopped',
                participant_id: this.conferenceRoom.participantId
            });

        } catch (error) {
            LinguaMeet.log(`Erreur arrêt partage d'écran: ${error.message}`, 'error');
        }
    }

    cleanup() {
        // Arrêter le partage d'écran si actif
        if (this.isScreenSharing && this.screenStream) {
            this.screenStream.getTracks().forEach(track => track.stop());
        }
        
        // Fermer toutes les connexions peer
        this.peerConnections.forEach((pc, participantId) => {
            pc.close();
        });
        this.peerConnections.clear();
        
        // Arrêter le flux local
        if (this.localStream) {
            this.localStream.getTracks().forEach(track => track.stop());
        }
        
        LinguaMeet.log('Manager vidéo nettoyé');
    }

    getLocalStream() {
        return this.localStream;
    }
}
