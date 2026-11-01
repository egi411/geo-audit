(() => {
  "use strict";
  const scene = document.querySelector(".hero-scene");
  if (!scene) return;
  const reduced = matchMedia("(prefers-reduced-motion: reduce)");
  let visible = true,
    frame = 0;
  const active = () =>
    scene.classList.toggle(
      "scene-active",
      visible && !document.hidden && !reduced.matches,
    );
  if ("IntersectionObserver" in window) {
    new IntersectionObserver((entries) => {
      visible = entries[0].isIntersecting;
      active();
    }).observe(scene);
  }
  window.addEventListener(
    "pointermove",
    (event) => {
      if (
        event.pointerType !== "mouse" ||
        !visible ||
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
    scene.style.removeProperty("--rx");
    scene.style.removeProperty("--ry");
    active();
  });
  document.addEventListener("visibilitychange", active);
  active();
})();
