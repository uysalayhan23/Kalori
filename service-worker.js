/* Offline app shell only: never cache API responses or private diary data. */
const VERSION="kalori-static-v7";
const SHELL=["./","./index.html","./foods.html","./meal-builder.html","./profile.html","./barcode.html","./history.html","./food-catalog.js","./packaged-foods.js","./food-quality.js","./journal-data.js","./kalori-ui.css","./kalori-nav.js","./apple-touch-icon.png","./icon-192.png","./icon-512.png","./manifest.webmanifest"];
self.addEventListener("install",event=>{
  event.waitUntil(caches.open(VERSION).then(cache=>cache.addAll(SHELL)).then(()=>self.skipWaiting()));
});
self.addEventListener("activate",event=>{
  event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(key=>key.startsWith("kalori-static-")&&key!==VERSION).map(key=>caches.delete(key)))).then(()=>self.clients.claim()));
});
self.addEventListener("fetch",event=>{
  const request=event.request;
  if(request.method!=="GET")return;
  const url=new URL(request.url);
  if(url.origin!==self.location.origin)return;
  const allowed=SHELL.some(relative=>new URL(relative,self.registration.scope).href===url.href);
  if(!allowed)return;
  event.respondWith(
    fetch(request).then(response=>{
      if(response.ok){const copy=response.clone();event.waitUntil(caches.open(VERSION).then(cache=>cache.put(request,copy)));}
      return response;
    }).catch(()=>caches.match(request).then(cached=>cached||Response.error()))
  );
});
