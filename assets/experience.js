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
  const readingProgress=document.querySelector(".a-reading-progress");
  function progress(){if(progressPending)return;progressPending=true;requestAnimationFrame(()=>{
    const max=document.documentElement.scrollHeight-innerHeight;
    readingProgress?.style.setProperty("--read",max>0?String(scrollY/max):"0");
    if(!document.hidden&&!reduced.matches){
      visible.forEach(el=>{
        const box=el.parentElement.getBoundingClientRect();
        const distance=(innerHeight/2-box.top-box.height/2)/innerHeight;
        el.style.setProperty("--scene-rise",Math.round(Math.max(-1,Math.min(1,distance))*26)+"px");
      });
    }
    progressPending=false;
  });}
  document.addEventListener("scroll",progress,{passive:true});progress();
  document.querySelectorAll(".a-benefit-grid,.a-three,.a-post-grid").forEach(grid=>[...grid.children].forEach((el,i)=>el.style.setProperty("--reveal-delay",`${i*70}ms`)));
})();
