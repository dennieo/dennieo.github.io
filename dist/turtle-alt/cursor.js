(() => {
  "use strict";

  // An enhancement for a mouse, never an alternative to the real link/button.
  const finePointer = window.matchMedia("(hover: hover) and (pointer: fine)");
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const cursor = document.createElement("div");
  const label = document.createElement("span");
  cursor.className = "context-cursor";
  cursor.setAttribute("aria-hidden", "true");
  label.className = "context-cursor-label";
  cursor.append(label);
  document.body.append(cursor);

  let activeTarget = null;
  let frame = 0;
  let x = 0;
  let y = 0;
  let targetX = 0;
  let targetY = 0;

  function hide() {
    activeTarget?.classList.remove("is-cursor-hovered");
    activeTarget = null;
    cursor.classList.remove("is-visible");
    cancelAnimationFrame(frame);
    frame = 0;
  }

  function render() {
    frame = 0;
    if (!activeTarget) return;
    const follow = reducedMotion.matches ? 1 : 0.24;
    x += (targetX - x) * follow;
    y += (targetY - y) * follow;
    cursor.style.transform = `translate3d(${x}px, ${y}px, 0)`;
    if (Math.abs(targetX - x) + Math.abs(targetY - y) > 0.1) {
      frame = requestAnimationFrame(render);
    }
  }

  document.addEventListener(
    "pointermove",
    (event) => {
      if (
        !finePointer.matches ||
        event.pointerType !== "mouse" ||
        document.querySelector("dialog[open]")
      ) {
        hide();
        return;
      }

      const target =
        event.target instanceof Element
          ? event.target.closest("[data-cursor]")
          : null;
      if (!target || target.matches(":disabled, [aria-disabled='true']")) {
        hide();
        return;
      }

      targetX = event.clientX;
      targetY = event.clientY;
      if (target !== activeTarget) {
        const entering = activeTarget === null;
        activeTarget?.classList.remove("is-cursor-hovered");
        activeTarget = target;
        label.textContent = target.dataset.cursor.replace(" ", "\n");
        if (entering) {
          x = targetX;
          y = targetY;
          cursor.style.transform = `translate3d(${x}px, ${y}px, 0)`;
        }
        target.classList.add("is-cursor-hovered");
        cursor.classList.add("is-visible");
      }
      if (!frame) frame = requestAnimationFrame(render);
    },
    { passive: true },
  );

  // Avoid leaving the visual behind on navigation, scroll, a dialog, or tab-out.
  document.addEventListener("pointerdown", hide, { passive: true });
  document.addEventListener("pointercancel", hide, { passive: true });
  document.addEventListener(
    "pointerout",
    (event) => {
      if (!event.relatedTarget) hide();
    },
    { passive: true },
  );
  document.addEventListener("keydown", hide);
  document.addEventListener("scroll", hide, { passive: true, capture: true });
  document.addEventListener("visibilitychange", hide);
  window.addEventListener("blur", hide);
  window.addEventListener("pagehide", hide);
  window.addEventListener("resize", hide, { passive: true });
  finePointer.addEventListener("change", hide);
  reducedMotion.addEventListener("change", hide);

  // Also cover dialogs opened by something other than a click or keypress.
  document.querySelectorAll("dialog").forEach((dialog) => {
    new MutationObserver(hide).observe(dialog, {
      attributes: true,
      attributeFilter: ["open"],
    });
  });
})();
