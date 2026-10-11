/* Static shell cache only. No online API responses or private journal data are cached. */
const VERSION="kalori-static-v1";
const SHELL=["./","./index.html","./foods.html","./meal-builder.html","./profile.html","./barcode.html","./food-catalog.js","./packaged-foods.js"];
self.addEventListener("install",event=>{event.waitUntil(caches.open(VERSION).then(cache=>cache.addAll(SHELL)).then(()=>self.skipWaiting()))});
self.addEventListener("activate",event=>{event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(key=>key.startsWith("kalori-static-")&&key!==VERSION).map(key=>caches.delete(key)))).then(()=>self.clients.claim()))});
self.addEventListener("fetch",event=>{const request=event.request;if(request.method!=="GET")return;const url=new URL(request.url);
 if(url.origin!==self.location.origin)return;
 event.respondWith(caches.match(request).then(cached=>cached||fetch(request).then(response=>response)));
});
