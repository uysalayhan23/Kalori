const assert=require('node:assert/strict');
const journal=require('../journal-data.js');
const key=journal.KEY;
const backing=new Map();
let rejectRead=false,rejectWrite=false;
const storage={
  getItem(k){if(rejectRead)throw Error('storage read denied');return backing.has(k)?backing.get(k):null;},
  setItem(k,v){if(rejectWrite)throw Error('quota exceeded');backing.set(k,v);}
};
const day='2026-10-12';
const entry={id:'restart-1',day,food:'Öğün',kcal:null};
const fresh=journal.read(storage);
assert.equal(fresh.entries.length,0);
journal.write(storage,journal.add(fresh,entry));
const appRestart=journal.read(storage);
assert.equal(appRestart.entries.length,1);
assert.equal(appRestart.entries[0].food,'Öğün');
const withWater=journal.water(appRestart,day,2);
journal.write(storage,withWater);
assert.equal(journal.read(storage).water[day],2);
const snapshot=backing.get(key);
rejectWrite=true;
assert.throws(()=>journal.write(storage,journal.remove(withWater,'restart-1')),/quota exceeded/);
assert.equal(backing.get(key),snapshot,'failed write must not alter prior records');
rejectWrite=false;
rejectRead=true;
assert.throws(()=>journal.read(storage),/storage read denied/);
assert.equal(backing.get(key),snapshot,'failed read must not clear persisted entries');
rejectRead=false;
assert.equal(journal.read(storage).entries.length,1);
backing.set(key,'{"entries":');
assert.throws(()=>journal.read(storage),SyntaxError);
assert.equal(backing.get(key),'{"entries":','corrupt storage must not be overwritten on read');
console.log('PASS: app-restart simulation, water persistence, read/write errors, corrupt journal preservation.');
