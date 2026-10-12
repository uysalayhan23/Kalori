const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const journal=require('../journal-data.js');
const pages=Object.fromEntries(['meal-builder.html','index.html','history.html'].map(n=>[n,fs.readFileSync(path.join(__dirname,'..',n),'utf8')]));
const scripts=Object.fromEntries(Object.entries(pages).map(([n,s])=>[n,[...s.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].map(m=>m[1]).find(s=>s.includes('KaloriJournal.read(localStorage)'))]));
for(const [n,s] of Object.entries(scripts))assert.ok(s,n+' missing journal script');
class Element {
 constructor(){this.value='';this.textContent='';this.children=[];this.events={};this.style={};this.hidden=true;this.files=[];this.onclick=null;}
 replaceChildren(...items){this.children=items;if(items.length&&typeof items[0].value==='string')this.value=items[0].value}
 append(...items){this.children.push(...items)}
 addEventListener(k,fn){this.events[k]=fn}
 get childNodes(){return this.children}
 get childElementCount(){return this.children.length}
 setAttribute(){}
 reset(){}
 click(){return (this.onclick||this.events.click)?.({preventDefault(){}})}
 submit(){return this.events.submit?.({preventDefault(){}})}
}
const backing=new Map();let writable=true;
const storage={getItem:key=>backing.get(key)??null,setItem(key,value){if(!writable)throw Error('quota');backing.set(key,value)}};
const food={id:'food-test',name:'Deneme yiyeceği',kcal:120,protein:6,carbs:17,fat:3,category:'sample'};
function open(name){
 const map=new Map(),get=id=>{if(!map.has(id))map.set(id,new Element());return map.get(id)};
 const doc={getElementById:get,createElement:()=>new Element()};
 const ctx={document:doc,localStorage:storage,KaloriJournal:journal,KaloriFoodCatalog:{foods:[food]},KaloriPackagedFoods:[],KaloriFoodQuality:{warning:()=>null,blocksGrams:()=>false},
  Date,Math,Number,String,Map,Set,Option:class{constructor(text,value){this.text=text;this.value=value}},
  confirm:()=>true,crypto:{randomUUID:()=> 'home-generated'},setTimeout:()=>{},console};
 ctx.globalThis=ctx;
 vm.runInNewContext(scripts[name],ctx,{timeout:2000});
 return {get,ctx};
}
(async()=>{
 const builder=open('meal-builder.html');
 const date='2026-10-12';
 builder.get('day').value=date;builder.get('time').value='12:30';
 builder.get('meal').value='Öğle';builder.get('food').value=food.id;builder.get('grams').value='150';
 builder.get('add').click();
 assert.equal(builder.get('items').children.length,1);
 assert.match(builder.get('total').textContent,/180\.0 kcal/);
 writable=false;
 builder.get('save').click();
 assert.match(builder.get('message').textContent,/kaydedilemedi/);
 assert.equal(builder.get('items').children.length,1,'failed save must retain pending meal');
 assert.equal(backing.has(journal.KEY),false,'failed save must not create journal');
 writable=true;
 builder.get('save').click();
 assert.match(builder.get('message').textContent,/kaydedildi/);
 assert.equal(builder.get('items').children.length,1,'empty meal placeholder after save');
 let rows=journal.read(storage).entries;
 assert.equal(rows.length,1);
 assert.equal(rows[0].day,date);
 assert.equal(rows[0].food,food.name);
 assert.equal(rows[0].kcal,180);
 const home=open('index.html');
 home.get('day').value=date;home.get('day').events.change();
 assert.equal(home.get('count').textContent,1);
 assert.ok(home.get('entries').children.some(row=>row.children.some(child=>child.textContent===food.name)));
 const history=open('history.html');
 history.get('day').value=date;history.get('day').events.change();
 assert.ok(history.get('entries').children.some(row=>row.children.some(child=>child.textContent.includes(food.name))));
 const snapshot=backing.get(journal.KEY);
 writable=false;
 home.get('entries').children[0].children[1].click();
 assert.equal(backing.get(journal.KEY),snapshot,'failed delete must preserve disk');
 assert.equal(home.get('count').textContent,1,'failed delete must preserve UI');
 writable=true;
 home.get('entries').children[0].children[1].click();
 assert.equal(journal.read(storage).entries.length,0);
 const emptyHistory=open('history.html');
 emptyHistory.get('day').value=date;emptyHistory.get('day').events.change();
 assert.ok(emptyHistory.get('entries').children.some(row=>row.textContent.includes('kayıt bulunamadı')));
 const backup={entries:[{...rows[0],id:'restored-test'}],water:{[date]:2}};
 home.get('restoreFile').files=[{size:100,text:async()=>JSON.stringify(backup)}];
 await home.get('restore').click();
 assert.equal(journal.read(storage).entries.length,1);
 assert.equal(journal.read(storage).water[date],2);
 const restoredHistory=open('history.html');
 restoredHistory.get('day').value=date;restoredHistory.get('day').events.change();
 assert.ok(restoredHistory.get('entries').children.some(row=>row.children.some(child=>child.textContent.includes(food.name))));
 console.log('PASS: meal-builder selection/grams/save/quota, home delete, history reload, JSON restore, shared storage.');
})().catch(e=>{console.error(e);process.exitCode=1});
