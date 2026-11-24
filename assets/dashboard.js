(() => {
  const header = document.querySelector(".site-header");
  function updateHeader() {
    header.classList.toggle("is-scrolled", window.scrollY > 16);
  }
  updateHeader();
  window.addEventListener("scroll", updateHeader, { passive: true });

  // The charts, labels and switching work in the static page. Animate only on entry.
  if (!("IntersectionObserver" in window)) return;
  const cases = document.getElementById("cases");
  if (cases) {
    const caseLink = header.querySelector("[data-cases-link]");
    const homeLink = header.querySelector('[aria-current="page"]');
    new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          homeLink.removeAttribute("aria-current");
          caseLink.setAttribute("aria-current", "location");
        } else {
          homeLink.setAttribute("aria-current", "page");
          caseLink.removeAttribute("aria-current");
        }
      },
      { rootMargin: "-10% 0px -48%" },
    ).observe(cases);
  }
  const observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        entry.target.classList.add("in-view");
        observer.unobserve(entry.target);
      }
    },
    { threshold: 0.18 },
  );
  document
    .querySelectorAll(".instrument, .compare-plot")
    .forEach((el) => observer.observe(el));
})();
