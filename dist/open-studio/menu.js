(() => {
  "use strict";
  // Full-screen phone menu. The dialog is modal, so focus is trapped
  // inside it, the page behind is inert, and Escape closes it.
  const menu = document.querySelector("#site-menu");
  const toggle = document.querySelector('[aria-controls="site-menu"]');
  if (!menu || !toggle) return;
  const phone = window.matchMedia("(max-width: 760px)");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  let closeTimer;
  function openMenu() {
    clearTimeout(closeTimer);
    menu.classList.remove("is-closing");
    menu.showModal();
    toggle.setAttribute("aria-expanded", "true");
  }
  function closeMenu(animate = true) {
    if (!menu.open) return;
    clearTimeout(closeTimer);
    if (!animate || reduceMotion.matches) {
      menu.close();
      return;
    }
    menu.classList.add("is-closing");
    closeTimer = setTimeout(() => menu.close(), 200);
  }
  toggle.addEventListener("click", openMenu);
  menu
    .querySelector("[data-menu-close]")
    .addEventListener("click", () => closeMenu());
  menu.addEventListener("cancel", (event) => {
    event.preventDefault();
    closeMenu();
  });
  menu.addEventListener("close", () => {
    menu.classList.remove("is-closing");
    toggle.setAttribute("aria-expanded", "false");
  });
  // Close before following a link so in-page anchors scroll the unlocked page.
  menu.addEventListener("click", (event) => {
    if (event.target.closest("a")) closeMenu(false);
  });
  phone.addEventListener("change", (event) => {
    if (!event.matches) closeMenu(false);
  });
})();
