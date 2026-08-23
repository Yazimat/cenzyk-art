(() => {
  const bindPopups = (clickRoot, openAttr, tplPrefix, popupRoot = clickRoot) => {
    const dialog = popupRoot.querySelector(".blog-popup");
    const panel = popupRoot.querySelector(".blog-popup-panel");
    const closeBtn = popupRoot.querySelector(".blog-popup-close");
    if (!dialog || !panel) return null;

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

    clickRoot.addEventListener("click", (e) => {
      const btn = e.target.closest(`[${openAttr}]`);
      if (btn) {
        e.preventDefault();
        open(btn.getAttribute(openAttr));
        return;
      }
      if (e.target.closest("[data-blog-close]") && !dialog.hidden) {
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
      if (e.key === "Escape" && !dialog.hidden) close();
    });

    return { open, close };
  };

  document.querySelectorAll("[data-blog-popups]").forEach((root) => {
    bindPopups(root, "data-blog-open", "blog-popup-");
  });
  document.querySelectorAll("[data-case-popups]").forEach((root) => {
    bindPopups(root, "data-case-open", "case-popup-");
  });

  const d3Root = document.querySelector("[data-3d-popups]");
  const d3 = d3Root ? bindPopups(document, "data-3d-open", "popup-3d-", d3Root) : null;

  if (d3) {
    const params = new URLSearchParams(window.location.search);
    if (params.get("3d") === "1" || window.location.hash === "#3d") {
      window.setTimeout(() => d3.open("primerka"), 60);
    }
  }
})();
