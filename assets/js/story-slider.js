(() => {
  const THRESHOLD = 40;

  window.initStorySlider = (root) => {
    if (!root || root.dataset.storyReady === "1") return;
    root.dataset.storyReady = "1";

    const frame = root.querySelector(".story-frame") || root;
    const track = root.querySelector(".story-track");
    const slides = Array.prototype.slice.call(root.querySelectorAll(".story-slide"));
    const bars = Array.prototype.slice.call(root.querySelectorAll(".story-bars i"));
    const live = root.querySelector("[data-story-live]");
    const prevBtn = root.querySelector("[data-story-dir='-1']");
    const nextBtn = root.querySelector("[data-story-dir='1']");
    if (!track || !slides.length) return;

    let index = 0;
    let startX = 0;
    let deltaX = 0;
    let dragging = false;
    let swiped = false;

    const render = () => {
      track.style.transform = `translateX(${-index * 100}%)`;
      slides.forEach((slide, n) => {
        slide.classList.toggle("is-active", n === index);
        slide.setAttribute("aria-hidden", n === index ? "false" : "true");
      });
      bars.forEach((bar, n) => {
        bar.classList.toggle("is-done", n < index);
        bar.classList.toggle("is-current", n === index);
      });
      root.setAttribute("data-story-index", String(index));
      root.classList.toggle("is-first", index === 0);
      root.classList.toggle("is-last", index === slides.length - 1);
      if (prevBtn) prevBtn.hidden = index === 0;
      if (nextBtn) nextBtn.hidden = index === slides.length - 1;
      if (live) {
        live.textContent = `Кадр ${index + 1} из ${slides.length}`;
      }
    };

    const go = (i) => {
      index = Math.max(0, Math.min(slides.length - 1, i));
      render();
    };

    const fromPoint = (clientX) => {
      const rect = frame.getBoundingClientRect();
      const x = clientX - rect.left;
      if (x < rect.width * 0.32) go(index - 1);
      else go(index + 1);
    };

    prevBtn?.addEventListener("click", (e) => {
      e.stopPropagation();
      go(index - 1);
    });
    nextBtn?.addEventListener("click", (e) => {
      e.stopPropagation();
      go(index + 1);
    });

    frame.addEventListener("click", (e) => {
      if (e.target.closest("a, button")) return;
      if (swiped) {
        swiped = false;
        return;
      }
      fromPoint(e.clientX);
    });

    root.addEventListener("keydown", (e) => {
      if (e.key === "ArrowLeft") {
        e.preventDefault();
        go(index - 1);
      }
      if (e.key === "ArrowRight") {
        e.preventDefault();
        go(index + 1);
      }
    });
    if (!root.hasAttribute("tabindex")) root.setAttribute("tabindex", "0");

    frame.addEventListener("touchstart", (e) => {
      if (!e.touches || !e.touches.length) return;
      dragging = true;
      swiped = false;
      startX = e.touches[0].clientX;
      deltaX = 0;
    }, { passive: true });

    frame.addEventListener("touchmove", (e) => {
      if (!dragging || !e.touches || !e.touches.length) return;
      deltaX = e.touches[0].clientX - startX;
    }, { passive: true });

    frame.addEventListener("touchend", () => {
      if (!dragging) return;
      dragging = false;
      if (Math.abs(deltaX) > THRESHOLD) {
        swiped = true;
        go(index + (deltaX < 0 ? 1 : -1));
      }
    });

    render();
  };
})();
