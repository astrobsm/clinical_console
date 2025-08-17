// Force HTTPS for all API requests
self.addEventListener('fetch', function(event) {
  if (event.request.url.includes('/api/')) {
    const url = new URL(event.request.url);
    if (url.protocol === 'http:') {
      url.protocol = 'https:';
      const newRequest = new Request(url.toString(), {
        method: event.request.method,
        headers: event.request.headers,
        body: event.request.body,
        mode: event.request.mode,
        credentials: event.request.credentials,
        cache: event.request.cache,
        redirect: event.request.redirect,
        referrer: event.request.referrer
      });
      event.respondWith(fetch(newRequest));
    }
  }
});
