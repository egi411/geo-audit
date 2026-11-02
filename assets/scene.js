(() => {
  "use strict";
  const scene = document.querySelector(".hero-scene");
  const elements = [
    ...document.querySelectorAll(
      ".hero-scene,.source-sculpture,.audit-sculpture,.offer-object",
    ),
  ];
  if (!elements.length) return;
  const reduced = matchMedia("(prefers-reduced-motion: reduce)");
  const visible = new Map(
    elements.map((el) => [el, !("IntersectionObserver" in window)]),
  );
  let frame = 0;
  function refresh() {
    elements.forEach((el) => {
      const active = visible.get(el) && !document.hidden && !reduced.matches;
      el.classList.toggle("motion-in-view", active);
      if (el === scene) el.classList.toggle("scene-active", active);
    });
  }
  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) =>
        visible.set(entry.target, entry.isIntersecting),
      );
      refresh();
    });
    elements.forEach((el) => observer.observe(el));
  }
  window.addEventListener(
    "pointermove",
    (event) => {
      if (
        !scene ||
        event.pointerType !== "mouse" ||
        !visible.get(scene) ||
        document.hidden ||
        reduced.matches ||
        frame
      )
        return;
      frame = requestAnimationFrame(() => {
        scene.style.setProperty(
          "--rx",
          `${(event.clientY / innerHeight - 0.5) * -5}deg`,
        );
        scene.style.setProperty(
          "--ry",
          `${(event.clientX / innerWidth - 0.5) * 7}deg`,
        );
        frame = 0;
      });
    },
    { passive: true },
  );
  reduced.addEventListener("change", () => {
    scene?.style.removeProperty("--rx");
    scene?.style.removeProperty("--ry");
    refresh();
  });
  document.addEventListener("visibilitychange", refresh);
  refresh();
})();
