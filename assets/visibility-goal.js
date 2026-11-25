// The static document already shows the complete target, including with JS disabled.
(() => {
  const home = document.querySelector(".home-hero");
  const header = document.querySelector(".site-header");
  const notice = document.querySelector(".cookie-banner");
  function fitHero() {
    home.style.setProperty(
      "--top-chrome",
      header.offsetHeight + notice.offsetHeight + "px",
    );
  }
  fitHero();
  if ("ResizeObserver" in window) {
    const observer = new ResizeObserver(fitHero);
    observer.observe(header);
    observer.observe(notice);
  } else window.addEventListener("resize", fitHero);

  const scene = document.querySelector(".visibility-scene");
  const number = scene.querySelector("[data-coverage-value]");
  const parts = [...scene.querySelectorAll(".coverage-segments path")];
  const motion = matchMedia("(prefers-reduced-motion: reduce)");
  if (motion.matches || !("IntersectionObserver" in window)) return;

  let frame = 0;
  let previous = 0;
  function paint(count) {
    for (let i = previous; i < count; i++) parts[i].classList.add("filled");
    number.textContent = String(count);
    previous = count;
  }
  function finish() {
    cancelAnimationFrame(frame);
    scene.classList.remove("filling");
    number.textContent = parts.length;
    motion.removeEventListener("change", finish);
  }
  const observer = new IntersectionObserver(([entry]) => {
    if (!entry.isIntersecting) return;
    observer.disconnect();
    if (motion.matches) return;
    const start = performance.now();
    scene.classList.add("filling");
    motion.addEventListener("change", finish);
    function tick(now) {
      const progress = Math.max(0, Math.min(1, (now - start) / 1450));
      paint(Math.floor(parts.length * (1 - (1 - progress) ** 2)));
      if (progress < 1) frame = requestAnimationFrame(tick);
      else finish();
    }
    tick(start);
  });
  observer.observe(scene);
})();
