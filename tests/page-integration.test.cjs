const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const path=require('node:path');
const journal=require('../journal-data.js');
const root=path.join(__dirname,'..');
const pages=['index.html','meal-builder.html','history.html'];
for(const page of pages){
  const html=fs.readFileSync(path.join(root,page),'utf8');
  assert.match(html,/<script src="journal-data\.js"><\/script>/,'shared journal script missing: '+page);
  for(const match of html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g))
    new vm.Script(match[1],{filename:page});
}
const date='2026-10-12';
const row={id:'a',day:date,time:'13:00',meal:'Öğle',food:'Makarna',kcal:300,protein:10,carbs:45,fat:7};
const second={id:'b',day:date,time:'14:30',meal:'Ara öğün',food:'Meyve',kcal:null,protein:null,carbs:null,fat:null};
let db={entries:[],water:{}};
db=journal.add(db,row);
db=journal.add(db,second);
db=journal.water(db,date,2);
const store={value:null,getItem(){return this.value},setItem(k,v){this.value=v}};
journal.write(store,db);
const reloaded=journal.read(store);
assert.equal(reloaded.entries.filter(e=>e.day===date).length,2);
assert.equal(reloaded.entries.filter(e=>typeof e.kcal==='number').reduce((a,e)=>a+e.kcal,0),300);
assert.equal(reloaded.water[date],2);
db=journal.remove(reloaded,'a');
journal.write(store,db);
assert.equal(journal.read(store).entries.length,1);
assert.equal(journal.read(store).entries[0].kcal,null);
assert.equal(journal.valid({entries:[{...row,kcal:Infinity}],water:{}}),false);
console.log('PASS: three page script syntax, shared journal loading, reload, partial energy, remove and water.');
