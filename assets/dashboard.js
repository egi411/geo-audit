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
      ".service-figure, .project-intro, .recommendation-map",
    )
    .forEach((el) => observer.observe(el));
})();
