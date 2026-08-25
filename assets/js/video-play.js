(() => {
  const enhance = (root = document) => {
    root.querySelectorAll(".bp-video").forEach((wrap) => {
      if (wrap.dataset.playReady === "1") return;
      wrap.dataset.playReady = "1";

      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "bp-video-play";
      btn.setAttribute("aria-label", "Смотреть видео");
      wrap.appendChild(btn);

      const start = () => {
        const video = wrap.querySelector("video");
        const iframe = wrap.querySelector("iframe");
        if (video) {
          const playPromise = video.play();
          if (playPromise && typeof playPromise.catch === "function") {
            playPromise.catch(() => {});
          }
          wrap.classList.add("is-playing");
          return;
        }
        if (iframe) {
          let src = iframe.getAttribute("src") || "";
          if (!/[?&]autoplay=1(?:&|$)/.test(src)) {
            src += (src.includes("?") ? "&" : "?") + "autoplay=1";
            iframe.setAttribute("src", src);
          }
          wrap.classList.add("is-playing");
        }
      };

      btn.addEventListener("click", (e) => {
        e.preventDefault();
        e.stopPropagation();
        start();
      });

      const video = wrap.querySelector("video");
      if (video) {
        video.addEventListener("play", () => wrap.classList.add("is-playing"));
        video.addEventListener("pause", () => {
          if (video.paused) wrap.classList.remove("is-playing");
        });
        video.addEventListener("ended", () => wrap.classList.remove("is-playing"));
      }
    });
  };

  window.enhanceVideoPlays = enhance;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => enhance());
  } else {
    enhance();
  }
})();
