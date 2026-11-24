(() => {
  const header = document.querySelector(".site-header");
  function scrollHeader() {
    header.classList.toggle("is-scrolled", window.scrollY > 16);
  }
  scrollHeader();
  window.addEventListener("scroll", scrollHeader, { passive: true });

  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)");
  // The plot is fully rendered in HTML, including its totals and legend.
  function setup(board) {
    const series = JSON.parse(board.dataset.counts);
    const range = board.querySelector("input[type=range]");
    const total = Number(range.max);
    const outputs = [...board.querySelectorAll("[data-count]")];
    const bases = [
      ...board.querySelectorAll("[data-base]"),
      board.querySelector("[data-position]"),
    ];
    let frame = 0;
    let position = total;
    let played = false;

    function render(value) {
      position = value;
      const key = board.querySelector("input[type=radio]:checked").value;
      const percent = (value / total) * 100;
      board.style.setProperty("--seek", percent + "%");
      board.style.setProperty(
        "--remaining",
        value === total ? "-3px" : 100 - percent + "%",
      );
      board.style.setProperty(
        "--level",
        (series[key][value] / total) * 100 + "%",
      );
      outputs.forEach((el) => {
        el.value = series[el.dataset.count][value];
      });
      bases.forEach((el) => {
        el.textContent = value;
      });
      range.value = value;
      range.setAttribute("aria-valuetext", value + " из " + total);
    }
    function stop() {
      cancelAnimationFrame(frame);
      frame = 0;
    }
    function complete() {
      stop();
      render(total);
    }
    function play() {
      if (played || reduced.matches || document.hidden) return;
      played = true;
      const start = performance.now();
      function step(time) {
        const value = Math.min(
          total,
          1 + Math.floor((Math.max(0, time - start) * total) / 1100),
        );
        if (value !== position) render(value);
        frame = value < total ? requestAnimationFrame(step) : 0;
      }
      frame = requestAnimationFrame(step);
    }
    board.dataset.ready = "";
    render(total);
    board.addEventListener("input", () => {
      played = true;
      stop();
      render(Number(range.value));
    });
    if ("IntersectionObserver" in window) {
      const observer = new IntersectionObserver(
        ([entry]) => {
          if (entry.isIntersecting) play();
          else if (frame) complete();
        },
        { threshold: 0.28 },
      );
      observer.observe(board);
    }
    reduced.addEventListener("change", () => {
      if (frame && reduced.matches) complete();
    });
    document.addEventListener("visibilitychange", () => {
      if (frame && document.hidden) complete();
    });
  }
  document.querySelectorAll("[data-dashboard]").forEach(setup);
  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      (entries) =>
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("in-view");
          observer.unobserve(entry.target);
        }),
      { threshold: 0.2 },
    );
    document
      .querySelectorAll(".frequency-paper,.observation-plate")
      .forEach((el) => observer.observe(el));
  }
})();
