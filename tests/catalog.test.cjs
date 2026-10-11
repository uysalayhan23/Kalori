/* Run: node tests/catalog.test.cjs (no npm, no GitHub Actions) */
const assert=require('node:assert/strict');
const fs=require('node:fs');const vm=require('node:vm');
const ctx={};ctx.globalThis=ctx;
vm.runInNewContext(fs.readFileSync('food-catalog.js','utf8'),ctx);
const foods=ctx.KaloriFoodCatalog.foods;
assert.equal(foods.length,195,'initial catalog count must not change silently');
assert.equal(new Set(foods.map(x=>x.id)).size,foods.length,'ids must be unique');
assert.equal(new Set(foods.map(x=>x.name.toLocaleLowerCase('tr'))).size,foods.length,'names must be unique');
for(const f of foods){
 assert.ok(f.name&&f.category);
 assert.ok(Number.isFinite(f.kcal)&&f.kcal>=0&&f.kcal<=900,'invalid energy: '+f.name);
 assert.equal(f.verification,'unverified','never imply verified without source');
 assert.equal(f.sourceReference,null,'placeholder citation');
 for(const m of ['protein','fat','carbs'])assert.equal(f[m],null,'missing macros must be unknown');
}
const gram=150,per100=83;assert.equal(per100*gram/100,124.5,'gram-based scaling');
console.log('PASS: '+foods.length+' catalog records, unique ids/names, provenance guard and gram scaling.');
