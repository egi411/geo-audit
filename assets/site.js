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
})();
