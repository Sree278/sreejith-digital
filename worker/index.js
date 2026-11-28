/**
 * sreejithdigital.com — enquiry endpoint (Cloudflare Worker + static assets).
 *
 * Only requests matching `run_worker_first` in wrangler.toml (/api/*) reach
 * this code; every page and asset is served straight from ./public.
 *
 * POST /api/enquiry
 *   - accepts JSON (from main.js) or a normal form post (no-JS fallback)
 *   - validates input, drops obvious bots (honeypot + time check)
 *   - emails the enquiry through Cloudflare Email Routing (send_email binding)
 *   - optionally keeps a copy in Workers KV (ENQUIRIES binding, 180-day TTL)
 *
 * Until Email Routing and the ENQUIRY_EMAIL binding are configured it answers
 * 503 "not_configured", and main.js falls back to preparing the email in the
 * visitor's own mail app — so the form never silently loses a lead.
 *
 * Configuration (see DEPLOYMENT.md → "Enquiry form"):
 *   [[send_email]] name = "ENQUIRY_EMAIL"        (wrangler.toml)
 *   ENQUIRY_FROM  — sender on this domain       ([vars] in wrangler.toml)
 *   ENQUIRY_TO    — your verified inbox          (secret: wrangler secret put ENQUIRY_TO)
 */
import { EmailMessage } from "cloudflare:email";

const MAX_BODY_BYTES = 20000;
const MIN_FILL_MS = 2500;
const LIMITS = { name: 100, email: 200, website: 300, service: 120, budget: 120, message: 4000, offer: 60, form_location: 60, page: 200, reference: 40 };
const EMAIL_RE = /^[^\s@<>"',;]+@[^\s@<>"',;]+\.[^\s@<>"',;]{2,}$/;

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/api/enquiry") {
      return handleEnquiry(request, env);
    }
    if (url.pathname === "/api/contact") {
      return handleContactReveal(request, env);
    }
    if (url.pathname === "/api/contact/verify") {
      return handleContactVerify(request, env);
    }
    if (url.pathname.startsWith("/api/")) {
      return json({ ok: false, code: "not_found" }, 404);
    }
    return env.ASSETS.fetch(request);
  },
};

/* ---------------------------------------------------------------------
   POST /api/contact — reveal the phone number to a verified-looking visitor.
   The number lives only in the CONTACT_PHONE secret, never in the HTML or the
   schema, so scrapers reading pages never see it. A visitor must give an email
   that (1) is well formed, (2) is not a disposable or relay address, and
   (3) is either from a reputable provider or a domain that really receives
   mail (MX record). Optional Cloudflare Turnstile adds a human challenge.
   --------------------------------------------------------------------- */
const REPUTABLE_EMAIL_DOMAINS = new Set([
  "gmail.com", "googlemail.com", "outlook.com", "hotmail.com", "live.com", "msn.com",
  "yahoo.com", "yahoo.in", "yahoo.co.in", "ymail.com", "icloud.com", "me.com", "mac.com",
  "proton.me", "protonmail.com", "zoho.com", "zohomail.in", "rediffmail.com", "aol.com",
  "fastmail.com", "hey.com",
]);
const BLOCKED_EMAIL_DOMAINS = new Set([
  // Disposable / temporary inboxes
  "mailinator.com", "guerrillamail.com", "guerrillamail.net", "guerrillamail.org", "guerrillamail.biz",
  "sharklasers.com", "grr.la", "guerrillamailblock.com", "pokemail.net", "spam4.me",
  "10minutemail.com", "10minutemail.net", "20minutemail.com", "tempmail.com", "temp-mail.org",
  "temp-mail.io", "tempmail.net", "tempmailo.com", "tempail.com", "tempr.email", "tmpmail.org",
  "tmpmail.net", "throwawaymail.com", "trashmail.com", "trashmail.net", "trashmail.de",
  "yopmail.com", "yopmail.net", "yopmail.fr", "cool.fr.nf", "jetable.org", "nospam.ze.tc",
  "getnada.com", "nada.email", "maildrop.cc", "mailnesia.com", "mailcatch.com", "mintemail.com",
  "dispostable.com", "fakeinbox.com", "fakemail.net", "emailondeck.com", "spamgourmet.com",
  "mytemp.email", "mohmal.com", "burnermail.io", "inboxkitten.com", "moakt.com", "mailsac.com",
  "dropmail.me", "emailfake.com", "fakemailgenerator.com", "email-fake.com", "generator.email",
  "mail.tm", "1secmail.com", "1secmail.net", "1secmail.org", "wegwerfmail.de", "wegwerfmail.net",
  "discard.email", "discardmail.com", "mailforspam.com", "spambox.us", "spamex.com", "tempinbox.com",
  "harakirimail.com", "mailpoof.com", "tempmailaddress.com", "minuteinbox.com", "luxusmail.org",
  "anonbox.net", "mailtemp.net", "tmail.ws", "mail7.io", "mailnator.com", "yomail.info",
  "linshiyouxiang.net", "bccto.me", "chacuo.net", "33mail.com", "trbvm.com", "owlymail.com",
  "temporary-mail.net", "tempsky.com", "boxformail.in", "vusra.com", "nowmymail.com",
  // Generated forwarding / relay addresses
  "privaterelay.appleid.com", "relay.firefox.com", "mozmail.com", "simplelogin.com", "simplelogin.co",
  "simplelogin.fr", "aleeas.com", "slmail.me", "anonaddy.com", "anonaddy.me", "addy.io",
  "duck.com", "passmail.net", "passinbox.com", "mailnull.com",
]);

