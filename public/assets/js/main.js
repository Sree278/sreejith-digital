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

  const contactForm = document.querySelector("[data-contact-form]");
  if (contactForm instanceof HTMLFormElement) {
    const status = contactForm.querySelector("[data-form-status]");
    const fieldLabels = {
      name: "Name",
      email: "Work email",
      company: "Company",
      website: "Website",
      service: "Area of interest",
      timeline: "Ideal timeline",
      message: "What would you like to improve?",
    };

    contactForm.addEventListener("input", () => {
      if (!status) return;
      status.textContent = "";
      status.removeAttribute("data-state");
    });

    contactForm.addEventListener("submit", (event) => {
      event.preventDefault();

      if (!contactForm.reportValidity()) {
        if (status) {
          status.textContent = "Please complete the required fields before continuing.";
          status.dataset.state = "error";
        }
        return;
      }

      const data = new FormData(contactForm);
      const recipient = contactForm.dataset.contactEmail || "hello@sreejithdigital.com";
      const name = String(data.get("name") || "").trim();
      const company = String(data.get("company") || "").trim();
      const subject = `Consultation enquiry — ${company || name || "Sreejith Digital website"}`;

      const lines = [
        "Consultation enquiry from sreejithdigital.com",
        "",
      ];

      Object.entries(fieldLabels).forEach(([field, label]) => {
        const value = String(data.get(field) || "").trim();
        lines.push(`${label}: ${value || "—"}`);
      });

      lines.push("", "Sent from the static contact form. No data was stored by the website.");

      const mailto =
        `mailto:${recipient}` +
        `?subject=${encodeURIComponent(subject)}` +
        `&body=${encodeURIComponent(lines.join("\n"))}`;

      if (status) {
        status.textContent = "Your email app should open with the enquiry ready to review and send.";
        status.removeAttribute("data-state");
      }

      window.location.href = mailto;
    });
  }
})();
