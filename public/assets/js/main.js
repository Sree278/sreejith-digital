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
     Contact page: reveal the phone number after an email check.
     The number is never in the page; /api/contact returns it on success.
     --------------------------------------------------------------------- */
  document.querySelectorAll("[data-phone-form]").forEach((form) => {
    if (!(form instanceof HTMLFormElement)) return;
    const panel = form.closest("[data-phone-panel]");
    const status = form.querySelector("[data-phone-status]");
    const started = form.querySelector("[data-phone-started]");
    const result = panel ? panel.querySelector("[data-phone-result]") : null;
    const button = form.querySelector('button[type="submit"]');
    if (started instanceof HTMLInputElement) started.value = String(Date.now());

    const turnstileHost = form.querySelector("[data-turnstile-sitekey]");
    if (turnstileHost && !document.querySelector("script[data-turnstile]")) {
      const script = document.createElement("script");
      script.src = "https://challenges.cloudflare.com/turnstile/v0/api.js";
      script.async = true;
      script.defer = true;
      script.dataset.turnstile = "1";
      script.onload = () => {
        if (window.turnstile) window.turnstile.render(turnstileHost, { sitekey: turnstileHost.getAttribute("data-turnstile-sitekey") });
      };
      document.head.appendChild(script);
    }

    const messages = {
      invalid_email: "Please enter a valid email address.",
      invalid_phone: "Please enter a valid mobile number, for example +91 98XXXXXXXX.",
      email_not_accepted: "That email address can’t be used. Please use a Gmail, Outlook, Yahoo, iCloud or your company email (no temporary or relay addresses).",
      rate_limited: "Too many requests. Please try again later or use the enquiry form.",
      challenge_failed: "Please complete the check and try again.",
      try_again: "We couldn’t check that address just now. Please try again in a moment.",
      not_configured: "The number isn’t available online right now. Please use the enquiry form or email.",
      daily_limit: "The number has been requested too many times today. Please use the enquiry form and I will reply personally.",
      link_invalid: "That confirmation link has expired or was already used. Please request a new one.",
    };
    const showNumber = (data) => {
      const tel = panel.querySelector("[data-phone-tel]");
      const wa = panel.querySelector("[data-phone-wa]");
      if (tel) { tel.textContent = data.phone; tel.setAttribute("href", `tel:${data.phone}`); }
      if (wa && /^https:\/\/wa\.me\/[0-9]+$/.test(data.whatsapp || "")) wa.setAttribute("href", data.whatsapp);
      form.hidden = true;
      if (result) result.hidden = false;
      trackEvent("phone_reveal", {});
    };
    const setStatus = (text, state) => {
      if (!status) return;
      status.textContent = text;
      if (state) status.dataset.state = state;
      else status.removeAttribute("data-state");
    };

    // Opened from the confirmation email: ?verify=<signed token>
    const verifyToken = new URLSearchParams(window.location.search).get("verify");
    if (verifyToken) {
      setStatus("Confirming your email…");
      fetch("/api/contact/verify", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({ token: verifyToken }),
      })
        .then((response) => response.json().catch(() => null).then((data) => ({ response, data })))
        .then(({ response, data }) => {
          if (response.ok && data && data.ok && data.phone) {
            showNumber(data);
            window.history.replaceState(null, "", window.location.pathname);
          } else {
            setStatus(messages[data && data.code] || "Something went wrong. Please use the enquiry form or email.", "error");
          }
        })
        .catch(() => setStatus("The check couldn’t reach the server. Please use the enquiry form or email.", "error"));
    }
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const emailField = form.querySelector('[name="email"]');
      if (!(emailField instanceof HTMLInputElement) || !emailField.value.trim() || !emailField.checkValidity()) {
        setStatus(messages.invalid_email, "error");
        return;
      }
      const phoneField = form.querySelector('[name="visitor_phone"]');
      if (!(phoneField instanceof HTMLInputElement) || !/^\+?[0-9][0-9\s().-]{7,18}$/.test(phoneField.value.trim())) {
        setStatus(messages.invalid_phone, "error");
        return;
      }
      const payload = {
        email: emailField.value.trim(),
        visitor_phone: phoneField.value.trim(),
        started_at: started instanceof HTMLInputElement ? started.value : "",
        company_url: String(new FormData(form).get("company_url") || ""),
      };
      const token = form.querySelector('[name="cf-turnstile-response"]');
      if (token instanceof HTMLInputElement) payload.turnstile_token = token.value;
      if (button) button.disabled = true;
      setStatus("Checking…");
      try {
        const response = await fetch("/api/contact", {
          method: "POST",
          headers: { "Content-Type": "application/json", Accept: "application/json" },
          body: JSON.stringify(payload),
        });
        let data = null;
        try { data = await response.json(); } catch (error) { data = null; }
        if (response.ok && data && data.ok && data.phone) {
          showNumber(data);
          return;
        }
        if (response.ok && data && data.ok && data.step === "verify_sent") {
          setStatus("Check your inbox: I have emailed you a link. Open it within 30 minutes to see my number.", "ok");
          if (window.turnstile) window.turnstile.reset();
          return;
        }
        setStatus(messages[data && data.code] || "Something went wrong. Please use the enquiry form or email.", "error");
      } catch (error) {
        setStatus("The check couldn’t reach the server. Please use the enquiry form or email.", "error");
      } finally {
        // A Turnstile token works once; always get a fresh one for the next try.
        if (window.turnstile && !form.hidden) window.turnstile.reset();
        if (button) button.disabled = false;
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
