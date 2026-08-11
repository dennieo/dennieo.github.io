/* Google Analytics 4 for imdennie.com
 * One file, loaded on every page. Put your Measurement ID below and it goes live.
 * Beyond pageviews it tracks the high-intent actions on a portfolio:
 *   - link_click  (with link_category: app_store, karta_demo, numi_site,
 *                  prompt_io, linkedin, github, shipshape, email, case_study,
 *                  blog, external)
 *   - resume_pdf  (someone saved/printed the resume)
 */
(function () {
  "use strict";

  // ---------------------------------------------------------------------------
  // TODO(Dennie): paste your GA4 Measurement ID here (looks like "G-ABC123DEF4").
  // Get it at analytics.google.com → Admin → Data streams → your web stream.
  var GA_ID = "G-SXF5SS0QYH";
  // ---------------------------------------------------------------------------

  // Stay completely off until a real ID is set (the placeholder disables it).
  if (GA_ID === "G-XXXXXXXXXX" || !/^G-[A-Z0-9]{6,}$/.test(GA_ID)) return;

  // Load the gtag library.
  var g = document.createElement("script");
  g.async = true;
  g.src = "https://www.googletagmanager.com/gtag/js?id=" + GA_ID;
  document.head.appendChild(g);

  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }
  window.gtag = gtag;
  gtag("js", new Date());
  gtag("config", GA_ID);

  // Classify a clicked link into a useful bucket (or null = ignore).
  function categorize(a) {
    var href = a.getAttribute("href") || "";
    if (/^mailto:/i.test(href)) return "email";

    var external = /^https?:\/\//i.test(href) && a.hostname !== location.hostname;
    if (!external) {
      // Internal navigation — page_view already covers it. Only flag the
      // sections worth measuring intent on.
      if (/\/case\//.test(a.pathname)) return "case_study";
      if (/\/blog\//.test(a.pathname)) return "blog";
      return null;
    }

    var host = a.hostname;
    if (/apps\.apple\.com$/.test(host) || /(^|\.)apps\.apple\.com$/.test(host)) return "app_store";
    if (/(^|\.)getnumi\.app$/.test(host)) return "numi_site";
    if (/karta-nu\.vercel\.app$/.test(host)) return "karta_demo";
    if (/(^|\.)prompt\.io$/.test(host)) return "prompt_io";
    if (/(^|\.)linkedin\.com$/.test(host)) return "linkedin";
    if (/(^|\.)github\.com$/.test(host)) return "github";
    if (/(^|\.)shipshape\.ai$/.test(host)) return "shipshape";
    return "external";
  }

  document.addEventListener("click", function (e) {
    var a = e.target.closest ? e.target.closest("a[href]") : null;
    if (!a) return;
    var category = categorize(a);
    if (!category) return;
    gtag("event", "link_click", {
      link_category: category,
      link_url: a.href,
      link_text: (a.textContent || "").replace(/\s+/g, " ").trim().slice(0, 80),
      page_path: location.pathname
    });
  }, true);

  // Resume "Save as PDF" / any print of the resume.
  window.addEventListener("beforeprint", function () {
    gtag("event", "resume_pdf", { page_path: location.pathname });
  });
})();
