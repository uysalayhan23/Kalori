const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const html=fs.readFileSync(path.join(__dirname,'../index.html'),'utf8');
const journal=require('../journal-data.js');
const scripts=[...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].map(m=>m[1]);
assert.ok(scripts.length>=1);
const main=scripts.find(s=>s.includes('KaloriJournal.read(localStorage)'));
assert.ok(main,'main script not found');
class El{
 constructor(){this.value='';this.textContent='';this.children=[];this.events={};this.files=[];this.style={};}
 addEventListener(k,fn){this.events[k]=fn}
 click(){if(this.events.click)return this.events.click({preventDefault(){}})}
 submit(){if(this.events.submit)return this.events.submit({preventDefault(){}})}
 replaceChildren(...x){this.children=x}
 append(...x){this.children.push(...x)}
 get childNodes(){return this.children}
 setAttribute(){}
 reset(){}
}
async function scenario(failWrite=false,initial=null,restoreFile=null){
 const els=new Map(),backing=new Map();
 if(initial!==null)backing.set(journal.KEY,JSON.stringify(initial));
 const get=id=>{if(!els.has(id))els.set(id,new El());return els.get(id)};
 const store={getItem:k=>backing.get(k)??null,setItem(k,v){if(failWrite)throw Error('quota');backing.set(k,v)}};
 const document={getElementById:get,createElement:()=>new El()};
 const context={KaloriJournal:journal,localStorage:store,document,console,Date,Math,Number,String,Map,Set,
  confirm:()=>true,crypto:{randomUUID:()=> 'browser-test-'+Math.random()},navigator:{},location:{protocol:'file:'},
  Blob:class{},URL:{createObjectURL:()=>'',revokeObjectURL(){}},setTimeout:()=>{}};
 context.globalThis=context;
 vm.runInNewContext(main,context,{timeout:1500});
 get('day').value='2026-10-12';get('food').value='Sandviç';get('meal').value='Öğle';get('mealTime').value='12:00';
 get('portion').value='1 porsiyon';
 await get('foodForm').submit();
 return {get,backing,store,context};
}
(async()=>{
 const s=await scenario();
 assert.equal(journal.read(s.store).entries.length,1,'meal persisted');
 assert.equal(s.get('count').textContent,1,'meal shown');
 const snapshot=s.backing.get(journal.KEY);
 s.store.setItem=()=>{throw Error('quota')};
 s.get('waterAdd').click();
 assert.equal(s.backing.get(journal.KEY),snapshot,'failed water write must preserve disk');
 assert.equal(s.get('water').textContent,0,'failed water write must preserve UI');
 assert.match(s.get('feedback').textContent,/saklanamadı/);
 s.get('entries').children[0].children[1].click();
 assert.equal(s.get('count').textContent,1,'failed deletion must preserve UI');
 assert.equal(s.backing.get(journal.KEY),snapshot,'failed deletion must preserve disk');
 s.store.setItem=(k,v)=>s.backing.set(k,v);
 s.get('waterAdd').click();assert.equal(s.get('water').textContent,1);
 s.get('waterRemove').click();assert.equal(s.get('water').textContent,0);
 s.get('entries').children[0].children[1].click();
 assert.equal(s.get('count').textContent,0,'successful deletion reflected');
 assert.equal(journal.read(s.store).entries.length,0,'successful deletion persisted');
 const blocked=await scenario(true);
 assert.equal(blocked.get('count').textContent,0,'failed meal save must preserve UI');
 assert.equal(blocked.backing.has(journal.KEY),false,'failed meal save must not write');
 assert.match(blocked.get('feedback').textContent,/saklanamadı/);
 const before=JSON.stringify({entries:[{id:'existing',day:'2026-10-12',food:'Eski kayıt'}],water:{}});
 const restored=await scenario(false,JSON.parse(before));
 restored.get('restoreFile').files=[{size:12,text:async()=>'{not json'}];
 await restored.get('restore').click();
 assert.equal(restored.backing.get(journal.KEY),JSON.stringify(JSON.parse(before)));
 assert.match(restored.get('feedback').textContent,/değiştirilmedi/);
 restored.get('restoreFile').files=[{size:12,text:async()=>JSON.stringify({entries:[],water:{}})}];
 await restored.get('restore').click();
 assert.equal(journal.read(restored.store).entries.length,0,'valid restore persisted');
 assert.match(restored.get('feedback').textContent,/Yedek geri yüklendi/);
 const failedRestore=await scenario(false,JSON.parse(before));
 const previous=failedRestore.backing.get(journal.KEY);
 failedRestore.store.setItem=()=>{throw Error('quota')};
 failedRestore.get('restoreFile').files=[{size:12,text:async()=>JSON.stringify({entries:[],water:{}})}];
 await failedRestore.get('restore').click();
 assert.equal(failedRestore.backing.get(journal.KEY),previous,'failed restore preserves disk');
 assert.equal(failedRestore.get('count').textContent,2,'failed restore preserves UI'); // one existing plus scenario meal
 assert.match(failedRestore.get('feedback').textContent,/değiştirilmedi/);
 console.log('PASS: UI meal add/delete, water, invalid/valid/failed restore and quota consistency.');
})().catch(e=>{console.error(e);process.exitCode=1});
