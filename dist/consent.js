/* Cookie consent for imdennie.com.
 *
 * Google Analytics is the site's only optional cookie. Nothing analytics-related
 * loads until the visitor accepts; Global Privacy Control and Do Not Track count
 * as a refusal. The choice lives in localStorage (strictly necessary storage)
 * and is asked again after about six months. dist/analytics.js reads
 * window.siteConsent and listens for the site:consentchange event. Any element
 * with data-cookie-settings (the footer button) reopens the choice.
 */
(function () {
  "use strict";

  if (window.siteConsent) return;

  var KEY = "imdennie-consent";
  var VERSION = 1;
  var MAX_AGE_MS = 182 * 24 * 60 * 60 * 1000;
  var uk = (document.documentElement.lang || "").toLowerCase().indexOf("uk") === 0;
  var TEXT = uk ? {
    label: "Налаштування cookie",
    title: "Cookie на imdennie.com",
    body: "Я хотів би використовувати cookie Google Analytics, щоб розуміти, як відвідувачі користуються сайтом. Вони вимкнені, доки ви не погодитеся.",
    details: "Докладніше",
    detailsHref: "/privacy.html#cookies-uk",
    accept: "Прийняти",
    reject: "Відхилити",
    close: "Закрити",
    on: "Зараз аналітика ввімкнена.",
    off: "Зараз аналітика вимкнена.",
    signal: "Ваш браузер надсилає сигнал конфіденційності (Global Privacy Control або Do Not Track), тому аналітика залишається вимкненою."
  } : {
    label: "Cookie choices",
    title: "Cookies on imdennie.com",
    body: "I’d like to use Google Analytics cookies to understand how visitors use this site. They stay off unless you accept.",
    details: "Cookie details",
    detailsHref: "/privacy.html#cookies",
    accept: "Accept",
    reject: "Reject",
    close: "Close",
    on: "Analytics is currently on.",
    off: "Analytics is currently off.",
    signal: "Your browser sends a privacy signal (Global Privacy Control or Do Not Track), so analytics stays off."
  };

  // Accept and Reject share one style so neither choice is nudged.
  var CSS =
    ".consent{position:fixed;z-index:20;right:max(16px,env(safe-area-inset-right));bottom:max(16px,env(safe-area-inset-bottom));left:max(16px,env(safe-area-inset-left));" +
      "max-width:460px;margin-left:auto;padding:22px 22px 20px;color:var(--ink,#101b1e);background:#fff;border:1px solid var(--line,#cdd2d6);" +
      "box-shadow:0 18px 50px rgba(16,27,30,.14);font-family:\"DM Sans\",Arial,sans-serif;font-size:15px;line-height:1.5;letter-spacing:-.01em}" +
    ".consent[hidden],.consent [hidden]{display:none}" +
    ".consent-title{margin:0 0 6px;font-size:18px;font-weight:600;letter-spacing:-.02em}" +
    ".consent-title:focus{outline:none}" +
    ".consent-text,.consent-status{margin:0;color:var(--muted,#505862)}" +
    ".consent-status{margin-top:8px}" +
    ".consent-text a{color:var(--ink,#101b1e);text-decoration:underline 1px;text-underline-offset:3px}" +
    ".consent-actions{display:flex;gap:10px;margin-top:18px}" +
    ".consent-btn{flex:1 1 0;min-height:44px;padding:10px 16px;border:1px solid var(--ink,#101b1e);color:var(--ink,#101b1e);background:#fff;font-weight:500}" +
    ".consent-btn:hover{background:#eef2ef}" +
    ".site-footer [data-cookie-settings]{display:inline-flex;align-items:center;min-height:44px}" +
    "@media print{.consent{display:none}}";

  function privacySignal() {
    return navigator.globalPrivacyControl === true ||
      navigator.doNotTrack === "1" || window.doNotTrack === "1";
  }

  function read() {
    try {
      var stored = JSON.parse(window.localStorage.getItem(KEY));
      if (stored && stored.v === VERSION && typeof stored.analytics === "boolean" &&
          Date.now() - stored.t < MAX_AGE_MS) return stored;
    } catch (error) { /* storage blocked or corrupt: ask again */ }
    return null;
  }

  var choice = read();

  function analyticsGranted() {
    return !privacySignal() && Boolean(choice && choice.analytics);
  }

  function decide(analytics) {
    choice = { v: VERSION, t: Date.now(), analytics: analytics };
    try { window.localStorage.setItem(KEY, JSON.stringify(choice)); } catch (error) { /* this page only */ }
    hide();
    window.dispatchEvent(new CustomEvent("site:consentchange", { detail: { analytics: analyticsGranted() } }));
  }

  window.siteConsent = { analyticsGranted: analyticsGranted };

  var banner = null;
  var opener = null;

  function build() {
    var style = document.createElement("style");
    style.textContent = CSS;
    document.head.appendChild(style);
    banner = document.createElement("section");
    banner.className = "consent";
    banner.setAttribute("aria-label", TEXT.label);
    banner.hidden = true;
    banner.innerHTML =
      '<p class="consent-title" tabindex="-1"></p>' +
      '<p class="consent-text"><span></span> <a></a></p>' +
      '<p class="consent-status"></p>' +
      '<div class="consent-actions">' +
        '<button type="button" class="consent-btn" data-consent="reject"></button>' +
        '<button type="button" class="consent-btn" data-consent="accept"></button>' +
        '<button type="button" class="consent-btn" data-consent="close"></button>' +
      "</div>";
    banner.querySelector(".consent-title").textContent = TEXT.title;
    banner.querySelector(".consent-text span").textContent = TEXT.body;
    var link = banner.querySelector(".consent-text a");
    link.textContent = TEXT.details;
    link.href = TEXT.detailsHref;
    banner.querySelector('[data-consent="reject"]').textContent = TEXT.reject;
    banner.querySelector('[data-consent="accept"]').textContent = TEXT.accept;
    banner.querySelector('[data-consent="close"]').textContent = TEXT.close;
    banner.addEventListener("click", function (event) {
      var action = event.target.closest("[data-consent]");
      if (!action) return;
      var value = action.getAttribute("data-consent");
      if (value === "close") hide();
      else decide(value === "accept");
    });
    banner.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && choice) hide();
    });
    document.body.appendChild(banner);
  }

  function show(fromSettings) {
    if (!banner) build();
    var signal = privacySignal();
    var status = banner.querySelector(".consent-status");
    status.textContent = signal ? TEXT.signal : fromSettings && choice ? (choice.analytics ? TEXT.on : TEXT.off) : "";
    status.hidden = !status.textContent;
    banner.querySelector('[data-consent="reject"]').hidden = signal;
    banner.querySelector('[data-consent="accept"]').hidden = signal;
    banner.querySelector('[data-consent="close"]').hidden = !signal;
    banner.hidden = false;
    if (fromSettings) {
      opener = document.activeElement;
      banner.querySelector(".consent-title").focus();
    }
  }

  function hide() {
    if (!banner || banner.hidden) return;
    var hadFocus = banner.contains(document.activeElement);
    banner.hidden = true;
    if (hadFocus && opener && document.contains(opener)) opener.focus();
    opener = null;
  }

  document.addEventListener("click", function (event) {
    var trigger = event.target.closest && event.target.closest("[data-cookie-settings]");
    if (!trigger) return;
    event.preventDefault();
    show(true);
  });

  function start() {
    if (!choice && !privacySignal()) show(false);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start, { once: true });
  else start();
})();