const contactHits = new Map(); // best-effort, per isolate: ip/email -> [timestamps]

function tooManyRequests(key, limit, windowMs) {
  const now = Date.now();
  const recent = (contactHits.get(key) || []).filter((time) => now - time < windowMs);
  if (recent.length >= limit) {
    contactHits.set(key, recent);
    return true;
  }
  recent.push(now);
  contactHits.set(key, recent);
  if (contactHits.size > 5000) contactHits.clear();
  return false;
}

// Visitor's own number (spam-proofing, like the email). Indian mobiles or
// international E.164 numbers; obvious fillers such as 9999999999 are refused.
function normaliseVisitorPhone(value) {
  const compact = String(value || "").trim().replace(/[\s().-]/g, "");
  if (!/^\+?[0-9]{8,15}$/.test(compact)) return null;
  let digits = compact.replace(/^\+/, "");
  let national;
  if (compact.startsWith("+")) {
    if (digits.startsWith("91")) {
      national = digits.slice(2);
      if (!/^[6-9][0-9]{9}$/.test(national)) return null;
    } else if (digits.length < 9 || digits.startsWith("0")) {
      return null;
    } else {
      national = digits.slice(-9);
    }
  } else {
    national = digits.replace(/^(?:91|0)(?=[6-9][0-9]{9}$)/, "");
    if (!/^[6-9][0-9]{9}$/.test(national)) return null;
    digits = `91${national}`;
  }
  if (/^(.)\1{6,}$/.test(national) || /0123456789|1234567890|9876543210|0987654321/.test(national)) return null;
  return `+${digits}`;
}

function emailDomainBlocked(domain) {
  if (BLOCKED_EMAIL_DOMAINS.has(domain)) return true;
  const parts = domain.split(".");
  for (let i = 1; i < parts.length - 1; i += 1) {
    if (BLOCKED_EMAIL_DOMAINS.has(parts.slice(i).join("."))) return true;
  }
  return /(^|[.-])(temp|tmp|trash|throwaway|disposable|burner|fakeinbox|10min|guerrilla)[a-z0-9-]*\./.test(domain);
}

async function domainReceivesMail(domain) {
  try {
    const response = await fetch(
      `https://cloudflare-dns.com/dns-query?name=${encodeURIComponent(domain)}&type=MX`,
      { headers: { Accept: "application/dns-json" }, cf: { cacheTtl: 3600 } }
    );
    if (!response.ok) return null;
    const data = await response.json();
    if (data.Status !== 0) return false;
    return Array.isArray(data.Answer) && data.Answer.some((record) => record.type === 15);
  } catch (error) {
    return null;
  }
}

