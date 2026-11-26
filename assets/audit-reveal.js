(() => {
  const cover = document.querySelector(".audit-opening");
  const header = document.querySelector(".site-header");
  const notice = document.querySelector(".cookie-banner");
  let frame = 0;

  function updateNavigation() {
    frame = 0;
    header.classList.toggle("is-past-cover", cover.getBoundingClientRect().bottom <= header.offsetHeight + 1);
  }
  function scheduleNavigation() {
    if (!frame) frame = requestAnimationFrame(updateNavigation);
  }
  function fitCover() {
    cover.style.setProperty("--top-chrome", header.offsetHeight + notice.offsetHeight + "px");
    scheduleNavigation();
  }

  fitCover();
  window.addEventListener("scroll", scheduleNavigation, { passive: true });
  window.addEventListener("resize", fitCover);
  window.addEventListener("pageshow", fitCover);
  if ("ResizeObserver" in window) {
    const chrome = new ResizeObserver(fitCover);
    chrome.observe(header);
    chrome.observe(notice);
  }

  const spread = document.querySelector(".report-spread");
  const motion = matchMedia("(prefers-reduced-motion: reduce)");
  if (!spread) return;

  const board = spread.querySelector(".scoreboard");
  if ("IntersectionObserver" in window) {
    const revealBars = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) {
        board.classList.add("in-view");
        revealBars.disconnect();
      }
    }, { threshold: 0.16 });
    revealBars.observe(board);
  }
  const barsFor = key => board.querySelectorAll('[data-measure="' + key + '"] li b');
  let previousMeasure = board.querySelector("input:checked").value;
  board.querySelector(".score-tabs").addEventListener("change", event => {
    const nextMeasure = event.target.value;
    if (!motion.matches && typeof board.animate === "function") {
      const previousBars = barsFor(previousMeasure);
      board.classList.add("is-comparing");
      barsFor(nextMeasure).forEach((bar, i) => {
        const start = previousBars[i].style.getPropertyValue("--value");
        const end = bar.style.getPropertyValue("--value");
        bar.animate([{ width: start }, { width: end }], {
          duration: 390, easing: "cubic-bezier(.25,.7,.25,1)"
        });
      });
    }
    previousMeasure = nextMeasure;
  });

  if (motion.matches || !("IntersectionObserver" in window)) return;

  const pocket = spread.querySelector(".report-pocket");
  if (pocket.getBoundingClientRect().bottom <= 0 || spread.contains(document.activeElement)) return;

  const observer = new IntersectionObserver(([entry]) => {
    if (entry.isIntersecting) {
      spread.dataset.fold = "opening";
      observer.disconnect();
    } else if (entry.boundingClientRect.bottom <= 0) {
      finish();
    }
  }, { rootMargin: "0px 0px -6% 0px" });

  function finish() {
    observer.disconnect();
    delete spread.dataset.fold;
    spread.removeEventListener("focusin", finish);
    spread.removeEventListener("animationend", onAnimationEnd);
    motion.removeEventListener("change", finish);
  }
  function onAnimationEnd(event) {
    if (event.animationName === "unfold-report") finish();
  }

  spread.dataset.fold = "closed";
  spread.addEventListener("animationend", onAnimationEnd);
  spread.addEventListener("focusin", finish);
  motion.addEventListener("change", finish);
  observer.observe(pocket);
})();
