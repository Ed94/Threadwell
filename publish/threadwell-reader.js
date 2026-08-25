(() => {
  const WIDE_KEY = "threadwell-wide";

  function articleRoot() {
    return document.querySelector("article");
  }

  function setWide(on) {
    document.body.classList.toggle("threadwell-wide", on);
    try {
      localStorage.setItem(WIDE_KEY, on ? "1" : "0");
    } catch (_err) {
      /* ignore */
    }
    const btn = document.getElementById("threadwell-wide");
    if (btn) {
      btn.setAttribute("aria-pressed", on ? "true" : "false");
      btn.textContent = on ? "Narrow" : "Wide";
    }
  }

  function addWideButton() {
    if (document.getElementById("threadwell-wide")) {
      return;
    }
    const btn = document.createElement("button");
    btn.id = "threadwell-wide";
    btn.type = "button";
    btn.className = "threadwell-wide-btn";
    btn.textContent = "Wide";
    btn.addEventListener("click", () => {
      setWide(!document.body.classList.contains("threadwell-wide"));
    });
    document.body.appendChild(btn);
    try {
      if (localStorage.getItem(WIDE_KEY) === "1") {
        setWide(true);
      }
    } catch (_err) {
      /* ignore */
    }
  }

  function closeZoom() {
    const overlay = document.getElementById("threadwell-zoom");
    if (overlay) {
      overlay.remove();
    }
  }

  function openZoom(src) {
    closeZoom();
    const overlay = document.createElement("div");
    overlay.id = "threadwell-zoom";
    overlay.className = "threadwell-zoom";
    const img = document.createElement("img");
    img.src = src;
    img.alt = "";
    overlay.appendChild(img);
    overlay.addEventListener("click", closeZoom);
    document.body.appendChild(overlay);
  }

  function onArticleClick(event) {
    const target = event.target;
    if (!(target instanceof HTMLImageElement)) {
      return;
    }
    if (!articleRoot() || !articleRoot().contains(target)) {
      return;
    }
    if (target.closest("#threadwell-zoom")) {
      return;
    }
    event.preventDefault();
    openZoom(target.currentSrc || target.src);
  }

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeZoom();
    }
  });
  document.addEventListener("click", onArticleClick);
  addWideButton();
})();
