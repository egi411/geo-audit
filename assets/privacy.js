(() => {
  "use strict";
  const banner = document.getElementById("cookie-banner");
  if (!banner) return;
  const key = "aileeds:privacy-choice:v1";
  const lifetime = 180 * 24 * 60 * 60 * 1000;
  let trigger;
  let saved = false;
  try {
    const choice = JSON.parse(localStorage.getItem(key));
    saved =
      choice?.choice === "necessary" &&
      Number.isFinite(choice.at) &&
      Date.now() >= choice.at &&
      Date.now() - choice.at < lifetime;
  } catch {
    /* A blocked store does not prevent the page from working. */
  }
  banner.hidden = saved;
  document.querySelectorAll("[data-cookie-settings]").forEach((button) => {
    button.addEventListener("click", () => {
      trigger = button;
      banner.hidden = false;
      banner
        .querySelector("[data-cookie-accept]")
        .focus({ preventScroll: true });
    });
  });
  banner.querySelector("[data-cookie-accept]").addEventListener("click", () => {
    try {
      localStorage.setItem(
        key,
        JSON.stringify({ choice: "necessary", at: Date.now() }),
      );
    } catch {
      /* The current notice still closes without storage. */
    }
    banner.hidden = true;
    trigger?.focus({ preventScroll: true });
    trigger = undefined;
  });
})();
