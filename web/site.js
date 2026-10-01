const root=document.documentElement;
const button=document.querySelector('#theme');
const storage={get(){try{return localStorage.getItem('lecture-theme')}catch{return null}},set(v){try{localStorage.setItem('lecture-theme',v)}catch{}}};
function theme(v){root.dataset.theme=v;button.textContent=v==='dark'?'Light theme':'Dark theme';button.setAttribute('aria-pressed',String(v==='dark'))}
theme(storage.get()||'light');
button.addEventListener('click',()=>{const v=root.dataset.theme==='dark'?'light':'dark';theme(v);storage.set(v)});
const search=document.querySelector('#search');
if(search){
  const rows=[...document.querySelectorAll('.book-row')];
  search.addEventListener('input',()=>{
    const q=search.value.trim().toLocaleLowerCase();let count=0;
    for(const r of rows){r.hidden=!r.dataset.search.toLocaleLowerCase().includes(q);if(!r.hidden)count++}
    document.querySelector('#result-count').textContent=count+' projects';
    document.querySelector('#empty').hidden=count!==0;
  });
}
