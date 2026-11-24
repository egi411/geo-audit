(() => {
  "use strict";
  // Page zoom changes CSS viewport width and pixel density in inverse proportion.
  // Track that change separately from window resizing and pinch zoom.
  const displayKey = "aileed:display-zoom";
  let density = window.devicePixelRatio || 1;
  let width = window.innerWidth;
  let magnification = 1;
  try {
    const saved = JSON.parse(sessionStorage.getItem(displayKey));
    if (saved?.density === density && Number.isFinite(saved.factor) && saved.factor > 0) {
      magnification = saved.factor;
    }
  } catch { /* A blocked store still allows zoom during this visit. */ }

  function updateDisplayScale() {
    const nextDensity = window.devicePixelRatio || 1;
    const nextWidth = window.innerWidth;
    if (density !== nextDensity) {
      const sameWindowWidth = Math.abs(width * density - nextWidth * nextDensity) <= Math.max(density, nextDensity) * 2;
      magnification = sameWindowWidth ? magnification * nextDensity / density : 1;
      if (Math.abs(magnification - 1) < .005) magnification = 1;
      try {
        if (magnification === 1) sessionStorage.removeItem(displayKey);
        else sessionStorage.setItem(displayKey, JSON.stringify({density: nextDensity, factor: magnification}));
      } catch { /* No storage is needed for the current document. */ }
    }
    width = nextWidth;
    density = nextDensity;
    const root = document.documentElement.style;
    if (magnification === 1) {
      root.removeProperty("--layout-vw");
      root.removeProperty("--layout-vh");
    } else {
      root.setProperty("--layout-vw", (width * magnification / 100) + "px");
      root.setProperty("--layout-vh", (window.innerHeight * magnification / 100) + "px");
    }
  }
  updateDisplayScale();
  window.addEventListener("resize", updateDisplayScale, {passive: true});
  window.addEventListener("pageshow", updateDisplayScale);

  const menu = document.querySelector(".menu-toggle");
  const navigation = document.querySelector(".nav-links");
  function closeMenu() {
    navigation.classList.remove("open");
    menu.setAttribute("aria-expanded", "false");
    menu.setAttribute("aria-label", "Открыть меню");
  }
  menu?.addEventListener("click", () => {
    const open = menu.getAttribute("aria-expanded") !== "true";
    navigation.classList.toggle("open", open);
    menu.setAttribute("aria-expanded", String(open));
    menu.setAttribute("aria-label", open ? "Закрыть меню" : "Открыть меню");
  });
  navigation?.addEventListener("click", (e) => {
    if (e.target.closest("a")) closeMenu();
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && navigation?.classList.contains("open")) {
      closeMenu();
      menu.focus();
    }
  });
  const desktop = matchMedia("(min-width:769px)");
  desktop.addEventListener("change", closeMenu);
  if (
    "IntersectionObserver" in window &&
    !matchMedia("(prefers-reduced-motion:reduce)").matches
  ) {
    const observer = new IntersectionObserver(
      (entries) =>
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("visible");
            observer.unobserve(entry.target);
          }
        }),
      { threshold: 0.08 },
    );
    document.querySelectorAll(".reveal").forEach((el) => observer.observe(el));
    document.documentElement.classList.add("motion-enabled");
  }
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
  document.querySelector(".buyer-controls")?.addEventListener("change", (event) => {
    const active = document.querySelector('[data-buyer="' + event.target.value + '"] figcaption');
    keepAnswerVisible(active);
  });
  document.querySelector(".sample-choices")?.addEventListener("change", (event) => {
    const active = document.querySelector('[data-variant="' + event.target.value + '"] blockquote');
    keepAnswerVisible(active);
  });
  const dialog = document.getElementById("brief-dialog");
  let trigger;
  document.querySelectorAll("[data-open-brief]").forEach((button) =>
    button.addEventListener("click", (event) => {
      if (!dialog || typeof dialog.showModal !== "function") return;
      event.preventDefault();
      trigger = button;
      dialog.showModal();
    }),
  );
  dialog
    ?.querySelector(".dialog-close")
    .addEventListener("click", () => dialog.close());
  dialog?.addEventListener("click", (e) => {
    if (e.target === dialog) {
      const r = dialog.getBoundingClientRect();
      if (
        e.clientX < r.left ||
        e.clientX > r.right ||
        e.clientY < r.top ||
        e.clientY > r.bottom
      )
        dialog.close();
    }
  });
  dialog?.addEventListener("close", () => trigger?.focus());
})();
