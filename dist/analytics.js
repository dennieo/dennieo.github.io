/* Custom GA4 events for imdennie.com
 *
 * The base Google tag (gtag.js loader + config) is the standard inline snippet
 * in each page's <head> — that's what Google's tag detection looks for. This
 * file only adds the extra, high-intent events on top of it:
 *   - link_click  (link_category: app_store, karta_demo, numi_site, prompt_io,
 *                  linkedin, github, shipshape, email, case_study, blog)
 *   - resume_pdf  (someone saved / printed the resume)
 *
 * It pushes to the same dataLayer the inline tag created, so nothing loads
 * twice and there are no duplicate pageviews. Harmless if the tag is absent.
 */
(function () {
  "use strict";

  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }

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
    if (/(^|\.)apps\.apple\.com$/.test(host)) return "app_store";
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
