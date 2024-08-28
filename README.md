# Enable PWA (Progressive Web App)

to enable the offline access PWA feature for local database web apps.

## program steps

input: project directory path (directory name as project name)

variables: project name, cur date, directory tree

preparation:

- sorting based on extension
- link manifest file to all .html
- insert service worker script in index.html

######### app.webmanifest ({project name})

```json
{
  "name": "$projectName",
  "short_name": "$projectName",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#000000",
  "theme_color": "#000000",
  "icons": [
    {
      "src": "icon.png",
      "sizes": "192x192",
      "type": "image/png"
    }
  ]
}
```

######### every `<head>` insertion ({current child path})

`<link href="$currentChildPath/app.webmanifest" rel="manifest" />`

######### `index.html` `<body>` insertion

`<script src="register-sw.js"></script>`

######### register-sw.js

```js
if ("serviceWorker" in navigator) {
    navigator.serviceWorker
        .register("/sw.js")
        .then((registration) => {
            console.log(
                "Service Worker registered with scope:",
                registration.scope
            );
        })
        .catch((error) => {
            console.error(
                "Service Worker registration failed:",
                error
            );
        });
}
```

######### sw.js ({current date, sorted directory tree})

```js
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

```
