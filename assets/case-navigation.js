// Mark the chapter crossing the reading line, including when a saved link opens.
(() => {
  const nav = document.querySelector(".case-contents");
  if (!nav) return;
  const chapters = [...nav.querySelectorAll('a[href^="#"]')]
    .map((link) => ({
      link,
      section: document.getElementById(link.hash.slice(1)),
    }))
    .filter((chapter) => chapter.section);
  if (!chapters.length) return;
  const header = document.querySelector(".site-header");
  let pending = false;
  function update() {
    pending = false;
    const line =
      (header?.offsetHeight || 0) + Math.min(innerHeight * 0.22, 160);
    let current = null;
    for (const chapter of chapters) {
      if (chapter.section.getBoundingClientRect().top <= line)
        current = chapter;
    }
    for (const chapter of chapters) {
      if (chapter === current)
        chapter.link.setAttribute("aria-current", "location");
      else chapter.link.removeAttribute("aria-current");
    }
  }
  function schedule() {
    if (pending) return;
    pending = true;
    requestAnimationFrame(update);
  }
  window.addEventListener("scroll", schedule, { passive: true });
  window.addEventListener("resize", schedule);
  window.addEventListener("pageshow", schedule);
  update();
})();
