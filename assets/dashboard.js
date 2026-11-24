(() => {
  const header = document.querySelector(".site-header");
  const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)");
  const home = document.querySelector(".home-hero");
  if (home || document.querySelector("#case-directory")) {
    const moveCaseBookmark = () => {
      const oldRoute = {
        "#case-fashion": "fashion/",
        "#case-winline": "winline/",
        "#cases": "",
      };
      if (!Object.hasOwn(oldRoute, location.hash)) return;
      const directory = home ? "cases/" : "./";
      location.replace(
        new URL(directory + oldRoute[location.hash], document.baseURI),
      );
    };
    moveCaseBookmark();
    window.addEventListener("hashchange", moveCaseBookmark);
  }
  if (home) {
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
  }

  const film = home?.querySelector("[data-line-src]");
  if (film && "IntersectionObserver" in window && film.canPlayType("video/mp4")) {
    const narrowFrame = matchMedia("(max-width: 600px)");
    let inView = false;
    const syncFilm = () => {
      const still = reducedMotion.matches || navigator.connection?.saveData;
      if (still || !inView || document.hidden) {
        film.pause();
        if (still) film.classList.remove("is-ready");
        return;
      }
      const src = narrowFrame.matches ? film.dataset.lineMobile : film.dataset.lineSrc;
      if (film.getAttribute("src") !== src) {
        film.classList.remove("is-ready");
        film.src = src;
      }
      if (!film.ended) film.play().catch(() => {});
    };
    film.addEventListener("playing", () => film.classList.add("is-ready"));
    film.addEventListener("error", () => film.classList.remove("is-ready"));
    new IntersectionObserver(([entry]) => {
      inView = entry.isIntersecting;
      syncFilm();
    }).observe(film);
    narrowFrame.addEventListener("change", syncFilm);
    reducedMotion.addEventListener("change", syncFilm);
    document.addEventListener("visibilitychange", syncFilm);
  }

  function updateHeader() {
    header.classList.toggle("is-scrolled", scrollY > 16);
  }
  updateHeader();
  window.addEventListener("scroll", updateHeader, { passive: true });

  // Preserve native details for keyboard activation and for browsers without animations.
  for (const entry of document.querySelectorAll(".question-list details")) {
    const panel = entry.querySelector(".faq-answer");
    let animation;
    let expanding;
    entry.querySelector("summary").addEventListener("click", (event) => {
      if (!panel.animate || reducedMotion.matches) return;
      event.preventDefault();
      expanding = animation ? !expanding : !entry.open;
      const from = entry.open ? panel.getBoundingClientRect().height : 0;
      animation?.cancel();
      entry.open = true;
      const to = expanding ? panel.scrollHeight : 0;
      animation = panel.animate(
        [{ height: from + "px" }, { height: to + "px" }],
        { duration: 260, easing: "cubic-bezier(.22,.75,.23,1)" },
      );
      animation.onfinish = () => {
        entry.open = expanding;
        animation = null;
      };
    });
    reducedMotion.addEventListener("change", () => {
      if (reducedMotion.matches) animation?.finish();
    });
  }

  for (const reader of document.querySelectorAll(".slide-reader")) {
    const track = reader.querySelector(".slide-track");
    const controls = reader.querySelector(".deck-controls");
    const previous = controls.querySelector("[data-back]");
    const next = controls.querySelector("[data-next]");
    const count = track.children.length;
    let index = 0;
    let target = null;
    function setIndex(value) {
      index = value;
      controls.querySelector("output").value = value + 1 + " / " + count;
      previous.disabled = value === 0;
      next.disabled = value === count - 1;
    }
    function go(value, smooth = true) {
      target = Math.max(0, Math.min(value, count - 1));
      setIndex(target);
      track.scrollTo({
        left: target * track.clientWidth,
        behavior: smooth && !reducedMotion.matches ? "smooth" : "instant",
      });
    }
    previous.addEventListener("click", () => go(index - 1));
    next.addEventListener("click", () => go(index + 1));
    track.addEventListener("keydown", (e) => {
      if (!["ArrowLeft", "ArrowRight", "Home", "End"].includes(e.key)) return;
      e.preventDefault();
      if (e.key === "Home") go(0);
      else if (e.key === "End") go(count - 1);
      else go(index + (e.key === "ArrowRight" ? 1 : -1));
    });
    for (const name of ["pointerdown", "wheel", "focusin"]) {
      track.addEventListener(
        name,
        () => {
          target = null;
        },
        { passive: true },
      );
    }
    track.addEventListener(
      "scroll",
      () => {
        const current = Math.round(track.scrollLeft / track.clientWidth);
        if (target !== null && current !== target) return;
        target = null;
        if (current !== index) setIndex(current);
      },
      { passive: true },
    );
    let width = track.clientWidth;
    if ("ResizeObserver" in window)
      new ResizeObserver(() => {
        if (width === track.clientWidth) return;
        width = track.clientWidth;
        go(index, false);
      }).observe(track);
    controls.hidden = false;
    setIndex(0);
  }

  if (!("IntersectionObserver" in window)) return;
  const observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        entry.target.classList.add("in-view");
        observer.unobserve(entry.target);
      }
    },
    { threshold: 0.16 },
  );
  document
    .querySelectorAll(
      ".service-figure, .project-intro, .slide-reader, .decision-path",
    )
    .forEach((el) => observer.observe(el));
})();
