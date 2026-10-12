const assert=require('node:assert/strict');
const journal=require('../journal-data.js');
const original={entries:[{id:'saved-1',day:'2026-10-12',food:'Öğün',kcal:null}],water:{'2026-10-12':1}};
let stored=JSON.stringify(original);
const storage={getItem:()=>stored,setItem:(key,val)=>{stored=val}};
const before=stored;
for(const invalid of [
  '{broken json',
  '[]',
  '{}',
  '{"entries":[],"water":[]}',
  '{"entries":[{"id":"x","day":"2026-10-12","food":"A","kcal":-1}],"water":{}}',
  '{"entries":[{"id":"dup","day":"2026-10-12","food":"A"},{"id":"dup","day":"2026-10-12","food":"B"}],"water":{}}'
]){
  assert.throws(()=>{const data=JSON.parse(invalid);if(!journal.valid(data))throw Error('invalid JSON backup');journal.write(storage,data)});
  assert.equal(stored,before,'invalid backup must not overwrite existing journal');
}
const valid=JSON.stringify({entries:[],water:{}});
journal.write(storage,JSON.parse(valid));
assert.deepEqual(journal.read(storage),JSON.parse(valid));
console.log('PASS: six invalid backup payloads rejected without overwriting journal; valid restore succeeds.');
