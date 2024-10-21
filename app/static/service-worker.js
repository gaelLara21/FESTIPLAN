const CACHE_NAME = 'app-cache-v1';
const urlsToCache = [
  '/',
  '/login',
  '/signup',
  '/boletos',
  '/crear',
  '/venta',
  '/contacto',
  '/nosotros',
  '/terminos',
  '/galeria',
  '/eventos',
  '/mis_boletos',
  '/mis_eventos',
  '/static/css/styles.css',
  '/static/css/style.css',
  '/static/css/register.css',
  '/static/js/jquery-3.5.1.min.js',
  '/css/bootstrap.min.css', 
  '/css/all.min.css',       
  '/js/bootstrap.bundle.min.js',
  '/static/icons/icon-192x192.png',
  '/static/icons/icon-512x512.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache);
      })
  );
});
// Manejo de las solicitudes
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        return response || fetch(event.request);
      })
  );
});

// Actualización del caché
self.addEventListener('activate', event => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (!cacheWhitelist.includes(cacheName)) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
