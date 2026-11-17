(() => {
  "use strict";
  const banner = document.getElementById("cookie-banner");
  if (!banner) return;
  const key = "aileed:privacy-choice:v1";
  const lifetime = 180 * 24 * 60 * 60 * 1000;
  let trigger;
  let saved = false;
  try {
    const raw = localStorage.getItem(key) || localStorage.getItem("aileeds:privacy-choice:v1");
    const choice = JSON.parse(raw);
    saved = choice?.choice === "necessary" && Number.isFinite(choice.at) && Date.now() >= choice.at && Date.now() - choice.at < lifetime;
  } catch { /* The notice works even with unavailable storage. */ }
  banner.hidden = saved;
  document.querySelectorAll("[data-cookie-settings]").forEach(button => button.addEventListener("click", () => {
    trigger = button;
    banner.hidden = false;
    banner.scrollIntoView({block:"center",behavior:"instant"});
    banner.querySelector("[data-cookie-accept]").focus({preventScroll:true});
  }));
  banner.querySelector("[data-cookie-accept]").addEventListener("click", () => {
    try { localStorage.setItem(key, JSON.stringify({choice:"necessary",at:Date.now()})); } catch { /* Still close for this visit. */ }
    banner.hidden = true;
    trigger?.focus({preventScroll:true}); trigger = undefined;
  });
})();
