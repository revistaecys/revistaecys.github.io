document.addEventListener('DOMContentLoaded',()=>{const body=document.body;
const menu=document.getElementById('summary-toggle'); if(menu)menu.addEventListener('click',()=>{
 if(window.innerWidth<821){body.classList.toggle('show-summary');}else{body.classList.toggle('hide-summary');}});
const input=document.getElementById('chapter-search');if(input)input.addEventListener('input',()=>{
 const norm=s=>s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'');const q=norm(input.value);
 document.querySelectorAll('.summary li').forEach(li=>{li.hidden=!norm(li.textContent).includes(q)})});
const small=document.getElementById('font-down'),big=document.getElementById('font-up');let px=16;
if(small)small.addEventListener('click',()=>{px=Math.max(13,px-1);document.querySelector('.normal').style.fontSize=px+'px'});
if(big)big.addEventListener('click',()=>{px=Math.min(23,px+1);document.querySelector('.normal').style.fontSize=px+'px'});
window.addEventListener('keydown',e=>{if(e.key==='Escape')body.classList.remove('show-summary')});
});