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
    if (url.pathname.startsWith("/api/")) {
      return json({ ok: false, code: "not_found" }, 404);
    }
    return env.ASSETS.fetch(request);
  },
};

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