async function handleContactReveal(request, env) {
  if (request.method !== "POST") {
    return json({ ok: false, code: "method_not_allowed" }, 405, { Allow: "POST" });
  }
  const raw = await request.text();
  if (raw.length > 2000) return json({ ok: false, code: "too_large" }, 413);
  let fields;
  try {
    fields = JSON.parse(raw);
  } catch (error) {
    return json({ ok: false, code: "bad_request" }, 400);
  }

  const phone = String(env.CONTACT_PHONE || "").replace(/[\s()-]/g, "");
  if (!/^\+?[0-9]{10,15}$/.test(phone)) {
    return json({ ok: false, code: "not_configured" }, 503);
  }

  const email = String(fields.email || "").trim().toLowerCase().slice(0, 200);
  const startedAt = Number(fields.started_at || 0);
  const botLike = String(fields.company_url || "").trim() !== "" || (startedAt > 0 && Date.now() - startedAt < 2000);
  if (botLike) return json({ ok: false, code: "invalid_email" }, 422);

  const visitorPhone = normaliseVisitorPhone(fields.visitor_phone);

  const ip = request.headers.get("CF-Connecting-IP") || "unknown";
  if (tooManyRequests(`ip:${ip}`, 3, 60 * 60 * 1000) || tooManyRequests(`email:${email}`, 2, 60 * 60 * 1000)) {
    return json({ ok: false, code: "rate_limited" }, 429);
  }

  if (!EMAIL_RE.test(email) || email.length > 120 || email.split("@").length !== 2) {
    return json({ ok: false, code: "invalid_email" }, 422);
  }
  if (!visitorPhone) {
    return json({ ok: false, code: "invalid_phone" }, 422);
  }
  const [local, domain] = email.split("@");
  if (local.length > 64 || !/^[a-z0-9.!#$%&'*+/=?^_`{|}~-]+$/.test(local) || !/^[a-z0-9.-]+\.[a-z]{2,}$/.test(domain)) {
    return json({ ok: false, code: "invalid_email" }, 422);
  }
  if (emailDomainBlocked(domain)) {
    return json({ ok: false, code: "email_not_accepted" }, 422);
  }

  if (!REPUTABLE_EMAIL_DOMAINS.has(domain)) {
    const receivesMail = await domainReceivesMail(domain);
    if (receivesMail === null) return json({ ok: false, code: "try_again" }, 503);
    if (!receivesMail) return json({ ok: false, code: "email_not_accepted" }, 422);
  }

  if (env.TURNSTILE_SECRET) {
    const token = String(fields.turnstile_token || "");
    let passed = false;
    if (token) {
      try {
        const verify = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: new URLSearchParams({ secret: env.TURNSTILE_SECRET, response: token, remoteip: ip }),
        });
        passed = Boolean((await verify.json()).success);
      } catch (error) {
        passed = false;
      }
    }
    if (!passed) return json({ ok: false, code: "challenge_failed" }, 403);
  }

  // Email verification (when a sender is configured): mail a signed, expiring
  // link. The number is shown only when the visitor opens it, which proves the
  // inbox is really theirs. Without a sender the checks above are the gate.
  if (verificationConfigured(env)) {
    if (await dailyCapReached(env)) return json({ ok: false, code: "daily_limit" }, 429);
    const token = await signToken(env, { e: email, p: visitorPhone, x: Date.now() + VERIFY_TTL_MS });
    const sent = await sendVerificationEmail(env, email, token);
    if (!sent) return json({ ok: false, code: "try_again" }, 503);
    return json({ ok: true, step: "verify_sent" });
  }

  if (await dailyCapReached(env)) return json({ ok: false, code: "daily_limit" }, 429);
  return revealNumber(env, email, visitorPhone, phone);
}

const VERIFY_TTL_MS = 30 * 60 * 1000;
const DAILY_REVEAL_CAP = 20;

function verificationConfigured(env) {
  return Boolean(env.VERIFY_SECRET && env.BREVO_API_KEY && env.VERIFY_FROM);
}

