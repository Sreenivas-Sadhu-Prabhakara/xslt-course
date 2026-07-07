/* Progressive enhancement for the XSLT course (themed like the Apigee family):
   copy buttons, mobile nav, reading bar, "On this page" spy, and localStorage
   progress (sidebar meter + per-lesson "mark complete"). Fully readable w/o JS. */
(function () {
  "use strict";
  var KEY = "xslt.progress.v1";
  var TOTAL = document.querySelectorAll(".sidebar li[data-idx]").length || 14;

  function getDone() { try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) { return []; } }
  function setDone(a) {
    a = a.filter(function (v, i, s) { return s.indexOf(v) === i; }).sort(function (x, y) { return x - y; });
    try { localStorage.setItem(KEY, JSON.stringify(a)); } catch (e) {}
    return a;
  }

  // Copy buttons (markup already present as .copy inside each code panel)
  document.querySelectorAll(".copy").forEach(function (b) {
    b.addEventListener("click", function () {
      var pre = b.closest(".panel") && b.closest(".panel").querySelector("pre");
      if (!pre) return;
      navigator.clipboard.writeText(pre.innerText).then(function () {
        b.textContent = "copied"; b.classList.add("copied");
        setTimeout(function () { b.textContent = "copy"; b.classList.remove("copied"); }, 1300);
      });
    });
  });

  // Mobile nav
  var toggle = document.getElementById("navToggle");
  if (toggle) toggle.addEventListener("click", function () { document.body.classList.toggle("nav-open"); });
  document.querySelectorAll(".sidebar a").forEach(function (a) {
    a.addEventListener("click", function () { document.body.classList.remove("nav-open"); });
  });

  // Progress meter + completion ticks
  function refresh() {
    var done = getDone();
    document.querySelectorAll(".sidebar li[data-idx]").forEach(function (li) {
      li.classList.toggle("completed", done.indexOf(+li.getAttribute("data-idx")) >= 0);
    });
    var fill = document.getElementById("navProgressFill");
    var text = document.getElementById("navProgressText");
    if (fill) fill.style.width = Math.round((done.length / TOTAL) * 100) + "%";
    if (text) text.textContent = done.length + " / " + TOTAL + " complete";
  }
  refresh();

  // "Mark complete" on a lesson page
  var btn = document.getElementById("markComplete");
  var main = document.querySelector("main[data-idx]");
  if (btn && main) {
    var idx = +main.getAttribute("data-idx");
    var sync = function () {
      var isDone = getDone().indexOf(idx) >= 0;
      btn.parentNode.classList.toggle("is-done", isDone);
      btn.childNodes[btn.childNodes.length - 1].nodeValue = isDone ? " Lesson complete" : " Mark lesson complete";
    };
    btn.addEventListener("click", function () {
      var done = getDone(), i = done.indexOf(idx);
      if (i >= 0) done.splice(i, 1); else done.push(idx);
      setDone(done); refresh(); sync();
    });
    sync();
  }

  // Reading-progress bar
  var bar = document.getElementById("readingBar");
  if (bar) {
    var onScroll = function () {
      var h = document.documentElement, b = document.body;
      var st = h.scrollTop || b.scrollTop;
      var sh = (h.scrollHeight || b.scrollHeight) - h.clientHeight;
      bar.style.width = (sh > 0 ? (st / sh) * 100 : 0) + "%";
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  // "On this page" active highlight
  var links = Array.prototype.slice.call(document.querySelectorAll(".toc-rail a"));
  if (links.length) {
    var targets = links.map(function (a) { return document.getElementById(decodeURIComponent(a.getAttribute("href").slice(1))); });
    var spy = function () {
      var pos = window.scrollY + 120, idx = 0;
      for (var i = 0; i < targets.length; i++) if (targets[i] && targets[i].offsetTop <= pos) idx = i;
      links.forEach(function (a, i) { a.classList.toggle("active", i === idx); });
    };
    window.addEventListener("scroll", spy, { passive: true });
    spy();
  }
})();
