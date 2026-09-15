(() => {
  "use strict";

  // Decorative mouse feedback. Real links, touch, and keyboard focus stay usable.
  const finePointer = window.matchMedia("(hover: hover) and (pointer: fine)");
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const cursor = document.createElement("div");
  const position = document.createElement("div");
  const ring = document.createElement("span");
  const dot = document.createElement("span");
  cursor.className = "context-cursor";
  cursor.dataset.mode = "default";
  cursor.setAttribute("aria-hidden", "true");
  position.className = "context-cursor-position";
  ring.className = "context-cursor-ring";
  dot.className = "context-cursor-dot";
  position.append(ring);
  cursor.append(position, dot);
  document.body.append(cursor);

  const labels = new Map();
  function getLabel(text) {
    if (!labels.has(text)) {
      const label = document.createElement("span");
      label.className = "context-cursor-label";
      label.textContent = text.replace(" ", "\n");
      position.append(label);
      labels.set(text, label);
    }
    return labels.get(text);
  }
  document.querySelectorAll("[data-cursor]").forEach((target) => {
    getLabel(target.dataset.cursor);
  });

  let activeTarget = null;
  let activeLabel = null;
  let tracking = false;
  let visible = false;
  let frame = 0;
  let hitFrame = 0;
  let lastTime = 0;
  let x = 0;
  let y = 0;
  let targetX = 0;
  let targetY = 0;

  function setTarget(target, mode) {
    if (target !== activeTarget) {
      activeTarget?.classList.remove("is-cursor-hovered");
      activeTarget = target;
      if (mode === "lens") target.classList.add("is-cursor-hovered");
    }
    const nextLabel = mode === "lens" ? getLabel(target.dataset.cursor) : null;
    if (nextLabel !== activeLabel) {
      activeLabel?.classList.remove("is-active");
      nextLabel?.classList.add("is-active");
      activeLabel = nextLabel;
    }
    cursor.dataset.mode = mode;
  }

  function hide() {
    setTarget(null, "default");
    visible = false;
    cursor.classList.remove("is-visible");
    document.documentElement.classList.remove("has-context-cursor");
    cancelAnimationFrame(frame);
    frame = 0;
  }

  function suspend() {
    tracking = false;
    cancelAnimationFrame(hitFrame);
    hitFrame = 0;
    hide();
  }

  function render(time) {
    frame = 0;
    if (!visible) return;
    const elapsed = Math.min(time - lastTime || 1000 / 60, 64);
    lastTime = time;
    const follow = reducedMotion.matches
      ? 1
      : 1 - Math.pow(0.75, elapsed / (1000 / 60));
    x += (targetX - x) * follow;
    y += (targetY - y) * follow;
    position.style.transform = `translate3d(${x}px, ${y}px, 0)`;
    if (Math.abs(targetX - x) + Math.abs(targetY - y) > 0.1) {
      frame = requestAnimationFrame(render);
    }
  }

  function updateTarget() {
    if (!tracking) return;
    const element = document.elementFromPoint(targetX, targetY);
    if (
      !element ||
      document.querySelector("dialog[open]") ||
      element.closest(
        'input, textarea, select, [contenteditable]:not([contenteditable="false"]), :disabled, [aria-disabled="true"], [data-native-cursor]',
      )
    ) {
      hide();
      return;
    }

    const lens = element.closest("[data-cursor]");
    const control = element.closest(
      'a[href], button, summary, [role="button"], [role="tab"], [role="link"]',
    );
    setTarget(lens || control, lens ? "lens" : control ? "link" : "default");
    // Light primary buttons and white pill hovers need a dark compact cursor.
    cursor.dataset.contrast = control?.matches(".pill") ? "dark" : "light";
    if (!visible) {
      x = targetX;
      y = targetY;
      position.style.transform = `translate3d(${x}px, ${y}px, 0)`;
      visible = true;
      cursor.classList.add("is-visible");
      document.documentElement.classList.add("has-context-cursor");
    }
    dot.style.transform = `translate3d(${targetX}px, ${targetY}px, 0) translate(-50%, -50%)`;
    if (!frame) {
      lastTime = performance.now();
      frame = requestAnimationFrame(render);
    }
  }

  document.addEventListener(
    "pointermove",
    (event) => {
      if (!finePointer.matches || event.pointerType !== "mouse") {
        suspend();
        return;
      }
      tracking = true;
      targetX = event.clientX;
      targetY = event.clientY;
      updateTarget();
    },
    { passive: true },
  );
  // Recheck what moved beneath a stationary mouse instead of losing the cursor.
  document.addEventListener(
    "scroll",
    () => {
      if (!tracking || hitFrame) return;
      hitFrame = requestAnimationFrame(() => {
        hitFrame = 0;
        updateTarget();
      });
    },
    { passive: true, capture: true },
  );
  document.addEventListener("pointerdown", (event) => {
    if (event.pointerType !== "mouse") suspend();
  });
  document.addEventListener("pointercancel", suspend, { passive: true });
  document.addEventListener("pointerout", (event) => {
    if (!event.relatedTarget) suspend();
  });
  document.addEventListener("keydown", suspend);
  document.addEventListener("visibilitychange", suspend);
  window.addEventListener("blur", suspend);
  window.addEventListener("pagehide", suspend);
  window.addEventListener("resize", suspend, { passive: true });
  finePointer.addEventListener("change", suspend);
  reducedMotion.addEventListener("change", suspend);
  document.querySelectorAll("dialog").forEach((dialog) => {
    new MutationObserver(suspend).observe(dialog, {
      attributes: true,
      attributeFilter: ["open"],
    });
  });
})();
