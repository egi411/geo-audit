(() => {
  "use strict";
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
  const scenarios = [
    [
      "Можно рассмотреть <strong>компанию А</strong> и <strong>компанию Б</strong>. У них есть подробные описания решений и материалы по вашей задаче.",
      "Вашего бренда нет в рекомендации.",
      "Нет упоминания → нет шанса участвовать в выборе.",
    ],
    [
      "<strong>Ваш бренд</strong> тоже может подойти. По доступным сведениям, он работает только с крупными компаниями.",
      "Но вы работаете и с небольшими командами.",
      "Ошибка в фактах → клиент может исключить вас из выбора.",
    ],
    [
      "<strong>Ваш бренд</strong> стоит рассмотреть: у него есть решение для небольших команд, а на сайте подробно описаны условия и сценарии применения.",
      "Точное описание. Понятные причины рассмотреть бренд.",
      "К такому представлению стремимся. Ответы ИИ не гарантируются.",
    ],
  ];
  document.querySelectorAll("[data-scenario]").forEach((button) =>
    button.addEventListener("click", () => {
      document
        .querySelectorAll("[data-scenario]")
        .forEach((b) => b.setAttribute("aria-pressed", String(b === button)));
      const [body, brand, foot] = scenarios[Number(button.dataset.scenario)];
      const content = document.querySelector(".answer-content");
      content.querySelector(".answer-body").innerHTML = body;
      content.querySelector(".answer-brand").textContent = brand;
      content.querySelector(".answer-foot").textContent = foot;
    }),
  );
  const tabs = [...document.querySelectorAll("[role=tab]")];
  function selectTab(tab) {
    tabs.forEach((t) => {
      const active = t === tab;
      t.setAttribute("aria-selected", String(active));
      t.tabIndex = active ? 0 : -1;
      document.getElementById(t.getAttribute("aria-controls")).hidden = !active;
    });
  }
  tabs.forEach((tab, index) => {
    tab.addEventListener("click", () => selectTab(tab));
    tab.addEventListener("keydown", (e) => {
      let next;
      if (e.key === "ArrowRight") next = (index + 1) % tabs.length;
      if (e.key === "ArrowLeft") next = (index + tabs.length - 1) % tabs.length;
      if (e.key === "Home") next = 0;
      if (e.key === "End") next = tabs.length - 1;
      if (next !== undefined) {
        e.preventDefault();
        selectTab(tabs[next]);
        tabs[next].focus();
      }
    });
  });
  const dialog = document.getElementById("brief-dialog");
  let trigger;
  document.querySelectorAll("[data-open-brief]").forEach((button) =>
    button.addEventListener("click", () => {
      trigger = button;
      dialog.querySelector("[name=service]").value = location.pathname.includes(
        "/audit/",
      )
        ? "GEO-аудит"
        : "GEO-продвижение";
      dialog.querySelector(".brief-status").textContent = "";
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
  dialog?.querySelector("form").addEventListener("submit", (e) => {
    e.preventDefault();
    const form = e.currentTarget;
    const brand = form.elements.brand;
    if (!brand.value.trim()) {
      brand.setCustomValidity("Укажите бренд или сайт");
      brand.reportValidity();
      return;
    }
    brand.setCustomValidity("");
    const data = new FormData(form);
    const text = `Бриф / AiLeeds\n\nБренд или сайт: ${data.get("brand").trim()}\nУслуга: ${data.get("service")}\nАудитория: ${data.get("audience").trim() || "—"}\nЗадача и конкуренты: ${data.get("task").trim() || "—"}\n\nФайл подготовлен локально. Данные не отправлены.\n`;
    const url = URL.createObjectURL(
      new Blob(["\ufeff", text], { type: "text/plain;charset=utf-8" }),
    );
    const link = document.createElement("a");
    link.href = url;
    link.download = "aileeds-brief.txt";
    document.body.append(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 15000);
    dialog.querySelector(".brief-status").textContent =
      "Бриф подготовлен к скачиванию. Данные не отправлены.";
  });
  dialog
    ?.querySelector("[name=brand]")
    .addEventListener("input", (e) => e.target.setCustomValidity(""));
})();
