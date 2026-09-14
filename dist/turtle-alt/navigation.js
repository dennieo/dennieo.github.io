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

// Keep the original text available to assistive technology; only the visual
// duplicate moves into view. Static anchors leave menu and gallery labels alone.
(() => {
  "use strict";
  document
    .querySelectorAll("a.pill, .site-menu a, a.text-link")
    .forEach((link) => {
      if (
        link.classList.contains("hover-link") ||
        link.closest("[aria-live], [data-dynamic-label], [data-no-text-swap]")
      )
        return;

      const textNodes = [...link.childNodes].filter(
        (node) => node.nodeType === Node.TEXT_NODE && node.textContent.trim(),
      );
      if (!textNodes.length) return;

      textNodes.forEach((node) => {
        const slot = document.createElement("span");
        slot.className = "hover-link-slot";
        const original = document.createElement("span");
        original.className = "hover-link-original";
        const copy = document.createElement("span");
        copy.className = "hover-link-copy";
        copy.textContent = node.textContent;
        copy.setAttribute("aria-hidden", "true");
        // If the enhancement stylesheet fails, show just the original label.
        copy.hidden = true;
        node.replaceWith(slot);
        original.append(node);
        slot.append(original, copy);
      });
      link.classList.add("hover-link");
    });
})();
