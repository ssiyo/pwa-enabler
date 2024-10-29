const CACHE_VERSION = "$currentDate";
localStorage.setItem("CACHE_VERSION", CACHE_VERSION)

// cache files list
const cf = [
    "/",
$sortedDirectoryTree
];
self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(CACHE_VERSION).then(async (cache) => {
            console.log("ServiceWorker: Caching files:", cf.length, cf);
            try {
                cachedResult = await cache.addAll(cf);
            } catch (err) {
                console.error("sw: cache.addAll");
                for (let f of cf) {
                    try {
                        cachedResult = await cache.add(f);
                    } catch (err) {
                        console.warn("sw: cache.add", f);
                    }
                }
            }
            console.log("ServiceWorker: caching ended");

            return cachedResult;
        })
    );
});

self.addEventListener("activate", (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_VERSION) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

self.addEventListener("fetch", (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request);
        })
    );
});