(() => {
  "use strict";
  const reduced=matchMedia("(prefers-reduced-motion: reduce)");
  const fine=matchMedia("(hover:hover) and (pointer:fine)");
  const scenes=[...document.querySelectorAll("[data-scene]")];
  const visible=new Set();
  function refresh(){scenes.forEach(el=>el.classList.toggle("is-moving",visible.has(el)&&!document.hidden&&!reduced.matches));}
  if("IntersectionObserver" in window){
    const observer=new IntersectionObserver(entries=>{entries.forEach(e=>{e.isIntersecting?visible.add(e.target):visible.delete(e.target);});refresh();progress();});
    scenes.forEach(el=>observer.observe(el));
  }
  let pending=false;
  document.addEventListener("pointermove",event=>{
    if(!fine.matches||reduced.matches||document.hidden||pending)return;
    pending=true;
    requestAnimationFrame(()=>{visible.forEach(el=>{
      const r=el.getBoundingClientRect();
      const x=Math.max(-1,Math.min(1,(event.clientX-r.left-r.width/2)/(innerWidth/2)));
      const y=Math.max(-1,Math.min(1,(event.clientY-r.top-r.height/2)/(innerHeight/2)));
      el.style.setProperty("--scene-x",`${x*7}deg`);el.style.setProperty("--scene-y",`${y*-5}deg`);
    });pending=false;});
  },{passive:true});
  document.addEventListener("visibilitychange",refresh);
  reduced.addEventListener("change",()=>{scenes.forEach(el=>{el.style.removeProperty("--scene-x");el.style.removeProperty("--scene-y");});refresh();});
  let progressPending=false;
  const header=document.querySelector(".site-header");
  const entrances = document.querySelectorAll(".shortlist-model,.buyer-letter-layout,.shelf-story,.metric-cell,.service-tile,.delivery-list>div,.answer-lab,.reading-body>section,.question-list,.frequency-paper,.journal-opening h1,.audit-opening h1");
  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(entries => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        if (!reduced.matches) entry.target.classList.add("enter-light");
        observer.unobserve(entry.target);
      }
    }, {threshold: .08});
    entrances.forEach(el => observer.observe(el));
  }
  function progress(){if(progressPending)return;progressPending=true;requestAnimationFrame(()=>{
    header?.classList.toggle("is-scrolled", scrollY > 18);
    if(!document.hidden&&!reduced.matches){
      visible.forEach(el=>{
        const box=el.parentElement.getBoundingClientRect();
        const distance=(innerHeight/2-box.top-box.height/2)/innerHeight;
        el.style.setProperty("--scene-rise",(Math.max(-1,Math.min(1,distance))*1.625).toFixed(3)+"rem");
      });
    }
    progressPending=false;
  });}
  document.addEventListener("scroll",progress,{passive:true});progress();
  document.querySelectorAll(".a-benefit-grid,.a-three,.a-post-grid").forEach(grid=>[...grid.children].forEach((el,i)=>el.style.setProperty("--reveal-delay",`${i*70}ms`)));
})();