function b64url(bytes) {
  let text = "";
  for (const byte of bytes) text += String.fromCharCode(byte);
  return btoa(text).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

function b64urlDecode(value) {
  const padded = value.replace(/-/g, "+").replace(/_/g, "/") + "=".repeat((4 - (value.length % 4)) % 4);
  return Uint8Array.from(atob(padded), (char) => char.charCodeAt(0));
}

async function hmacKey(env, usage) {
  return crypto.subtle.importKey("raw", new TextEncoder().encode(env.VERIFY_SECRET), { name: "HMAC", hash: "SHA-256" }, false, [usage]);
}

async function signToken(env, payload) {
  const body = b64url(new TextEncoder().encode(JSON.stringify(payload)));
  const signature = await crypto.subtle.sign("HMAC", await hmacKey(env, "sign"), new TextEncoder().encode(body));
  return `${body}.${b64url(new Uint8Array(signature))}`;
}

async function readToken(env, token) {
  try {
    const [body, signature] = String(token || "").split(".");
    if (!body || !signature || token.length > 600) return null;
    const ok = await crypto.subtle.verify("HMAC", await hmacKey(env, "verify"), b64urlDecode(signature), new TextEncoder().encode(body));
    if (!ok) return null;
    const payload = JSON.parse(new TextDecoder().decode(b64urlDecode(body)));
    if (!payload || typeof payload.e !== "string" || typeof payload.p !== "string" || !(payload.x > Date.now())) return null;
    return payload;
  } catch (error) {
    return null;
  }
}

async function sendVerificationEmail(env, email, token) {
  const link = `https://sreejithdigital.com/contact/?verify=${encodeURIComponent(token)}`;
  try {
    const response = await fetch("https://api.brevo.com/v3/smtp/email", {
      method: "POST",
      headers: { "api-key": env.BREVO_API_KEY, "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify({
        sender: { name: "Sreejith Digital", email: env.VERIFY_FROM },
        to: [{ email }],
        subject: "Confirm your email to see my phone number",
        textContent: `Open this link within 30 minutes to see my phone number and WhatsApp:\n\n${link}\n\nIf you did not ask for this, ignore this email.\n\nSreejith, sreejithdigital.com`,
        htmlContent: `<p>Open this link within 30 minutes to see my phone number and WhatsApp:</p><p><a href="${link}">Show my contact number</a></p><p>If you did not ask for this, ignore this email.</p><p>Sreejith, sreejithdigital.com</p>`,
      }),
    });
    return response.ok;
  } catch (error) {
    return false;
  }
}

// Daily ceiling on reveals, kept in Workers KV (CONTACT_KV) when bound.
function todayKey() {
  return `reveals:${new Date().toISOString().slice(0, 10)}`;
}

async function dailyCapReached(env) {
  if (!env.CONTACT_KV) return false;
  const cap = Number(env.DAILY_REVEAL_CAP) || DAILY_REVEAL_CAP;
  return Number(await env.CONTACT_KV.get(todayKey())) >= cap;
}

async function countReveal(env) {
  if (!env.CONTACT_KV) return;
  const key = todayKey();
  await env.CONTACT_KV.put(key, String(Number(await env.CONTACT_KV.get(key)) + 1), { expirationTtl: 2 * 24 * 60 * 60 });
}

async function handleContactVerify(request, env) {
  if (request.method !== "POST") {
    return json({ ok: false, code: "method_not_allowed" }, 405, { Allow: "POST" });
  }
  const phone = String(env.CONTACT_PHONE || "").replace(/[\s()-]/g, "");
  if (!verificationConfigured(env) || !/^\+?[0-9]{10,15}$/.test(phone)) {
    return json({ ok: false, code: "not_configured" }, 503);
  }
  let fields;
  try {
    fields = JSON.parse(await request.text());
  } catch (error) {
    return json({ ok: false, code: "bad_request" }, 400);
  }
  const ip = request.headers.get("CF-Connecting-IP") || "unknown";
  if (tooManyRequests(`verify:${ip}`, 10, 60 * 60 * 1000)) return json({ ok: false, code: "rate_limited" }, 429);
  const payload = await readToken(env, fields.token);
  if (!payload) return json({ ok: false, code: "link_invalid" }, 410);
  if (env.CONTACT_KV) {
    const usedKey = `used:${String(fields.token).slice(-40)}`;
    if (await env.CONTACT_KV.get(usedKey)) return json({ ok: false, code: "link_invalid" }, 410);
    if (await dailyCapReached(env)) return json({ ok: false, code: "daily_limit" }, 429);
    await env.CONTACT_KV.put(usedKey, "1", { expirationTtl: 2 * 60 * 60 });
  }
  return revealNumber(env, payload.e, payload.p, phone);
}

