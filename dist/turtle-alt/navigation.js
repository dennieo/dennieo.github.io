(() => {
  "use strict";
  const menuButton = document.querySelector(".menu-toggle");
  const menu = document.querySelector("#site-menu");
  menu.hidden = true;
  document.documentElement.classList.add("menu-ready");
  function closeMenu(restoreFocus = false) {
    menu.hidden = true;
    menuButton.setAttribute("aria-expanded", "false");
    menuButton.textContent = "Menu";
    if (restoreFocus) menuButton.focus();
  }
  menuButton.addEventListener("click", () => {
    const open = menu.hidden;
    menu.hidden = !open;
    menuButton.setAttribute("aria-expanded", String(open));
    menuButton.textContent = open ? "Close" : "Menu";
  });
  menu.addEventListener("click", (event) => {
    const link = event.target.closest("a");
    if (!link) return;
    closeMenu();
    if (link.hash && link.pathname === location.pathname) {
      const target = document.querySelector(link.hash);
      if (target) {
        target.setAttribute("tabindex", "-1");
        target.focus({ preventScroll: true });
      }
    }
  });
  document.addEventListener("click", (event) => {
    if (
      !menu.hidden &&
      !menu.contains(event.target) &&
      !menuButton.contains(event.target)
    )
      closeMenu();
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !menu.hidden) closeMenu(true);
  });
  document.addEventListener("focusin", (event) => {
    if (
      !menu.hidden &&
      !menu.contains(event.target) &&
      !menuButton.contains(event.target)
    )
      closeMenu();
  });

  document.querySelector("#year").textContent = new Date().getFullYear();
})();
