(() => {
  const video = document.querySelector("video[data-film]");
  if (!video) return;
  const button = video.parentElement.querySelector(".film-control");
  const motion = window.matchMedia("(prefers-reduced-motion: reduce)");
  let visible = false;
  let pausedByUser = motion.matches || navigator.connection?.saveData === true;
  let request = 0;

  function label() {
    const stopped = video.paused;
    button.textContent = stopped ? "▶" : "Ⅱ";
    button.setAttribute("aria-pressed", String(stopped));
    button.setAttribute("aria-label", stopped ? "Включить анимацию" : "Пауза анимации");
  }
  async function synchronize() {
    const thisRequest = ++request;
    if (!visible || document.hidden || pausedByUser) {
      video.pause();
      label();
      return;
    }
    if (!video.hasAttribute("src")) video.src = video.dataset.film;
    try {
      await video.play();
    } catch {
      if (thisRequest === request) pausedByUser = true;
    }
    label();
  }
  button.addEventListener("click", () => {
    pausedByUser = !video.paused;
    synchronize();
  });
  motion.addEventListener("change", () => {
    pausedByUser = motion.matches;
    synchronize();
  });
  video.addEventListener("error", () => { button.hidden = true; });
  video.addEventListener("play", label);
  video.addEventListener("pause", label);
  document.addEventListener("visibilitychange", synchronize);
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(([entry]) => {
      visible = entry.isIntersecting;
      synchronize();
    }, {threshold: 0.05}).observe(video);
  } else {
    visible = true;
    synchronize();
  }
  label();
  button.hidden = false;
})();
