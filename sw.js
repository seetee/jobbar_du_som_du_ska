// Service worker för Arbetstid.
//
// Strategi: nätet först, cache som reserv. Appen är ett enda dokument utan
// versionerade filnamn, så cache-first skulle visa gammal kod tills cachen
// råkade rensas. Nät-först ger alltid senaste versionen när det finns täckning,
// och cachen tar över när det inte gör det.
//
// Höj CACHE-versionen när precache-listan ändras — activate städar bort resten.
const CACHE = "arbetstid-v1";
const SHELL = [
  "./",
  "./index.html",
  "./manifest.webmanifest",
  "./icons/icon-192.png",
  "./icons/icon-512.png",
  "./icons/icon-maskable-512.png",
  "./icons/apple-touch-icon.png",
];

self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE)
      .then(cache => cache.addAll(SHELL))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", event => {
  const req = event.request;
  // Lämna allt annat än egna GET-anrop till webbläsaren.
  if (req.method !== "GET" || new URL(req.url).origin !== location.origin) return;

  event.respondWith(
    fetch(req)
      .then(res => {
        // Bara lyckade svar får ersätta en fungerande kopia i cachen.
        if (res.ok) {
          const copy = res.clone();
          caches.open(CACHE).then(cache => cache.put(req, copy));
        }
        return res;
      })
      .catch(() =>
        caches.match(req).then(hit =>
          // Offline och okänd URL: navigeringar landar på appen, annars 504.
          hit || (req.mode === "navigate"
            ? caches.match("./index.html")
            : new Response("", { status: 504, statusText: "Offline" }))
        )
      )
  );
});