async function revealNumber(env, email, visitorPhone, phone) {
  await countReveal(env).catch(() => {});
  // Tell the owner who asked — every reveal is also a lead. Best effort.
  if (env.ENQUIRY_EMAIL && env.ENQUIRY_TO && env.ENQUIRY_FROM) {
    try {
      const record = {
        name: "Phone number request", email, offer: "Phone reveal", form_location: "contact-phone",
        page: "/contact/", website: "", service: "", budget: "",
        message: `This visitor passed the email and phone checks and was shown your phone number.\nTheir phone: ${visitorPhone}`,
        reference: makeReference(), received_at: new Date().toISOString(),
      };
      await env.ENQUIRY_EMAIL.send(new EmailMessage(env.ENQUIRY_FROM, env.ENQUIRY_TO, buildMessage(env.ENQUIRY_FROM, env.ENQUIRY_TO, record)));
    } catch (error) {
      // The reveal must not depend on the notification.
    }
  }
  const digits = phone.replace(/^\+/, "");
  return json({ ok: true, phone: `+${digits}`, whatsapp: `https://wa.me/${digits}` });
}

async function handleEnquiry(request, env) {
  if (request.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: { Allow: "POST, OPTIONS" } });
  }
  if (request.method !== "POST") {
    return json({ ok: false, code: "method_not_allowed" }, 405, { Allow: "POST, OPTIONS" });
  }

  const contentType = (request.headers.get("content-type") || "").toLowerCase();
  const wantsJson = contentType.includes("application/json");
  const raw = await request.text();
  if (raw.length > MAX_BODY_BYTES) {
    return respond(wantsJson, { ok: false, code: "too_large" }, 413);
  }

  let fields;
  try {
    fields = wantsJson ? JSON.parse(raw) : Object.fromEntries(new URLSearchParams(raw));
  } catch (error) {
    return respond(wantsJson, { ok: false, code: "bad_request" }, 400);
  }

  const clean = {};
  for (const [key, limit] of Object.entries(LIMITS)) {
    clean[key] = String(fields[key] ?? "").replace(/\r\n?/g, "\n").trim().slice(0, limit);
  }

  const reference = /^SD-[0-9]{8}-[A-Z0-9]{6}$/.test(clean.reference) ? clean.reference : makeReference();

  // Bots: honeypot filled, or the form was submitted implausibly fast.
  const startedAt = Number(fields.started_at || 0);
  const tooFast = startedAt > 0 && Date.now() - startedAt < MIN_FILL_MS;
  if (String(fields.company_url || "").trim() !== "" || tooFast) {
    return respond(wantsJson, { ok: true, reference }, 200);
  }

  const consent = String(fields.consent || "").toLowerCase();
  if (!clean.name || !EMAIL_RE.test(clean.email) || !["yes", "on", "true"].includes(consent)) {
    return respond(wantsJson, { ok: false, code: "invalid" }, 422);
  }

  const record = { ...clean, reference, received_at: new Date().toISOString() };

  if (env.ENQUIRIES && typeof env.ENQUIRIES.put === "function") {
    try {
      await env.ENQUIRIES.put(reference, JSON.stringify(record), { expirationTtl: 60 * 60 * 24 * 180 });
    } catch (error) {
      // Storage is a convenience copy; email delivery below is what matters.
    }
  }

  if (!env.ENQUIRY_EMAIL || !env.ENQUIRY_TO || !env.ENQUIRY_FROM) {
    return respond(wantsJson, { ok: false, code: "not_configured", reference }, 503);
  }

  try {
    const message = buildMessage(env.ENQUIRY_FROM, env.ENQUIRY_TO, record);
    await env.ENQUIRY_EMAIL.send(new EmailMessage(env.ENQUIRY_FROM, env.ENQUIRY_TO, message));
  } catch (error) {
    return respond(wantsJson, { ok: false, code: "send_failed", reference }, 502);
  }

  return respond(wantsJson, { ok: true, reference }, 200);
}

