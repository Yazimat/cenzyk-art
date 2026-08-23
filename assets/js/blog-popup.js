(() => {
  const bindPopups = (root, openAttr, tplPrefix) => {
    const dialog = root.querySelector(".blog-popup");
    const panel = root.querySelector(".blog-popup-panel");
    const closeBtn = root.querySelector(".blog-popup-close");
    if (!dialog || !panel) return;

    let lastFocus = null;

    const open = (id) => {
      const tpl = document.getElementById(`${tplPrefix}${id}`);
      if (!tpl) return;
      if (dialog.hidden) lastFocus = document.activeElement;
      panel.innerHTML = "";
      panel.appendChild(tpl.content.cloneNode(true));
      panel.scrollTop = 0;
      panel.querySelectorAll("[data-story-slider]").forEach((el) => {
        window.initStorySlider?.(el);
      });
      dialog.hidden = false;
      dialog.setAttribute("aria-hidden", "false");
      document.body.classList.add("blog-popup-open");
      closeBtn?.focus();
    };

    const close = () => {
      if (dialog.hidden) return;
      dialog.hidden = true;
      dialog.setAttribute("aria-hidden", "true");
      document.body.classList.remove("blog-popup-open");
      panel.innerHTML = "";
      if (lastFocus && typeof lastFocus.focus === "function") lastFocus.focus();
    };

    root.addEventListener("click", (e) => {
      const btn = e.target.closest(`[${openAttr}]`);
      if (btn) {
        e.preventDefault();
        open(btn.getAttribute(openAttr));
        return;
      }
      if (e.target.closest("[data-blog-close]")) {
        e.preventDefault();
        close();
        return;
      }
      const go = e.target.closest("[data-blog-goto]");
      if (go) {
        e.preventDefault();
        const id = go.getAttribute("data-blog-goto");
        close();
        window.setTimeout(() => {
          document.getElementById(id)?.scrollIntoView({ behavior: "smooth", block: "start" });
        }, 40);
      }
    });

    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") close();
    });
  };

  document.querySelectorAll("[data-blog-popups]").forEach((root) => {
    bindPopups(root, "data-blog-open", "blog-popup-");
  });
  document.querySelectorAll("[data-case-popups]").forEach((root) => {
    bindPopups(root, "data-case-open", "case-popup-");
  });
})();
