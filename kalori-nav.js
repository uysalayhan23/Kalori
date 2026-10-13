/* Kalori navigation: original icons, keyboard- and screen-reader-friendly. */
(function(){
  'use strict';
  if(!document.body || document.querySelector('.kh-tabbar'))return;
  const path=(location.pathname||'').split('/').pop()||'index.html';
  const home=path==='index.html';
  const meal=['meal-builder.html','foods.html','barcode.html'].includes(path);
  const history=path==='history.html';
  const icons={
    home:'<path d="m3 10 9-7 9 7v10a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V10Z"/><path d="M9 21v-7h6v7"/>',
    meal:'<path d="M4 3v7a3 3 0 0 0 6 0V3M7 3v18M17 3v18M17 3c4 2 4 7 0 9"/>',
    history:'<rect x="3" y="5" width="18" height="16" rx="3"/><path d="M7 3v4m10-4v4M3 10h18m-13 5h3m3 0h3"/>',
    profile:'<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 3.4-7 8-7s8 3 8 7"/>'
  };
  const tabs=[
    {url:'index.html',text:'Ana sayfa',icon:'home',active:home},
    {url:'meal-builder.html',text:'Öğün ekle',icon:'meal',active:meal},
    {url:'history.html',text:'Geçmiş',icon:'history',active:history},
    {url:'profile.html',text:'Profil',icon:'profile',active:!home&&!meal&&!history}
  ];
  const nav=document.createElement('nav');
  nav.className='kh-tabbar';
  nav.setAttribute('aria-label','Kalori alt gezinme');
  for(const tab of tabs){
    const a=document.createElement('a');
    a.href=tab.url;
    a.setAttribute('aria-label',tab.text);
    if(tab.active)a.setAttribute('aria-current','page');
    a.innerHTML='<svg viewBox="0 0 24 24" aria-hidden="true">'+icons[tab.icon]+'</svg><span>'+tab.text+'</span>';
    nav.appendChild(a);
  }
  document.body.appendChild(nav);
})();