function buildMessage(from, to, record) {
  const subject = `${record.offer || "Enquiry"} — ${record.name} [${record.reference}]`;
  const body = [
    "New enquiry from sreejithdigital.com",
    "",
    `Reference: ${record.reference}`,
    `Received:  ${record.received_at}`,
    `Type:      ${record.offer || "—"}`,
    `Form:      ${record.form_location || "—"} (${record.page || "—"})`,
    "",
    `Name:      ${record.name}`,
    `Email:     ${record.email}`,
    `Website:   ${record.website || "—"}`,
    `Service:   ${record.service || "—"}`,
    `Budget:    ${record.budget || "—"}`,
    "",
    "Message:",
    record.message || "—",
    "",
    "Reply directly to this email to answer the enquiry.",
  ].join("\r\n");

  const domain = String(from).split("@")[1] || "sreejithdigital.com";
  const headers = [
    `From: Sreejith Digital website <${headerSafe(from)}>`,
    `To: <${headerSafe(to)}>`,
    `Reply-To: ${encodeWord(record.name)} <${headerSafe(record.email)}>`,
    `Subject: ${encodeWord(subject)}`,
    `Message-ID: <${record.reference}.${Date.now()}@${headerSafe(domain)}>`,
    `Date: ${new Date().toUTCString()}`,
    "MIME-Version: 1.0",
    "Content-Type: text/plain; charset=UTF-8",
    "Content-Transfer-Encoding: base64",
  ];
  return `${headers.join("\r\n")}\r\n\r\n${wrapBase64(base64Utf8(body))}\r\n`;
}

function headerSafe(value) {
  return String(value).replace(/[\r\n<>]/g, "").trim();
}

function encodeWord(value) {
  const text = String(value).replace(/[\r\n]/g, " ");
  return /^[\x20-\x7E]*$/.test(text) && !/[=?"]/.test(text) ? text : `=?UTF-8?B?${base64Utf8(text)}?=`;
}

function base64Utf8(text) {
  const bytes = new TextEncoder().encode(text);
  let binary = "";
  for (const byte of bytes) binary += String.fromCharCode(byte);
  return btoa(binary);
}

function wrapBase64(value) {
  return value.replace(/.{1,76}/g, "$&\r\n").trim();
}

function makeReference() {
  const now = new Date();
  const pad = (number) => String(number).padStart(2, "0");
  const date = `${now.getUTCFullYear()}${pad(now.getUTCMonth() + 1)}${pad(now.getUTCDate())}`;
  const random = crypto.getRandomValues(new Uint8Array(4));
  const code = Array.from(random, (byte) => byte.toString(36).toUpperCase().padStart(2, "0")).join("").slice(0, 6);
  return `SD-${date}-${code.padEnd(6, "0")}`;
}

function json(payload, status = 200, extraHeaders = {}) {
  return new Response(JSON.stringify(payload), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store", ...extraHeaders },
  });
}

function respond(wantsJson, payload, status) {
  if (wantsJson) return json(payload, status);
  // No-JavaScript form post: send people somewhere useful either way.
  if (payload.ok) {
    return new Response(null, { status: 303, headers: { Location: `/thank-you/?ref=${encodeURIComponent(payload.reference || "")}` } });
  }
  const html = `<!doctype html><html lang="en-IN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex"><title>Enquiry not sent | Sreejith Digital</title></head><body style="font-family:system-ui,sans-serif;max-width:40rem;margin:4rem auto;padding:0 1rem;line-height:1.6"><h1>Your enquiry wasn’t sent</h1><p>Please email <a href="mailto:hello@sreejithdigital.com">hello@sreejithdigital.com</a> with your website and goal, or go back and try again.</p><p><a href="/contact/">Back to the contact page</a></p></body></html>`;
  return new Response(html, { status, headers: { "Content-Type": "text/html; charset=utf-8", "Cache-Control": "no-store" } });
}
