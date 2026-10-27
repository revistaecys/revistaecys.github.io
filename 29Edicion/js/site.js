document.addEventListener('DOMContentLoaded',()=>{
  const sidebar=document.querySelector('.sidebar');
  const overlay=document.querySelector('.mobile-overlay');
  const toggle=document.querySelector('#toggle-menu');
  const close=()=>{sidebar?.classList.remove('open');overlay?.classList.remove('show')};
  toggle?.addEventListener('click',()=>{sidebar?.classList.toggle('open');overlay?.classList.toggle('show')});
  overlay?.addEventListener('click',close);
  document.querySelector('#find-chapter')?.addEventListener('input',e=>{
    let q=e.target.value.toLocaleLowerCase('es').normalize('NFD').replace(/[\u0300-\u036f]/g,'');
    document.querySelectorAll('.sidebar-nav a').forEach(a=>{
      let name=a.textContent.toLocaleLowerCase('es').normalize('NFD').replace(/[\u0300-\u036f]/g,'');
      a.hidden=Boolean(q)&&!name.includes(q);
    });
  });
});
