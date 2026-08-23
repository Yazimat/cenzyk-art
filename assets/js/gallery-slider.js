(function () {
  var root = document.querySelector("[data-gallery-slider]");
  if (!root) return;

  var track = root.querySelector(".gallery-track");
  var slides = Array.prototype.slice.call(root.querySelectorAll(".gallery-slide"));
  var prev = root.querySelector(".gallery-prev");
  var next = root.querySelector(".gallery-next");
  var dotsWrap = root.querySelector(".gallery-dots");
  if (!track || !slides.length) return;

  var index = 0;
  var startX = 0;
  var deltaX = 0;
  var dragging = false;

  function renderDots() {
    if (!dotsWrap) return;
    dotsWrap.innerHTML = "";
    slides.forEach(function (_, i) {
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "gallery-dot" + (i === index ? " is-active" : "");
      btn.setAttribute("aria-label", "Фото " + (i + 1));
      btn.addEventListener("click", function () {
        go(i);
      });
      dotsWrap.appendChild(btn);
    });
  }

  function go(i) {
    index = (i + slides.length) % slides.length;
    track.style.transform = "translateX(" + -index * 100 + "%)";
    slides.forEach(function (slide, n) {
      slide.classList.toggle("is-active", n === index);
    });
    if (dotsWrap) {
      Array.prototype.forEach.call(dotsWrap.children, function (dot, n) {
        dot.classList.toggle("is-active", n === index);
      });
    }
  }

  if (prev) prev.addEventListener("click", function () { go(index - 1); });
  if (next) next.addEventListener("click", function () { go(index + 1); });

  root.addEventListener("keydown", function (e) {
    if (e.key === "ArrowLeft") go(index - 1);
    if (e.key === "ArrowRight") go(index + 1);
  });
  root.setAttribute("tabindex", "0");

  root.addEventListener("touchstart", function (e) {
    if (!e.touches || !e.touches.length) return;
    dragging = true;
    startX = e.touches[0].clientX;
    deltaX = 0;
  }, { passive: true });

  root.addEventListener("touchmove", function (e) {
    if (!dragging || !e.touches || !e.touches.length) return;
    deltaX = e.touches[0].clientX - startX;
  }, { passive: true });

  root.addEventListener("touchend", function () {
    if (!dragging) return;
    dragging = false;
    if (Math.abs(deltaX) > 40) {
      go(index + (deltaX < 0 ? 1 : -1));
    }
  });

  renderDots();
  go(0);
})();
