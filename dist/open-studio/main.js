(() => {
  "use strict";
  document.querySelector("#year").textContent = new Date().getFullYear();
  const galleries = {
    linc: { name: "Linc", files: ["linc-1", "linc-3", "linc-2", "linc-4"] },
    mgt: {
      name: "MyGoTrainer",
      files: ["mgt-1", "mgt-2", "mgt-3", "mgt-4", "mgt-5", "mgt-6", "mgt-7"],
    },
    ss: { name: "Shipshape", files: ["ss-1", "ss-2", "ss-3"] },
    chatbox: {
      name: "Chatbox",
      files: ["chatbox-1", "chatbox-2", "chatbox-3"],
    },
    ecomm: { name: "E-commerce", files: ["ecomm-1", "ecomm-2", "ecomm-3"] },
  };
  const dialog = document.querySelector("#gallery");
  let galleryKey = "linc";
  let galleryIndex = 0;
  let galleryTrigger;
  function renderGallery() {
    const gallery = galleries[galleryKey];
    document.querySelector("#gallery-title").textContent = gallery.name;
    const image = document.querySelector("#gallery-image");
    image.src = `dist/img/${galleryKey}/${gallery.files[galleryIndex]}@2x.jpg`;
    image.alt = `${gallery.name} — project screen ${galleryIndex + 1}`;
    document.querySelector("#gallery-count").textContent =
      `${galleryIndex + 1} / ${gallery.files.length}`;
  }
  function moveGallery(delta) {
    galleryIndex =
      (galleryIndex + delta + galleries[galleryKey].files.length) %
      galleries[galleryKey].files.length;
    renderGallery();
  }
  document.querySelectorAll("[data-gallery]").forEach((button) =>
    button.addEventListener("click", () => {
      galleryKey = button.dataset.gallery;
      galleryIndex = 0;
      galleryTrigger = button;
      renderGallery();
      dialog.showModal();
    }),
  );
  document
    .querySelector("#gallery-close")
    .addEventListener("click", () => dialog.close());
  document
    .querySelector("#gallery-prev")
    .addEventListener("click", () => moveGallery(-1));
  document
    .querySelector("#gallery-next")
    .addEventListener("click", () => moveGallery(1));
  dialog.addEventListener("keydown", (event) => {
    if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
      event.preventDefault();
      moveGallery(event.key === "ArrowLeft" ? -1 : 1);
    }
  });
  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) {
      const rect = dialog.getBoundingClientRect();
      if (
        event.clientX < rect.left ||
        event.clientX > rect.right ||
        event.clientY < rect.top ||
        event.clientY > rect.bottom
      )
        dialog.close();
    }
  });
  dialog.addEventListener("close", () => galleryTrigger?.focus());
})();
