/* Shared journal structure and atomic storage. Browser global + CommonJS for offline tests. */
(function(root){
  'use strict';
  const KEY='kalori_journal_v1';
  function valid(data){
    if(!data||typeof data!=='object'||Array.isArray(data)||!Array.isArray(data.entries)||!data.water||typeof data.water!=='object'||Array.isArray(data.water))return false;
    if(data.entries.length>100000)return false;
    const ids=new Set();
    for(const e of data.entries){
      if(!e||typeof e!=='object'||Array.isArray(e)||typeof e.id!=='string'||!e.id||e.id.length>160||ids.has(e.id)||typeof e.day!=='string'||!/^\d{4}-\d{2}-\d{2}$/.test(e.day)||typeof e.food!=='string'||!e.food.trim()||e.food.length>300)return false;
      ids.add(e.id);
      for(const k of ['kcal','protein','fat','carbs'])if(e[k]!=null&&(typeof e[k]!=='number'||!Number.isFinite(e[k])||e[k]<0||e[k]>10000))return false;
    }
    for(const [day,v] of Object.entries(data.water))if(!/^\d{4}-\d{2}-\d{2}$/.test(day)||typeof v!=='number'||!Number.isFinite(v)||v<0||v>1000)return false;
    return true;
  }
  function read(storage){
    const raw=storage.getItem(KEY);
    if(raw===null)return {entries:[],water:{}};
    const value=JSON.parse(raw);
    if(!valid(value))throw Error('Journal invalid');
    return value;
  }
  function write(storage,value){
    if(!valid(value))throw Error('Journal invalid');
    storage.setItem(KEY,JSON.stringify(value));
    return value;
  }
  function add(data,entry){return {...data,entries:[...data.entries,entry]}}
  function remove(data,id){return {...data,entries:data.entries.filter(e=>e.id!==id)}}
  function water(data,day,delta){const count=data.water[day]||0;return {...data,water:{...data.water,[day]:Math.min(1000,Math.max(0,count+delta))}}}
  const api={KEY,valid,read,write,add,remove,water};
  root.KaloriJournal=api;
  if(typeof module==='object'&&module.exports)module.exports=api;
})(globalThis);
