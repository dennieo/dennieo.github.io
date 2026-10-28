/* Google Analytics (GA4) for imdennie.com — loaded only with consent.
 *
 * dist/consent.js asks first. Until the visitor accepts, gtag() calls are
 * dropped rather than queued, so nothing collected before consent is sent
 * later, and gtag.js is never requested. Google signals and ad
 * personalisation stay off. Withdrawing consent disables GA and deletes its
 * cookies. On top of page views this adds two high-intent events:
 *   - link_click  (link_category: app_store, karta_demo, numi_site, prompt_io,
 *                  linkedin, github, shipshape, email, case_study, blog,
 *                  work_with_me)
 *   - resume_pdf  (someone saved / printed the resume)
 */
(function () {
  "use strict";

  var MEASUREMENT_ID = "G-SXF5SS0QYH";
  if (window._siteAnalyticsReady) return;
  window._siteAnalyticsReady = true;

  function granted() {
    return Boolean(window.siteConsent && window.siteConsent.analyticsGranted());
  }

  window.dataLayer = window.dataLayer || [];
  function gtag() {
    if (granted()) window.dataLayer.push(arguments);
  }
  window.gtag = gtag;

  var loaded = false;
  function load() {
    if (loaded || !granted()) return;
    loaded = true;
    window["ga-disable-" + MEASUREMENT_ID] = false;
    gtag("consent", "default", {
      analytics_storage: "granted",
      ad_storage: "denied",
      ad_user_data: "denied",
      ad_personalization: "denied"
    });
    gtag("js", new Date());
    gtag("config", MEASUREMENT_ID, {
      allow_google_signals: false,
      allow_ad_personalization_signals: false
    });
    var script = document.createElement("script");
    script.async = true;
    script.src = "https://www.googletagmanager.com/gtag/js?id=" + MEASUREMENT_ID;
    document.head.appendChild(script);
  }

  function stop() {
    window["ga-disable-" + MEASUREMENT_ID] = true;
    if (loaded) window.dataLayer.push(["consent", "update", { analytics_storage: "denied" }]);
    var host = location.hostname;
    document.cookie.split(";").forEach(function (cookie) {
      var name = cookie.split("=")[0].trim();
      if (name !== "_ga" && name.indexOf("_ga_") !== 0) return;
      [host, "." + host, "." + host.split(".").slice(-2).join(".")].forEach(function (domain) {
        document.cookie = name + "=; Max-Age=0; path=/; domain=" + domain;
      });
      document.cookie = name + "=; Max-Age=0; path=/";
    });
  }

  window.addEventListener("site:consentchange", function (event) {
    if (event.detail && event.detail.analytics) load();
    else stop();
  });
  load();

  // Classify a clicked link into a useful bucket (or null = ignore).
  function categorize(a) {
    var href = a.getAttribute("href") || "";
    if (/^mailto:/i.test(href)) return "email";

    var external = /^https?:\/\//i.test(href) && a.hostname !== location.hostname;
    if (!external) {
      // Internal navigation — page_view already covers it. Only flag the
      // sections worth measuring intent on. Same-page anchors and self-links
      // (skip link, "How it works ↓", aria-current nav) are not intent.
      if (a.pathname === location.pathname) return null;
      if (/\/case\//.test(a.pathname)) return "case_study";
      if (/^\/work-with-me\.html$/.test(a.pathname)) return "work_with_me";
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
    // Email links report only the category: the address itself is personal data.
    gtag("event", "link_click", {
      link_category: category,
      link_url: category === "email" ? "mailto:" : a.href,
      link_text: category === "email" ? "" : (a.textContent || "").replace(/\s+/g, " ").trim().slice(0, 80),
      page_path: location.pathname
    });
  }, true);

  // Resume "Save as PDF" / any print of the resume.
  window.addEventListener("beforeprint", function () {
    gtag("event", "resume_pdf", { page_path: location.pathname });
  });
})();
