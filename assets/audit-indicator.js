(() => {
  const board = document.querySelector("[data-indicator]");
  if (!board) return;
  const renderer = board.querySelector(".animated-indicator");
  const ctx = renderer.querySelector("canvas").getContext("2d");
  if (!ctx || !window.IntersectionObserver) return;
  const reduced = matchMedia("(prefers-reduced-motion: reduce)");
  const atlas = new Image();
  const positions = {name:16,source:32,link:48};
  let cursor = 0, animation = 0, visible = false;

  function stop() {
    cancelAnimationFrame(animation);
    animation = 0;
  }

  function select() {
    stop();
    const key = board.querySelector("input:checked").value;
    const end = positions[key];
    const target = board.querySelector('[data-variant="'+key+'"] .sample-coding');
    if (!atlas.naturalWidth || !visible || document.hidden || reduced.matches) {
      renderer.classList.remove("ready");
      return;
    }
    target.prepend(renderer);
    renderer.classList.add("ready");
    const start = cursor;
    const began = performance.now();
    const duration = Math.max(280, Math.abs(end-start)*28);
    function paint(now) {
      const t = Math.min(1,(now-began)/duration);
      cursor = start+(end-start)*(t*t*(3-2*t));
      const index = Math.round(cursor);
      const size = atlas.naturalWidth/7, height = atlas.naturalHeight/7;
      ctx.clearRect(0,0,420,280);
      ctx.drawImage(atlas,(index%7)*size,Math.floor(index/7)*height,size,height,0,0,420,280);
      if (t < 1) animation=requestAnimationFrame(paint);
    }
    paint(began);
  }
  function sync() {
    if (visible && !document.hidden && !reduced.matches && !navigator.connection?.saveData && !atlas.src) {
      atlas.src=board.dataset.indicator;
    }
    select();
  }
  atlas.addEventListener("load",select);
  board.addEventListener("change",select);
  new IntersectionObserver(([entry])=>{visible=entry.isIntersecting;sync()},{threshold:.03}).observe(board);
  reduced.addEventListener("change",sync);
  document.addEventListener("visibilitychange",sync);
})();
