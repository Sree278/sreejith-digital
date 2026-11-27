(() => {
  "use strict";

  const header = document.querySelector("[data-header]");
  const nav = document.querySelector("[data-primary-nav]");
  const navToggle = document.querySelector("[data-nav-toggle]");
  const navGroups = Array.from(document.querySelectorAll(".nav-group"));
  const yearElements = document.querySelectorAll("[data-year]");

  yearElements.forEach((element) => {
    element.textContent = String(new Date().getFullYear());
  });

  const setNavState = (open) => {
    if (!nav || !navToggle) return;
    nav.classList.toggle("is-open", open);
    navToggle.setAttribute("aria-expanded", String(open));
    navToggle.setAttribute("aria-label", open ? "Close navigation" : "Open navigation");
  };

  const closeNav = () => setNavState(false);

  const closeNavGroups = () => {
    navGroups.forEach((group) => group.removeAttribute("open"));
  };

  if (navToggle && nav) {
    navToggle.addEventListener("click", () => {
      setNavState(!nav.classList.contains("is-open"));
    });

    nav.addEventListener("click", (event) => {
      const link = event.target.closest("a");
      if (link && window.matchMedia("(max-width: 1079px)").matches) {
        closeNav();
      }
    });
  }

  navGroups.forEach((group) => {
    group.addEventListener("toggle", () => {
      if (!group.open) return;
      navGroups.forEach((other) => {
        if (other !== group) other.removeAttribute("open");
      });
    });
  });

  document.addEventListener("click", (event) => {
    const target = event.target;
    if (!(target instanceof Element)) return;

    if (!target.closest(".nav-group")) {
      closeNavGroups();
    }

    if (
      nav &&
      nav.classList.contains("is-open") &&
      !target.closest(".site-header") &&
      window.matchMedia("(max-width: 1079px)").matches
    ) {
      closeNav();
    }
  });

  document.addEventListener("focusin", (event) => {
    if (!(event.target instanceof Element)) return;
    if (!event.target.closest(".nav-group")) closeNavGroups();
  });

  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") return;
    closeNavGroups();
    closeNav();
  });

  window.addEventListener("resize", () => {
    if (window.innerWidth >= 1080) closeNav();
  });

  const updateHeader = () => {
    if (header) header.classList.toggle("is-scrolled", window.scrollY > 8);
  };
  const handleWindowScroll = () => {
    updateHeader();
    if (window.matchMedia("(min-width: 1080px)").matches) {
      closeNavGroups();
    }
  };
  updateHeader();
  window.addEventListener("scroll", handleWindowScroll, { passive: true });

  /* ---------------------------------------------------------------------
     Storage helpers — browser storage can be unavailable; never let it throw.
     --------------------------------------------------------------------- */
  const store = {
    get(key) {
      try { return window.localStorage.getItem(key); } catch (error) { return null; }
    },
    set(key, value) {
      try { window.localStorage.setItem(key, value); } catch (error) { /* ignore */ }
    },
    sessionGet(key) {
      try { return window.sessionStorage.getItem(key); } catch (error) { return null; }
    },
    sessionSet(key, value) {
      try { window.sessionStorage.setItem(key, value); } catch (error) { /* ignore */ }
    },
  };

  /* ---------------------------------------------------------------------
     Consent-gated analytics. Nothing loads unless IDs are configured in the
     generator (window.SD_ANALYTICS) AND the visitor chooses "Allow".
     --------------------------------------------------------------------- */
  const analyticsConfig = window.SD_ANALYTICS || null;
  const CONSENT_KEY = "sd-analytics-consent";
  let analyticsLoaded = false;

  const loadAnalytics = () => {
    if (!analyticsConfig || analyticsLoaded) return;
    analyticsLoaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function gtag() { window.dataLayer.push(arguments); };
    // Consent Mode v2: the visitor allowed analytics only. Advertising signals
    // stay denied until the banner asks for advertising consent as well.
    window.gtag("consent", "default", {
      analytics_storage: "granted",
      ad_storage: "denied",
      ad_user_data: "denied",
      ad_personalization: "denied",
      functionality_storage: "granted",
      security_storage: "granted",
    });
    if (analyticsConfig.gtm) {
      // Google Tag Manager carries GA4, Clarity and future ad tags.
      window.dataLayer.push({ "gtm.start": Date.now(), event: "gtm.js" });
      const gtm = document.createElement("script");
      gtm.async = true;
      gtm.src = `https://www.googletagmanager.com/gtm.js?id=${encodeURIComponent(analyticsConfig.gtm)}`;
      document.head.appendChild(gtm);
      return;
    }
    if (analyticsConfig.ga4) {
      const tag = document.createElement("script");
      tag.async = true;
      tag.src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(analyticsConfig.ga4)}`;
      document.head.appendChild(tag);
      window.dataLayer = window.dataLayer || [];
      window.gtag = function gtag() { window.dataLayer.push(arguments); };
      window.gtag("js", new Date());
      window.gtag("config", analyticsConfig.ga4, { anonymize_ip: true });
    }
    if (analyticsConfig.clarity) {
      (function clarityLoader(c, l, a, r, i) {
        c[a] = c[a] || function clarityQueue() { (c[a].q = c[a].q || []).push(arguments); };
        const t = l.createElement(r);
        t.async = 1;
        t.src = `https://www.clarity.ms/tag/${encodeURIComponent(i)}`;
        const y = l.getElementsByTagName(r)[0];
        y.parentNode.insertBefore(t, y);
      })(window, document, "clarity", "script", analyticsConfig.clarity);
    }
  };

  const trackEvent = (name, params) => {
    if (analyticsConfig && analyticsConfig.gtm) {
      // GTM reads these from the dataLayer (custom-event triggers).
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push(Object.assign({ event: name }, params || {}));
      return;
    }
    if (typeof window.gtag === "function") window.gtag("event", name, params || {});
  };

  const banner = document.querySelector("[data-consent-banner]");
  const setBannerOpen = (open) => {
    if (!banner) return;
    banner.hidden = !open;
    document.body.classList.toggle("consent-open", open);
  };

  if (analyticsConfig) {
    const choice = store.get(CONSENT_KEY);
    if (choice === "granted") loadAnalytics();
    if (!choice) setBannerOpen(true);
  }

  document.addEventListener("click", (event) => {
    const target = event.target;
    if (!(target instanceof Element)) return;
    const choiceButton = target.closest("[data-consent]");
    if (choiceButton) {
      const value = choiceButton.getAttribute("data-consent") === "granted" ? "granted" : "denied";
      store.set(CONSENT_KEY, value);
      setBannerOpen(false);
      if (value === "granted") loadAnalytics();
      return;
    }
    if (target.closest("[data-consent-open]")) setBannerOpen(true);
  });

  /* ---------------------------------------------------------------------
     Sticky mobile CTA: hide it while a form or the footer is on screen.
     --------------------------------------------------------------------- */
  const mobileCta = document.querySelector("[data-mobile-cta]");
  if (mobileCta && "IntersectionObserver" in window) {
    const blockers = document.querySelectorAll(".hero-actions, .site-footer, .cta-section, form");
    const visible = new Set();
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) visible.add(entry.target);
        else visible.delete(entry.target);
      });
      mobileCta.classList.toggle("is-hidden", visible.size > 0);
    }, { threshold: 0.05 });
    blockers.forEach((element) => observer.observe(element));
  }

  /* ---------------------------------------------------------------------
     Enquiry forms: POST to the Worker endpoint; if it is not configured or
     unreachable, fall back to preparing the email in the visitor's app.
     --------------------------------------------------------------------- */
  const makeReference = () => {
    const now = new Date();
    const pad = (value) => String(value).padStart(2, "0");
    const date = `${now.getFullYear()}${pad(now.getMonth() + 1)}${pad(now.getDate())}`;
    const random = Math.random().toString(36).slice(2, 8).toUpperCase();
    return `SD-${date}-${random}`;
  };

  const fieldLabels = {
    name: "Name",
    email: "Business email",
    website: "Website",
    service: "What do you need?",
    budget: "Monthly marketing budget",
    message: "Message",
    offer: "Enquiry type",
    form_location: "Form",
  };

  document.querySelectorAll("[data-enquiry-form]").forEach((form) => {
    if (!(form instanceof HTMLFormElement)) return;
    const status = form.querySelector("[data-form-status]");
    const startedAt = form.querySelector("[data-started-at]");
    const submitButton = form.querySelector('button[type="submit"]');
    if (startedAt instanceof HTMLInputElement) startedAt.value = String(Date.now());

    const setStatus = (text, state) => {
      if (!status) return;
      status.textContent = text;
      if (state) status.dataset.state = state;
      else status.removeAttribute("data-state");
    };

    let started = false;
    form.addEventListener("input", () => {
      setStatus("");
      if (!started) {
        started = true;
        trackEvent("form_start", { form_location: form.querySelector('[name="form_location"]')?.value || "" });
      }
    });

    const fallbackToEmail = (data, reference) => {
      const recipient = form.dataset.contactEmail || "hello@sreejithdigital.com";
      const name = String(data.get("name") || "").trim();
      const subject = `${String(data.get("offer") || "Enquiry")} — ${name || "sreejithdigital.com"} [${reference}]`;
      const lines = ["Enquiry from sreejithdigital.com", `Reference: ${reference}`, ""];
      Object.entries(fieldLabels).forEach(([field, label]) => {
        const value = String(data.get(field) || "").trim();
        lines.push(`${label}: ${value || "—"}`);
      });
      setStatus("The form couldn’t reach the server, so your email app will open with the enquiry ready to send.", "error");
      window.location.href =
        `mailto:${recipient}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(lines.join("\n"))}`;
    };

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      if (!form.reportValidity()) {
        setStatus("Please complete the required fields before sending.", "error");
        return;
      }

      const data = new FormData(form);
      const reference = makeReference();
      const payload = { reference };
      data.forEach((value, key) => { payload[key] = String(value); });
      payload.page = window.location.pathname;

      if (submitButton) submitButton.disabled = true;
      setStatus("Sending…");

      const controller = "AbortController" in window ? new AbortController() : null;
      const timer = controller ? window.setTimeout(() => controller.abort(), 12000) : null;

      try {
        const response = await fetch(form.getAttribute("action") || "/api/enquiry", {
          method: "POST",
          headers: { "Content-Type": "application/json", Accept: "application/json" },
          body: JSON.stringify(payload),
          signal: controller ? controller.signal : undefined,
        });
        let result = null;
        try { result = await response.json(); } catch (error) { result = null; }
        if (response.ok && result && result.ok) {
          const ref = result.reference || reference;
          store.sessionSet("sd-last-enquiry", ref);
          window.location.href = `/thank-you/?ref=${encodeURIComponent(ref)}`;
          return;
        }
        fallbackToEmail(data, reference);
      } catch (error) {
        fallbackToEmail(data, reference);
      } finally {
        if (timer) window.clearTimeout(timer);
        if (submitButton) submitButton.disabled = false;
      }
    });
  });

  /* ---------------------------------------------------------------------
     Thank-you page: show the reference and record one lead per enquiry.
     --------------------------------------------------------------------- */
  const refHolder = document.querySelector("[data-enquiry-ref]");
  if (refHolder) {
    const params = new URLSearchParams(window.location.search);
    const ref = (params.get("ref") || "").replace(/[^A-Z0-9-]/gi, "").slice(0, 40);
    if (ref) {
      const strong = refHolder.querySelector("strong");
      if (strong) strong.textContent = ref;
      refHolder.hidden = false;
      const trackedKey = `sd-lead-${ref}`;
      if (!store.sessionGet(trackedKey)) {
        store.sessionSet(trackedKey, "1");
        trackEvent("generate_lead", { reference: ref });
      }
    }
  }
})();
