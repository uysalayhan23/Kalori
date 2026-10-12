const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const journal=require('../journal-data.js');
const history=fs.readFileSync(path.join(__dirname,'../history.html'),'utf8');
const mealBuilder=fs.readFileSync(path.join(__dirname,'../meal-builder.html'),'utf8');
const home=fs.readFileSync(path.join(__dirname,'../index.html'),'utf8');
for(const page of [home,mealBuilder,history]){
 assert.ok(page.includes('src="journal-data.js"'));
 assert.ok(page.includes('KaloriJournal.read(localStorage)'));
}
const script=[...history.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].map(x=>x[1]).find(s=>s.includes('KaloriJournal.read(localStorage)'));
assert.ok(script);
class Element {
 constructor(){this.children=[];this.value='';this.textContent='';this.hidden=true;this.style={};this.events={};}
 append(...x){this.children.push(...x)}
 replaceChildren(...x){this.children=x;if(x.length && typeof x[0].value==="string")this.value=x[0].value}
 get childElementCount(){return this.children.length}
 addEventListener(name,fn){this.events[name]=fn}
}
function show(storage){
 const elements=new Map();
 const get=id=>{if(!elements.has(id))elements.set(id,new Element());return elements.get(id)};
 const document={getElementById:get,createElement:()=>new Element()};
 const ctx={KaloriJournal:journal,localStorage:storage,document,Date,Number,String,Map,Set,Math,Option:class{constructor(text,value){this.text=text;this.value=value}},KaloriFoodQuality:{warning:()=>null},KaloriPackagedFoods:[]};
 ctx.globalThis=ctx;
 vm.runInNewContext(script,ctx,{timeout:1500});
 return {get};
}
const saved=new Map(),storage={getItem:k=>saved.get(k)??null,setItem:(k,v)=>saved.set(k,v)};
const day=new Date();const date=[day.getFullYear(),String(day.getMonth()+1).padStart(2,'0'),String(day.getDate()).padStart(2,'0')].join('-');
const entry={id:'between-pages',day:date,food:'Ev yapımı öğün',meal:'Öğle',time:'12:00',kcal:null};
journal.write(storage,journal.add(journal.read(storage),entry));
let page=show(storage);
assert.ok(page.get('entries').children.some(row=>row.children.some(child=>child.textContent.includes('Ev yapımı öğün'))),'history should show saved home/meal-builder entry');
journal.write(storage,journal.remove(journal.read(storage),entry.id));
page=show(storage);
assert.equal(page.get('entries').children.length,1);
assert.match(page.get('entries').children[0].textContent,/kayıt bulunamadı/);
journal.write(storage,{entries:[entry],water:{}});
const snapshot=saved.get(journal.KEY);
const denied={getItem(){throw Error('denied')},setItem(){throw Error('denied')}};
page=show(denied);
assert.equal(page.get('storageError').hidden,false);
assert.match(page.get('storageError').textContent,/okunamadı/);
assert.equal(saved.get(journal.KEY),snapshot);
console.log('PASS: shared journal history add/delete reload and unreadable storage warning.');
