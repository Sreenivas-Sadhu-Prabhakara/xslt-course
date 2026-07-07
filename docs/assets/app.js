/* Progressive enhancement only — the site is fully readable without JS. */
(function () {
  "use strict";

  // Mobile nav toggle
  var btn = document.querySelector(".menu-btn");
  var navWrap = document.querySelector(".nav-wrap");
  if (btn && navWrap) {
    btn.addEventListener("click", function () {
      var open = navWrap.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  // Copy buttons on code panels
  document.querySelectorAll(".copy").forEach(function (b) {
    b.addEventListener("click", function () {
      var panel = b.closest(".panel");
      var pre = panel && panel.querySelector("pre");
      if (!pre) return;
      navigator.clipboard.writeText(pre.innerText).then(function () {
        var old = b.textContent;
        b.textContent = "copied";
        setTimeout(function () { b.textContent = old; }, 1200);
      });
    });
  });

  // Hero transform reveal — one orchestrated moment, motion-safe
  var hero = document.querySelector("[data-hero]");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (hero && !reduce) {
    hero.classList.add("hero-armed");
    requestAnimationFrame(function () {
      requestAnimationFrame(function () { hero.classList.add("hero-run"); });
    });
  }
})();
