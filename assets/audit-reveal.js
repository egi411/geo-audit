(() => {
  const spread = document.querySelector(".report-spread");
  const motion = matchMedia("(prefers-reduced-motion: reduce)");
  if (!spread) return;

  const board = spread.querySelector(".scoreboard");
  // Reveal the changed answer only when the selector is too close to a viewport edge.
  function keepAnswerVisible(element) {
    if (!element) return;
    const box = element.getBoundingClientRect();
    const header = document.querySelector(".site-header").getBoundingClientRect();
    const top = header.bottom + 14;
    const bottom = window.innerHeight - 14;
    const excerptEnd = box.top + Math.min(box.height, 130);
    if (box.top < top || excerptEnd > bottom) {
      window.scrollBy({top: box.top < top ? box.top - top : excerptEnd - bottom, behavior: "instant"});
    }
  }
  document.querySelector(".sample-choices")?.addEventListener("change", (event) => {
    const active = document.querySelector('[data-variant="' + event.target.value + '"] blockquote');
    keepAnswerVisible(active);
  });

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
