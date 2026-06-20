// Clear older Hugo Nuo service worker caches and then unregister this worker.
// The blog is static and does not need runtime caching; stale caches can mask
// fresh GitHub Pages deployments and cause confusing asset 404s.
self.addEventListener('install', event => {
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches
      .keys()
      .then(keys => Promise.all(keys.map(key => caches.delete(key))))
      .then(() => self.registration.unregister())
      .then(() => self.clients.matchAll({ type: 'window' }))
      .then(clients => Promise.all(clients.map(client => client.navigate(client.url)))),
  );
});
