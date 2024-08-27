import os
from datetime import datetime

def afterlast(arr, offsetstr):
    return arr[ len( arr ) - arr[::-1].index( offsetstr[::-1] ):]

def get_sorted_files(directory):
    unrelatedPWAFiles = ["README.md"]
    extensions = []
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if afterlast(file, '.') not in extensions:
                extensions.append(afterlast(file, '.'))
            file_list.append(afterlast(root, directory).replace("\\", '/') + "/" + file)

    if "/sw.js" not in file_list:
        file_list.append("/sw.js")
    
    # sort based on extension
    sortedExts = sorted(extensions)
    sortedFiles = []
    for e in sortedExts:
        for f in file_list:
            if f in unrelatedPWAFiles:
                continue
            if afterlast(f, '.') == e:
                sortedFiles.append(f)
    return sortedFiles


appWM = """{
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
"""

headInsertion = '<link href="$currentChildPathapp.webmanifest" rel="manifest" />'

bodyInsertion = '<script src="register-sw.js"></script>'

registerSW = """if ("serviceWorker" in navigator) {
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
"""
SWfile = """const CACHE_VERSION = "$currentDate";
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
"""


# input
directoryPath = input("project directory path: ")

projectName = ''
if "\\" in directoryPath:
    projectName = afterlast(directoryPath, "\\")
else:
    projectName = directoryPath

# Get the current date
currentDate = datetime.now().strftime("%Y-%m-%d %H:%M")

# insertion
print("inserting")
for root, dirs, files in os.walk(directoryPath):
    for file in files:
        if file.endswith(".html"):
            file_path = root + "\\" + file
            with open(file_path, "r+") as f:
                content = f.read()

                # does root contain absolute path with \ at the end
                manifestLinkHTML = headInsertion.replace("$currentChildPath", afterlast(root + "\\", directoryPath).replace("\\", '/')[1:])
                if manifestLinkHTML not in content:
                    content = content.replace("</head>", f"\t{manifestLinkHTML}\n\t</head>")

                if file == "index.html" and bodyInsertion not in content:
                    content = content.replace("</body>", f"\t{bodyInsertion}\n\t</body>")

                f.seek(0)
                f.write(content)
                f.truncate()

# file creation
print("writing /app.webmanifest")
with open(directoryPath + "/app.webmanifest", "w") as f:
    f.write(appWM.replace("$projectName", projectName))

print("writing /register-sw.js")
with open(directoryPath + "/register-sw.js", "w") as f:
    f.write(registerSW)

print("writing /sw.js")
with open(directoryPath + "/sw.js", "w") as f:
    sortedDirectoryTree = get_sorted_files(directoryPath)
    sortedDirectoryTree_str = ''
    curExt = ''
    for p in sortedDirectoryTree:
        if curExt and curExt != afterlast(p, '.'):
            sortedDirectoryTree_str += '\n'
        curExt = afterlast(p, '.')
        sortedDirectoryTree_str += '\t"' + p + '",\n'
    f.write(SWfile.replace("$currentDate", currentDate).replace("$sortedDirectoryTree", sortedDirectoryTree_str))

input("DONE")
