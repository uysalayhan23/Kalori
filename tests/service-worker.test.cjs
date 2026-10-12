const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const path=require('node:path');
const source=fs.readFileSync(path.join(__dirname,'..','service-worker.js'),'utf8');
const handlers={};
const cache=new Map();
const cacheAPI={
 open:async()=>({addAll:async urls=>{for(const u of urls)cache.set(new URL(u,'https://example.test/app/').href,{ok:true,source:'precache',clone(){return this}})},put:async(req,res)=>{cache.set(req.url,res)}}),
 keys:async()=>['kalori-static-v3','kalori-static-v4'],
 delete:async()=>true,
 match:async req=>cache.get(req.url)
};
let online=true;
const ctx={
 self:{
 location:{origin:'https://example.test'},
 registration:{scope:'https://example.test/app/'},
 clients:{claim:async()=>{}},
 skipWaiting:async()=>{},
 addEventListener(name,fn){handlers[name]=fn}
 },
 URL,Response:{error:()=>({error:true})},caches:cacheAPI,
 fetch:async req=>{if(!online)throw Error('offline');return {ok:true,source:'network',clone(){return this}}}
};
vm.runInNewContext(source,ctx);
const install={waitUntil(p){this.promise=p}};
handlers.install(install);
(async()=>{
 await install.promise;
 const route='https://example.test/app/index.html';
 let promise;let updates=[];
 handlers.fetch({request:{method:'GET',url:route},waitUntil(p){updates.push(p)},respondWith(p){promise=p}});
 assert.equal((await promise).source,'network','online uses current file');
 await Promise.all(updates);
 online=false;
 handlers.fetch({request:{method:'GET',url:route},waitUntil(p){updates.push(p)},respondWith(p){promise=p}});
 assert.equal((await promise).source,'network','offline uses cached current file');
 promise=undefined;
 handlers.fetch({request:{method:'GET',url:'https://example.test/api/v2/search'},respondWith(p){promise=p}});
 assert.equal(promise,undefined,'API responses are never cached');
 const shell=source.match(/const SHELL=\[([^;]+)\];/)[1];
 assert.match(shell,/manifest\.webmanifest/,'manifest pre-cached');
 console.log('PASS: offline shell refresh, fallback and API exclusion.');
})().catch(e=>{console.error(e);process.exitCode=1});
