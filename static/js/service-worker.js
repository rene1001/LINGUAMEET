/**
 * Service Worker pour LinguaMeet
 * Progressive Web App (PWA)
 * Version: 1.0.0
 */

const CACHE_NAME = 'linguameet-v1.0.0';
const OFFLINE_URL = '/offline/';

// Fichiers à mettre en cache
const CACHE_URLS = [
    '/',
    '/static/css/style.css',
    '/static/js/main.js',
    '/offline/',
    // Bootstrap et Font Awesome sont chargés depuis CDN, ils seront mis en cache dynamiquement
];

// Installation du Service Worker
self.addEventListener('install', (event) => {
    console.log('[Service Worker] Installation...');
    
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('[Service Worker] Cache ouvert');
                // Ajouter les URLs essentielles au cache
                return cache.addAll(CACHE_URLS.filter(url => !url.includes('offline')));
            })
            .then(() => self.skipWaiting())
    );
});

// Activation du Service Worker
self.addEventListener('activate', (event) => {
    console.log('[Service Worker] Activation...');
    
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('[Service Worker] Suppression ancien cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

// Interception des requêtes (stratégie Network First)
self.addEventListener('fetch', (event) => {
    // Ignorer les requêtes non-HTTP
    if (!event.request.url.startsWith('http')) {
        return;
    }
    
    // Ignorer les WebSockets
    if (event.request.url.includes('ws://') || event.request.url.includes('wss://')) {
        return;
    }
    
    // Ignorer les requêtes admin
    if (event.request.url.includes('/admin/')) {
        return;
    }
    
    event.respondWith(
        // Stratégie: Network First, fallback to Cache
        fetch(event.request)
            .then((response) => {
                // Si la réponse est valide, la mettre en cache
                if (response && response.status === 200) {
                    const responseToCache = response.clone();
                    
                    caches.open(CACHE_NAME).then((cache) => {
                        // Ne pas cacher les requêtes POST/PUT/DELETE
                        if (event.request.method === 'GET') {
                            cache.put(event.request, responseToCache);
                        }
                    });
                }
                
                return response;
            })
            .catch(() => {
                // En cas d'erreur réseau, chercher dans le cache
                return caches.match(event.request)
                    .then((cachedResponse) => {
                        if (cachedResponse) {
                            return cachedResponse;
                        }
                        
                        // Si la ressource n'est pas en cache, retourner la page offline
                        if (event.request.mode === 'navigate') {
                            return caches.match(OFFLINE_URL);
                        }
                        
                        // Pour les autres types de requêtes, retourner une réponse vide
                        return new Response('Offline', {
                            status: 503,
                            statusText: 'Service Unavailable',
                            headers: new Headers({
                                'Content-Type': 'text/plain'
                            })
                        });
                    });
            })
    );
});

// Gestion des messages
self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
    
    if (event.data && event.data.type === 'CLEAR_CACHE') {
        event.waitUntil(
            caches.delete(CACHE_NAME).then(() => {
                console.log('[Service Worker] Cache vidé');
                return self.registration.unregister();
            })
        );
    }
});

// Notification de mise à jour disponible
self.addEventListener('controllerchange', () => {
    console.log('[Service Worker] Nouvelle version disponible');
});
