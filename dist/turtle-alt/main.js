(() => {
  "use strict";
  const products = {
    numi: {
      title: "Less logging.<br>More living.",
      description: "Numi — nutrition, with a little intelligence.",
      name: "Numi",
      images: [
        ["numi/device-meal.webp", "Numi weekly nutrition insights"],
        ["numi/device-home.webp", "Numi daily nutrition overview"],
        ["numi/device-progress.webp", "Numi progress tracking"],
      ],
    },
    tysha: {
      title: "A little more<br>peace and quiet.",
      description: "Tysha — made for the 3 a.m. shift.",
      name: "Tysha",
      images: [
        ["tysha/screen-1.webp", "Tysha instant sound playback"],
        ["tysha/screen-2.webp", "Tysha sound library"],
      ],
    },
    karta: {
      title: "Scan. Eat.<br>Pay. Go.",
      description: "Karta — the whole restaurant, connected.",
      name: "Karta",
      images: [
        ["karta/dashboard@2x.jpg", "Karta restaurant dashboard"],
        ["karta/guest-menu.jpg", "Karta guest menu"],
      ],
    },
  };
  const panel = document.querySelector("#showcase-panel");
  const tabs = [...document.querySelectorAll('[data-product][role="tab"]')];
  function selectProduct(tab) {
    const key = tab.dataset.product;
    const product = products[key];
    tabs.forEach((item) => {
      item.setAttribute("aria-selected", String(item === tab));
      item.tabIndex = item === tab ? 0 : -1;
    });
    panel.dataset.product = key;
    panel.setAttribute("aria-labelledby", tab.id);
    panel.querySelector("h2").innerHTML = product.title;
    panel.querySelector(".showcase-copy p").textContent = product.description;
    const link = panel.querySelector("a");
    link.href = `case/${key}.html`;
    link.setAttribute("aria-label", `Explore ${product.name} case study`);
    panel.querySelector(".showcase-phones").replaceChildren(
      ...product.images.map(([src, alt]) => {
        const image = document.createElement("img");
        image.src = `dist/img/${src}`;
        image.alt = alt;
        return image;
      }),
    );
  }
  tabs.forEach((tab, index) => {
    tab.addEventListener("click", () => selectProduct(tab));
    tab.addEventListener("keydown", (event) => {
      let next;
      if (event.key === "ArrowRight") next = (index + 1) % tabs.length;
      if (event.key === "ArrowLeft")
        next = (index + tabs.length - 1) % tabs.length;
      if (event.key === "Home") next = 0;
      if (event.key === "End") next = tabs.length - 1;
      if (next === undefined) return;
      event.preventDefault();
      tabs[next].focus();
      selectProduct(tabs[next]);
    });
  });

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
