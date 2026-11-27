#!/usr/bin/env python3
"""Generate the static HTML website for sreejithdigital.com.

The generated files are committed to public/, which is the static asset
directory used by both Cloudflare Workers static assets and Cloudflare Pages.
Run this script from anywhere to regenerate every page and the sitemap:

    python3 scripts/generate_site.py
"""

from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = REPO_ROOT / "public"
BASE_URL = "https://sreejithdigital.com"
SITE_NAME = "Sreejith Digital"
CONTACT_EMAIL = "hello@sreejithdigital.com"
LAST_UPDATED = "2026-11-27"
SITE_VERSION = "2026-11-27.5"
DEFAULT_DESCRIPTION = (
    "SEO expert in India, based in Chennai. SEO services for technical, "
    "local and AI search — with dated client results, not ranking promises."
)

# ---------------------------------------------------------------------------
# Owner / entity details. Only confirmed facts go here; optional lists render
# nothing while they are empty, so no placeholder ever reaches a live page.
# ---------------------------------------------------------------------------
OWNER_NAME = "Sreejith CU"  # as credited publicly on client work ("Site by Sreejith CU")
OWNER_JOB_TITLE = "SEO consultant"
OWNER_BASE_CITY = "Chennai"
OWNER_ORIGIN = "Thrissur, Kerala"  # owner-confirmed home town, 27 Nov 2026
OWNER_PHOTO = ""  # e.g. "/assets/img/sreejith-cu.jpg" once a real headshot is added
OWNER_PROFILES: list[str] = []  # verified profile URLs, e.g. LinkedIn — feeds schema sameAs + About page
OWNER_LANGUAGES: list[str] = ["English", "Malayalam"]  # owner-confirmed 27 Nov 2026
OWNER_KNOWS_ABOUT = [
    "Search engine optimization",
    "Technical SEO",
    "Local SEO",
    "Structured data",
    "Generative engine optimization",
    "Answer engine optimization",
    "Multi-location SEO",
    "Web analytics",
]

# Work history, newest first. Add employers and projects only once confirmed.
EXPERIENCE: list[dict] = [
    {
        "period": "2026 – present",
        "role": "SEO, website and release lead",
        "org": "Mindtech Solutions — MEP, HVAC and fit-out contractor",
        "summary": (
            "Run search strategy, the website, privacy-safe lead tracking and "
            "production releases for a contractor working across India. Results "
            "include page-1 Google positions in Bengaluru and Delhi NCR and a "
            "national Google AI Overview citation."
        ),
        "href": "/case-studies/mindtech-solutions-mep-seo/",
    },
]

# Analytics stay off until an ID is added AND a visitor opts in (consent banner).
# Google Tag Manager is the single loader: GA4 (G-EP5M7JTRXK), Microsoft Clarity
# (zkbxk7xkbk) and future Google Ads conversion tags live in the GTM container.
# Leave GA4_MEASUREMENT_ID and CLARITY_PROJECT_ID empty while GTM is set, or
# those tools would load twice.
GTM_CONTAINER_ID = "GTM-K4MJL3SM"
GA4_MEASUREMENT_ID = ""  # direct-load fallback only, e.g. "G-XXXXXXXXXX"
CLARITY_PROJECT_ID = ""  # direct-load fallback only, e.g. "abcd1234ef"

# Enquiries POST here (Cloudflare Worker in worker/index.js). If the endpoint is
# not configured yet, main.js falls back to preparing an email instead.
ENQUIRY_ENDPOINT = "/api/enquiry"

OG_IMAGE = "/assets/img/og-image.png"
PERSON_ID = BASE_URL + "/about/#person"
BUSINESS_ID = BASE_URL + "/#business"
WEBSITE_ID = BASE_URL + "/#website"
CASE_STUDY_URL = "/case-studies/mindtech-solutions-mep-seo/"
RESULTS_DATE = "6 November 2026"
AI_CITATION_DATE = "25 November 2026"

# Dated, publicly observable Google positions for the client (Google India).
CLIENT_RANKINGS = [
    {"term": "Retail fit-out contractor", "city": "Bengaluru", "position": 1},
    {"term": "MEP contractor", "city": "Bengaluru", "position": 3},
    {"term": "MEP contractor", "city": "Delhi NCR", "position": 4},
    {"term": "Fire protection contractor", "city": "Bengaluru", "position": 5},
    {"term": "HVAC contractor", "city": "Bengaluru", "position": 8},
]
CLIENT_NOT_YET = [
    "Electrical contractor (Bengaluru)",
    "AC / HVAC AMC (Bengaluru)",
    "Building automation / BMS (Bengaluru)",
    "MEP contractor (Hyderabad)",
    "MEP contractor (Chennai)",
    "Google map pack (any city)",
]


def e(value: object) -> str:
    return escape(str(value), quote=True)


SERVICES = [
    {
        "slug": "seo-services",
        "name": "SEO Services",
        "short": "A connected organic growth programme, from diagnosis to delivery.",
        "description": "End-to-end SEO services that connect technical health, search intent, content, and measurement.",
        "intro": (
            "A complete organic search programme for teams that want one clear "
            "roadmap instead of disconnected audits and one-off fixes."
        ),
        "audience": "Growing teams that need strategy and hands-on execution in one engagement.",
        "included": [
            ("Search demand map", "Map priority topics to intent, funnel stage, and the pages that should own them."),
            ("Technical foundation", "Resolve crawl, indexation, page experience, and site architecture friction."),
            ("On-page improvement", "Refine titles, headings, internal links, and conversion paths on priority pages."),
            ("Content roadmap", "Turn gaps and opportunities into briefs your team can actually publish against."),
            ("Measurement", "Define meaningful conversions and report what changed, why, and what comes next."),
        ],
        "deliverables": [
            "Prioritised 90-day roadmap",
            "Technical findings log with owners and impact",
            "Keyword-to-URL map and content briefs",
            "Monthly performance commentary",
        ],
        "process": [
            ("Discover", "Understand the business model, audience, current data, and constraints."),
            ("Diagnose", "Review technical health, search visibility, content, competitors, and analytics."),
            ("Prioritise", "Agree on a small set of high-confidence actions with clear ownership."),
            ("Improve", "Implement, QA, measure, and refine the roadmap in regular cycles."),
        ],
        "faq": [
            ("Do you guarantee rankings?", "No ethical consultant can guarantee a specific ranking. The work focuses on durable improvements, clear priorities, and measurable business outcomes."),
            ("Can you work with our in-house team?", "Yes. Engagements can be hands-on, advisory, or a mix of both depending on your execution capacity."),
        ],
    },
    {
        "slug": "seo-consulting",
        "name": "SEO Consulting",
        "short": "Senior-level direction for teams that already have execution capacity.",
        "description": "SEO consulting and advisory support for in-house marketing, product, and engineering teams.",
        "intro": (
            "Practical senior guidance for teams that can ship the work but need "
            "a sharper strategy, a second opinion, or a reliable decision framework."
        ),
        "audience": "In-house teams, founders, and agencies that need expertise without a full outsourced programme.",
        "included": [
            ("Strategy sessions", "Working sessions that turn ambiguous goals into a focused search plan."),
            ("Objective audit", "An unbiased review of current performance, technical debt, and content gaps."),
            ("Migration guidance", "Risk reviews and launch checklists for redesigns, replatforms, and domain changes."),
            ("Stakeholder alignment", "Documentation that helps marketing, engineering, and leadership make the same decisions."),
            ("Quality assurance", "Review implementations before they reach production."),
        ],
        "deliverables": [
            "Written opportunity assessment",
            "Quarterly priority framework",
            "Decision log and implementation checklist",
            "Optional workshop recordings or notes",
        ],
        "process": [
            ("Align", "Clarify commercial goals, team structure, and the decisions that need support."),
            ("Review", "Inspect data, site architecture, content, and current ways of working."),
            ("Recommend", "Present options with trade-offs rather than a generic best-practice list."),
            ("Support", "Stay available for implementation questions, QA, and monthly recalibration."),
        ],
        "faq": [
            ("Is this a retainer?", "It can be. Advisory support is usually most useful as a recurring monthly or quarterly engagement."),
            ("Will you write every brief?", "The scope is flexible. Some teams want strategy only; others want briefs and implementation review too."),
        ],
    },
    {
        "slug": "local-seo",
        "name": "Local SEO",
        "short": "Make location-led searches easier to find, trust, and convert.",
        "description": "Local SEO for service-area businesses and multi-location teams, including profiles, pages, and reputation signals.",
        "intro": (
            "Build a consistent local presence across search results, map surfaces, "
            "business profiles, and well-structured location pages."
        ),
        "audience": "Businesses that serve defined cities, regions, or a network of physical locations.",
        "included": [
            ("Profile review", "Improve category, service, content, and conversion details on business profiles."),
            ("Location architecture", "Design useful city and service-area pages instead of thin duplicated templates."),
            ("Consistency checks", "Review name, address, phone, and citation consistency across priority listings."),
            ("Review workflow", "Create a practical, policy-aware process for earning and responding to reviews."),
            ("Local structured data", "Add appropriate schema and verify key business information."),
        ],
        "deliverables": [
            "Location page blueprint",
            "Business profile action list",
            "Citation and consistency audit",
            "Review request workflow",
        ],
        "process": [
            ("Map", "Catalogue locations, service areas, profiles, and current local visibility."),
            ("Standardise", "Fix the business data and page structure that everything else depends on."),
            ("Build", "Create genuinely useful local pages and supporting trust signals."),
            ("Maintain", "Set a light cadence for profile updates, reviews, and location performance."),
        ],
        "faq": [
            ("Do you need a physical office in each city?", "No. Service-area businesses can build useful location relevance without pretending to have offices they do not operate."),
            ("Can one page target every city?", "Usually not. Distinct, genuinely useful pages perform better than a single page with a list of swapped city names."),
        ],
    },
    {
        "slug": "google-ads-management",
        "name": "Google Ads Management",
        "short": "Capture existing demand without wasting spend on unclear intent.",
        "description": "Google Ads management focused on account structure, conversion quality, landing pages, and useful reporting.",
        "intro": (
            "Paid search works best when it is connected to a clear offer, reliable "
            "conversion data, and what you are learning from organic search."
        ),
        "audience": "Teams that need immediate demand capture or a cleaner, more accountable paid search account.",
        "included": [
            ("Account structure", "Organise campaigns around intent, margin, geography, and manageable budgets."),
            ("Query management", "Use search-term evidence to refine keywords, negatives, and match types."),
            ("Creative testing", "Write and test ads that match the promise on the landing page."),
            ("Conversion tracking", "Separate meaningful enquiries from low-value form fills and accidental clicks."),
            ("Landing page feedback", "Recommend changes to message match, page speed, and conversion friction."),
        ],
        "deliverables": [
            "Account build or cleanup plan",
            "Keyword and negative-keyword framework",
            "Conversion measurement checklist",
            "Monthly budget and performance commentary",
        ],
        "process": [
            ("Audit", "Review current campaigns, conversion data, landing pages, and wasted spend."),
            ("Rebuild", "Create a structure that makes intent and budget decisions easy to understand."),
            ("Launch", "Validate tracking, ads, targeting, and landing page experience."),
            ("Optimise", "Use clean query and conversion evidence to refine the account."),
        ],
        "faq": [
            ("Do you manage ad spend?", "Budget ownership and billing stay with the client. Recommendations and management cover the account configuration and optimisation."),
            ("Can paid and SEO share insights?", "Yes. Query data, conversion language, and landing page learning are useful across both channels."),
        ],
    },
    {
        "slug": "website-design",
        "name": "Website Design",
        "short": "Fast, clear websites designed around search intent and action.",
        "description": "SEO-aware website design and static front-end builds with clear information architecture and conversion paths.",
        "intro": (
            "A website should make the next step obvious, load quickly, and give "
            "both people and search engines a clean structure to understand."
        ),
        "audience": "Teams planning a new site, a redesign, or a lightweight static marketing site.",
        "included": [
            ("Information architecture", "Define a page structure that reflects services, audiences, and search demand."),
            ("Wireframes", "Plan hierarchy, proof, calls to action, and content before visual polish."),
            ("Responsive interface", "Build accessible layouts that work across desktop, tablet, and mobile."),
            ("Static implementation", "Ship fast HTML, CSS, and minimal JavaScript with no unnecessary dependencies."),
            ("Launch readiness", "Check metadata, redirects, canonical tags, analytics hooks, and Core Web Vitals basics."),
        ],
        "deliverables": [
            "Sitemap and page hierarchy",
            "Responsive design system",
            "Production-ready static HTML/CSS",
            "Pre-launch SEO and QA checklist",
        ],
        "process": [
            ("Define", "Agree on audiences, offers, pages, and the action each page should encourage."),
            ("Design", "Create a visual language and layout system around clarity and speed."),
            ("Build", "Implement accessible, responsive static templates."),
            ("Launch", "Verify redirects, metadata, forms, performance, and indexing."),
        ],
        "faq": [
            ("Do you work with a CMS?", "The static build can be handed off for CMS integration, or used as the design and front-end specification."),
            ("Will a redesign hurt SEO?", "It can. A redirect map, content inventory, and launch QA reduce that risk substantially."),
        ],
    },
    {
        "slug": "technical-seo",
        "name": "Technical SEO",
        "short": "Remove the crawl, indexing, and performance friction holding pages back.",
        "description": "Technical SEO audits and implementation guidance for crawlability, indexation, speed, schema, and migrations.",
        "intro": (
            "Strong content cannot compensate for a site that search engines struggle "
            "to crawl, render, understand, or confidently index."
        ),
        "audience": "Large sites, complex templates, JavaScript-heavy pages, and teams preparing a migration.",
        "included": [
            ("Crawl review", "Analyse crawl paths, internal links, robots directives, sitemaps, and status codes."),
            ("Indexation", "Find duplication, parameter issues, canonical conflicts, and thin template pages."),
            ("Rendering", "Check whether important content and links are available to search engines."),
            ("Performance", "Prioritise page speed and Core Web Vitals fixes with practical engineering notes."),
            ("Structured data", "Review schema coverage, validity, and whether it matches visible page content."),
        ],
        "deliverables": [
            "Technical issue register with severity and owner",
            "Crawl and indexation findings",
            "Template-level recommendations",
            "Migration risk and launch checklist",
        ],
        "process": [
            ("Collect", "Gather crawl data, Search Console evidence, analytics, templates, and architecture notes."),
            ("Validate", "Reproduce issues and separate symptoms from root causes."),
            ("Specify", "Write implementation-ready recommendations with acceptance criteria."),
            ("Verify", "Retest after release and confirm the expected change in search-engine signals."),
        ],
        "faq": [
            ("Is an automated audit enough?", "Automated tools are useful for evidence, but prioritisation and root-cause analysis still need human review."),
            ("Can you work with developers?", "Yes. Findings can be written as implementation-ready tickets for engineering teams."),
        ],
    },
    {
        "slug": "content-strategy",
        "name": "Content Strategy",
        "short": "Turn search demand into an editorial system your team can maintain.",
        "description": "Search-led content strategy covering topic clusters, intent mapping, briefs, internal links, and content refreshes.",
        "intro": (
            "Publishing more is rarely the answer. A useful content strategy makes "
            "each page's job, audience, and connection to the wider site explicit."
        ),
        "audience": "Content and marketing teams that need a defensible publishing plan rather than a list of keywords.",
        "included": [
            ("Content audit", "Decide what to keep, improve, consolidate, or remove."),
            ("Topic clusters", "Group related demand around clear pillar and supporting pages."),
            ("Intent mapping", "Match pages to research, comparison, decision, and support intent."),
            ("Editorial briefs", "Give writers search evidence, structure, questions, and internal-link targets."),
            ("Refresh cycle", "Set a practical cadence for updating pages that already earn visibility."),
        ],
        "deliverables": [
            "Content inventory with actions",
            "Topic cluster and keyword-to-URL map",
            "Reusable brief template",
            "Quarterly publishing and refresh plan",
        ],
        "process": [
            ("Inventory", "Understand what exists, what performs, and what creates overlap."),
            ("Model", "Define clusters, page roles, and the internal links that connect them."),
            ("Brief", "Convert research into clear instructions for writers and designers."),
            ("Review", "Measure outcomes and refresh rather than endlessly adding new pages."),
        ],
        "faq": [
            ("Do you write the content?", "Writing can be included, but many teams use the strategy and briefs with their own writers."),
            ("How many articles should we publish?", "The right cadence depends on quality, capacity, and the opportunity. A maintainable plan beats an aggressive one."),
        ],
    },
    {
        "slug": "analytics-reporting",
        "name": "Analytics & Reporting",
        "short": "Connect search work to decisions, conversions, and commercial outcomes.",
        "description": "Analytics and reporting setup for SEO, including conversion definitions, dashboards, and decision-focused commentary.",
        "intro": (
            "Reporting should explain what changed and what to do next—not bury the "
            "team in screenshots, vanity metrics, and unexplained charts."
        ),
        "audience": "Teams that need trustworthy numbers and a shared view of what organic search contributes.",
        "included": [
            ("Measurement model", "Define primary conversions, supporting events, and the questions reports should answer."),
            ("Tracking review", "Check analytics, Search Console, tag behaviour, and conversion quality."),
            ("Dashboard design", "Build a concise view of visibility, engagement, conversions, and work completed."),
            ("Attribution context", "Document what the data can and cannot prove."),
            ("Monthly commentary", "Turn movement into decisions, owners, and next actions."),
        ],
        "deliverables": [
            "Measurement definitions document",
            "Tracking QA checklist",
            "Decision-focused dashboard",
            "Monthly insight and action notes",
        ],
        "process": [
            ("Define", "Agree on business outcomes and the evidence needed to evaluate them."),
            ("Instrument", "Validate events, conversions, and source data."),
            ("Visualise", "Create a compact dashboard with consistent definitions."),
            ("Interpret", "Add context and recommendations, not just automated charts."),
        ],
        "faq": [
            ("Which dashboard tool do you use?", "The setup can work with widely used analytics products. The measurement model matters more than the specific tool."),
            ("Can SEO revenue be attributed exactly?", "Rarely. Good reporting combines reliable conversion data with honest context about assisted journeys and external factors."),
        ],
    },
]

SERVICES.append(
    {
        "slug": "ai-search-optimization",
        "name": "AI Search Optimisation (AEO & GEO)",
        "short": "Be the business AI Overviews, ChatGPT and Perplexity can find, understand and cite.",
        "description": "AI search optimisation for Google AI Overviews, AI Mode, ChatGPT and Perplexity: entity clarity, answer-first content, crawl access and citations.",
        "intro": (
            "AI answers are built from the same web search engines already index. The work "
            "is making your business easy to identify, easy to quote and present in the "
            "sources AI systems trust."
        ),
        "audience": "Businesses with sound SEO basics that want to appear in AI Overviews and assistant answers for their category.",
        "included": [
            ("Entity clarity", "One consistent name, description and set of profiles, with Organization or Person structured data that matches the visible page."),
            ("Answer-first content", "Direct 40–60-word answers to the questions buyers ask, followed by detail, tables and visible FAQs."),
            ("Crawl access", "Confirm search and citation bots (Googlebot, Bingbot, OAI-SearchBot, PerplexityBot) are not blocked by robots.txt or CDN bot settings."),
            ("Citation sources", "Earn listings where AI answers draw from — credible directories, industry lists and review profiles — without self-ranking ‘top 10’ pages."),
            ("Measurement", "Track AI Overview and AI Mode appearances in Search Console, AI referrals in analytics and a fixed monthly prompt set."),
        ],
        "deliverables": [
            "AI visibility baseline (prompt set + Search Console)",
            "Entity and structured-data fix list",
            "Citation-source target list",
            "Monthly AI visibility log",
        ],
        "process": [
            ("Baseline", "Record how AI answers describe you and your competitors today, with dates."),
            ("Clarify", "Fix entity details, schema and on-page answers so your business is unambiguous."),
            ("Corroborate", "Earn mentions in the third-party sources those answers actually cite."),
            ("Measure", "Re-run the same prompts monthly and track AI referrals and Search Console data."),
        ],
        "faq": [
            ("Is AI search optimisation different from SEO?", "Mostly not. Google’s own guidance (May 2026) says optimising for its generative AI features is still SEO and needs no special files or markup. What changes is emphasis: entity clarity and third-party corroboration matter more."),
            ("Does an llms.txt file help?", "There is no measurable evidence yet. A study of roughly 300,000 domains found no relationship between having llms.txt and being cited by AI systems. It is harmless, but it is not where results come from."),
            ("Can you guarantee an AI Overview citation?", f"No. What I can show is a client cited in Google’s AI Overview for “MEP contractors in India” alongside national firms ({AI_CITATION_DATE}), and the method behind it."),
        ],
    }
)

SERVICE_ORDER = [
    "seo-consulting",
    "technical-seo",
    "local-seo",
    "ai-search-optimization",
    "seo-services",
    "content-strategy",
    "analytics-reporting",
    "google-ads-management",
    "website-design",
]
SERVICES.sort(key=lambda item: SERVICE_ORDER.index(item["slug"]))

# Answer-first block shown at the top of each service page (40–60 words).
SERVICE_ANSWERS = {
    "seo-services": "SEO services cover the whole programme: fixing what stops Google crawling and trusting your site, giving each page one clear search intent, improving content and internal links, and measuring enquiries rather than traffic. Expect first movement in two to four months; competitive terms take longer.",
    "seo-consulting": "SEO consulting gives your team senior direction without outsourcing the work: a senior-led audit, a prioritised roadmap, review before changes go live, and help when a decision is unclear. It suits teams that already have developers or writers but need someone accountable for search decisions.",
    "local-seo": "Local SEO makes a business easy to find for searches in a specific place: a complete Google Business Profile if you meet customers in person, one genuinely useful page per real service area, consistent business details across listings, and a steady flow of honest reviews.",
    "technical-seo": "Technical SEO removes the reasons Google can’t crawl, render or confidently index your pages: broken internal links, duplicate URLs, wrong canonicals, slow templates, blocked resources and schema that doesn’t match the page. The output is a ranked fix list your developers can ship and verify.",
    "ai-search-optimization": "AI search optimisation helps Google AI Overviews, AI Mode, ChatGPT and Perplexity identify your business and cite it. Google says it is still SEO; the emphasis shifts to an unambiguous entity, direct answers on your pages, open crawl access for search bots and mentions in the sources AI answers draw on.",
    "content-strategy": "Content strategy decides which pages should exist, what each one is for and how they link together, then turns that into briefs your team can publish. The goal is fewer, stronger pages that each own a clear search intent, refreshed on a schedule instead of endlessly added to.",
    "analytics-reporting": "SEO reporting should answer three questions: what changed, why, and what to do next. That needs Search Console and analytics set up properly, enquiries tracked as conversions with consent, and a short monthly note — not an export of forty charts.",
    "google-ads-management": "Google Ads management captures demand that already exists while SEO builds: tightly themed search campaigns, negative keywords that filter out job-seekers and course-buyers, landing pages that match the ad, and conversion tracking that counts real enquiries. Budget and billing stay with you.",
    "website-design": "An SEO-ready website is built around the pages buyers need, not a template: a clear hierarchy, fast static pages, structured data, redirects planned before launch and a contact path that actually reaches you. Launch is the cheapest moment to get SEO right.",
}

# Services that can point to the published case study as evidence.
SERVICE_PROOF = {
    "seo-services": "The full programme — technical fixes, money-page rewrites, proof and tracking — took an MEP contractor from brand-only visibility to page 1 for five commercial terms.",
    "technical-seo": "Indexation checks, schema that mirrors visible text and validated releases were the foundation of an MEP contractor’s move to page 1.",
    "local-seo": "One page per service intent and city, each passing a city-name test, put an MEP contractor on page 1 in Bengaluru and Delhi NCR.",
    "ai-search-optimization": "An MEP contractor was cited in Google’s AI Overview for “MEP contractors in India”, listed alongside national firms.",
    "seo-consulting": "Strategy, prioritisation and release review for an MEP contractor’s multi-city programme, documented decision by decision.",
    "analytics-reporting": "Consent-based GA4 and Clarity, a reference on every enquiry and source fields — verified end to end with controlled test enquiries.",
    "website-design": "The client site behind the case study: a design system, structured data across the site and releases with automated checks and rollback.",
}

INDUSTRIES = [
    {
        "slug": "b2b-saas",
        "name": "B2B & SaaS",
        "short": "Search programmes for long buying cycles and considered decisions.",
        "description": "SEO and content architecture for B2B and SaaS teams with multiple stakeholders and long evaluation cycles.",
        "intro": "Help buyers move from problem awareness to confident evaluation without relying on a single demo page.",
        "challenges": [
            "Product, feature, comparison, and problem-led queries often compete for the same URLs.",
            "Multiple stakeholders need different proof before a sales conversation starts.",
            "Content teams can publish frequently without a clear cluster or internal-link model.",
            "Attribution is rarely linear, so reporting needs more than last-click conversions.",
        ],
        "approach": [
            ("Map the buying committee", "Separate the questions asked by practitioners, managers, and budget owners."),
            ("Structure the site", "Give product, solution, comparison, and educational pages distinct jobs."),
            ("Build useful proof", "Connect claims to documentation, implementation detail, and realistic use cases."),
        ],
        "services": ["content-strategy", "technical-seo", "analytics-reporting"],
    },
    {
        "slug": "professional-services",
        "name": "Professional Services",
        "short": "Build trust and qualified enquiries around expertise-led searches.",
        "description": "Search strategy for consultants, agencies, legal, finance, and other expertise-led professional service firms.",
        "intro": "Make expertise visible, specific, and easy to verify before a prospective client makes contact.",
        "challenges": [
            "Generic service pages make different firms look interchangeable.",
            "Expertise often lives in people’s heads instead of structured, useful pages.",
            "Local and national intent can conflict without a deliberate page hierarchy.",
            "Enquiry forms frequently lack the context needed to qualify a lead.",
        ],
        "approach": [
            ("Clarify the offer", "Define services, outcomes, and fit in plain language."),
            ("Show the thinking", "Build resource pages around the questions clients ask before hiring."),
            ("Remove friction", "Align calls to action, forms, and measurement with qualified enquiries."),
        ],
        "services": ["seo-services", "local-seo", "website-design"],
    },
    {
        "slug": "ecommerce",
        "name": "Ecommerce",
        "short": "Cleaner category architecture and product discovery across large catalogues.",
        "description": "Technical and category-led SEO for ecommerce sites with filters, variants, and constantly changing inventory.",
        "intro": "Make the right categories discoverable while keeping crawl demand and duplicate pages under control.",
        "challenges": [
            "Faceted navigation can generate large numbers of low-value crawlable URLs.",
            "Category, product, and editorial content often overlap in search results.",
            "Out-of-stock and discontinued products need deliberate handling.",
            "Product data changes faster than manually maintained SEO guidance.",
        ],
        "approach": [
            ("Control templates", "Set indexation, canonical, and internal-link rules at template level."),
            ("Prioritise categories", "Map commercial demand to the category pages that can genuinely serve it."),
            ("Connect content", "Use buying guides and helpful editorial pages to support product discovery."),
        ],
        "services": ["technical-seo", "content-strategy", "analytics-reporting"],
    },
    {
        "slug": "local-multi-location",
        "name": "Local & Multi-location",
        "short": "Consistent local visibility without thin, duplicated city pages.",
        "description": "Local search architecture for service-area businesses and organisations with several locations.",
        "intro": "Give every legitimate location a useful page and a consistent set of trust signals.",
        "challenges": [
            "Location pages are often duplicates with only the city name changed.",
            "Business profiles, citations, and site data drift out of sync.",
            "Teams struggle to maintain reviews and local content across locations.",
            "Reporting rarely separates location-level performance from national visibility.",
        ],
        "approach": [
            ("Design the hierarchy", "Connect a location hub, individual locations, and relevant service pages."),
            ("Standardise data", "Create one source of truth for business information and profile details."),
            ("Add local substance", "Include genuinely location-specific services, proof, and next steps."),
        ],
        "services": ["local-seo", "website-design", "analytics-reporting"],
    },
]

INDUSTRIES.insert(
    0,
    {
        "slug": "construction-mep-contractors",
        "name": "Construction & MEP Contractors",
        "short": "Multi-city service pages, project proof and approvals content for contractors.",
        "description": "SEO for MEP, HVAC, fire protection, electrical and fit-out contractors: service and city architecture, project proof, approvals content and enquiry tracking.",
        "intro": "Contractors win on proof and coverage. Search should show which services you deliver, in which cities, with which projects behind them — without a stack of copy-paste city pages.",
        "challenges": [
            "Every service × city combination looks like a page to build, and most of them turn into near-duplicates.",
            "Project proof sits in brochures and WhatsApp groups instead of on the pages buyers read.",
            "Buyers worry about approvals — fire NOCs, electrical inspectorate sign-off, load sanctions — but contractor sites rarely explain them.",
            "Enquiries arrive by phone and email with no record of which page or search produced them.",
        ],
        "approach": [
            ("Build only distinct pages", "Apply the city-name test: if swapping the city name leaves the page true, it is not ready to publish."),
            ("Put proof beside claims", "Approved project cards, certifications and video on the page that makes the claim, with matching structured data."),
            ("Track real enquiries", "Consent-based analytics, a reference on every enquiry and source fields, so you know which pages produce RFQs."),
        ],
        "services": ["local-seo", "technical-seo", "ai-search-optimization"],
        "proof": True,
    },
)

LOCATIONS = [
    {
        "slug": "bengaluru",
        "name": "Bengaluru",
        "status": "Client results",
        "status_key": "results",
        "title": "SEO Expert in Bengaluru | Sreejith Digital",
        "description": "SEO consultant with page-1 client results in Bengaluru: an MEP contractor reached #1, #3, #5 and #8 on Google for commercial terms (Nov 2026).",
        "h1": "SEO expert in Bengaluru",
        "lede": "Bengaluru is where my client results are strongest. An MEP contractor’s Bengaluru pages reached Google’s first page for four commercial terms within about three months of the recorded baseline.",
        "short": "Where my client results are strongest: four page-1 positions, including #1.",
        "delivery": "Remote delivery from Chennai",
        "results_city": "Bengaluru",
        "context_heading": "What Bengaluru search rewards",
        "context": [
            "Bengaluru is India’s largest technology and startup market and one of its largest office markets. Commercial searches here are crowded with capable competitors, so generic service pages rarely win; specific proof does.",
            "Spelling matters more than people expect. Buyers search both “Bangalore” and “Bengaluru”. The client pages below use “Bangalore” in their titles because that is how most of their buyers search — your own Search Console queries should make that call for your business, not a guess.",
            "B2B buyers in the city research longer and compare vendors side by side, so a page has to carry its evidence — projects, certifications, process — right next to each claim.",
        ],
        "work_heading": "Work connected to Bengaluru",
        "work": [
            "The positions below belong to Mindtech Solutions, an MEP, HVAC and fit-out contractor whose Bengaluru projects are its strongest proof. The method — one page per service intent, approved project proof beside each claim, contextual internal links and structured data that mirrors the visible page — is written up step by step in the case study.",
            "Not on page 1 yet in the same check: electrical, AC AMC and building-automation (BMS) terms. Those are the next pages to strengthen, and they will be reported here when they move.",
        ],
        "engage_heading": "Working with Bengaluru teams",
        "engage": [
            "Remote-first delivery with scheduled calls and shared documents",
            "Audits start from what already earns impressions in Search Console",
            "Release-ready recommendations your developers can ship",
        ],
        "faqs": [
            ("Should my pages say Bangalore or Bengaluru?", "Use both naturally: the official name and the one many buyers still type. Let your Search Console queries decide which one leads in the title. For the client in the case study, “Bangalore” leads because that is how their buyers search."),
            ("How did the client reach page 1 that quickly?", "No shortcuts: technical foundations first, one page per service intent, approved project proof next to the claims, contextual internal links and careful releases. The full sequence, with dates, is in the case study."),
            ("Do you have an office in Bengaluru?", "No. I’m based in Chennai and work with Bengaluru businesses remotely. I won’t list a local address I don’t operate — it is a trust risk and a Google Business Profile risk."),
        ],
        "services": ["local-seo", "technical-seo", "seo-consulting"],
        "industries": ["construction-mep-contractors", "b2b-saas"],
    },
    {
        "slug": "delhi-ncr",
        "name": "Delhi NCR",
        "status": "Client results",
        "status_key": "results",
        "title": "SEO Expert in Delhi NCR — Delhi, Gurugram, Noida",
        "description": "SEO for Delhi NCR businesses with one regional strategy for Delhi, Gurugram and Noida. A client MEP page reached #4 on Google for its main NCR term (Nov 2026).",
        "h1": "SEO expert in Delhi NCR",
        "lede": "Delhi NCR is a region, not a city: Delhi, Gurugram and Noida sit in three different states. My client’s Delhi NCR page reached #4 on Google for its main term with one regional page — not three thin city pages.",
        "short": "One regional page, #4 on Google for the client’s main NCR term.",
        "delivery": "Remote delivery from Chennai",
        "results_city": "Delhi NCR",
        "context_heading": "Why NCR needs a regional plan",
        "context": [
            "NCR spans the National Capital Territory of Delhi; Gurugram and Faridabad in Haryana; and Noida, Greater Noida and Ghaziabad in Uttar Pradesh. Registrations, approvals and even useful local directories differ by state.",
            "Search behaviour splits the same way. People type “Delhi NCR”, “Delhi”, “Gurgaon” or “Gurugram”, and “Noida” — and the old name Gurgaon is still searched widely years after the 2016 rename. A regional page should acknowledge each one, naturally.",
            "Corporate headquarters cluster in Gurugram, IT and media in Noida, and government and trade in Delhi, so the same service can have very different buyers across the region.",
        ],
        "work_heading": "Work connected to Delhi NCR",
        "work": [
            "The #4 position came from Mindtech Solutions’ Delhi NCR page: one regional page covering Delhi, Gurugram and Noida. The client has no published Delhi project yet, and the page says so plainly. It ranks on clarity, structure and proof from other cities — not on invented local claims.",
            "That is the approach I recommend for most businesses targeting NCR: start with one strong regional page and split a city out only when its own demand and its own content justify it.",
        ],
        "engage_heading": "Working with NCR businesses",
        "engage": [
            "One regional page first, city pages only when earned",
            "Query reports split by Delhi, Gurugram/Gurgaon and Noida",
            "Remote delivery with scheduled calls",
        ],
        "faqs": [
            ("One NCR page, or separate Delhi, Gurugram and Noida pages?", "Start with one regional page. Split a city out only when it has its own demand in Search Console, content that would be false for the other cities, and proof to show. Three near-identical pages is the classic doorway pattern."),
            ("Gurgaon or Gurugram?", "Use both naturally: the official name and the one people still type. Your own query data should decide which leads in the title."),
            ("Do I need a Delhi office to rank in NCR?", "No. You need to be honest about where you work and useful to people searching there. A fake local address puts your Google Business Profile and your credibility at risk."),
        ],
        "services": ["local-seo", "seo-consulting", "content-strategy"],
        "industries": ["construction-mep-contractors", "professional-services"],
    },
    {
        "slug": "hyderabad",
        "name": "Hyderabad",
        "status": "In progress",
        "status_key": "progress",
        "title": "SEO Expert in Hyderabad | Sreejith Digital",
        "description": "Remote SEO consulting for Hyderabad and Secunderabad businesses: technical SEO, B2B search and honest, dated reporting on work in progress.",
        "h1": "SEO expert in Hyderabad",
        "lede": "Hyderabad is active in my client work right now: a dedicated page built on the client’s Telangana projects. It is not on page 1 yet, and this page will say so until it is.",
        "short": "Active client work, not on page 1 yet — reported honestly.",
        "delivery": "Remote delivery from Chennai",
        "results_city": "",
        "context_heading": "How Hyderabad searches",
        "context": [
            "Hyderabad’s commercial searches cluster around a few strong sectors: the HITEC City–Gachibowli technology corridor, pharmaceuticals and life sciences around Genome Valley, and fast-growing residential and commercial real estate.",
            "People search by twin city and by area — Hyderabad or Secunderabad, then Gachibowli, Madhapur, Kondapur or Kukatpally. For most businesses one strong Hyderabad page with clear area coverage beats a page for every locality.",
            "Telangana and Andhra Pradesh have had separate administrations since 2014, so content about approvals, regulations or “AP & Telangana” coverage has to be precise about which state it means.",
        ],
        "work_heading": "Work connected to Hyderabad",
        "work": [
            f"My MEP-contractor client’s Hyderabad page covers its projects across Telangana. In the {RESULTS_DATE} check it had not reached page 1.",
            "At this stage the work is strengthening proof and internal links from the client’s stronger pages — not publishing more Hyderabad pages. When the page moves, the position and date will appear here.",
        ],
        "engage_heading": "Working with Hyderabad teams",
        "engage": [
            "Remote-first delivery with scheduled calls",
            "One city page with area coverage before any locality pages",
            "Dated progress reporting, including what hasn’t moved yet",
        ],
        "faqs": [
            ("Why list a city where results aren’t in yet?", "Because it is true and it is useful. You can see the method working in other cities and judge the Hyderabad stage honestly."),
            ("Should I target Hyderabad and Secunderabad separately?", "Usually not. Cover both on one strong page unless Search Console shows separate demand and you have genuinely different things to say about each."),
            ("Is Telugu content worth creating?", "For commercial B2B services, English still dominates search. For consumer and local services it can help — check your query data before translating anything."),
        ],
        "services": ["technical-seo", "local-seo", "content-strategy"],
        "industries": ["construction-mep-contractors", "b2b-saas"],
    },
    {
        "slug": "chennai",
        "name": "Chennai",
        "status": "Home base",
        "status_key": "home",
        "title": "SEO Expert in Chennai | Sreejith Digital",
        "description": "SEO expert in Chennai offering SEO services to local, B2B and manufacturing firms: a senior specialist you work with directly, not an agency account team, and easy to meet in person.",
        "h1": "SEO expert in Chennai",
        "lede": "I’m based in south Chennai, on the GST Road side of the city. Chennai clients get the same method as everyone else — plus a consultant in the same city.",
        "short": "My home base, with meetings possible when a project needs one.",
        "delivery": "Based in Chennai",
        "results_city": "",
        "context_heading": "How Chennai searches differ",
        "context": [
            "Chennai is not one market. Automotive and electronics manufacturing along the Sriperumbudur–Oragadam belt, IT and services along OMR, hospitals and colleges, and thousands of family-run trading and service firms all search — and buy — differently.",
            "Manufacturers and industrial suppliers usually need B2B pages that answer a buyer’s specification questions. Clinics, schools and local services need Google Business Profile work and one strong location page. Treating them the same way is the most common Chennai SEO mistake I see.",
            "Buyers here often search by area — Velachery, Anna Nagar, T. Nagar, OMR, Tambaram. For most service businesses that calls for one strong Chennai page and well-chosen service areas on the business profile, not a separate page for every neighbourhood.",
        ],
        "work_heading": "Work connected to Chennai",
        "work": [
            f"Chennai is one of the cities in my MEP-contractor client’s programme; its Chennai page is built around the client’s logistics and fulfilment-centre work in the city. In the {RESULTS_DATE} check it was not yet on Google’s first page — Bengaluru is where that client’s results are strongest so far.",
            "I publish the misses as well as the wins. It is the only way a results page means anything.",
        ],
        "engage_heading": "Working together in Chennai",
        "engage": [
            "Same city and the same working day",
            "Meetings in person when a project genuinely needs one",
            "Close to Tambaram, Perungalathur, Vandalur and Guduvanchery on GST Road",
        ],
        "faqs": [
            ("Should I hire an SEO company in Chennai or a dedicated SEO expert?", "Chennai has many SEO companies, and an agency suits you if you want ads, social media, design and SEO handled by one team. A dedicated expert suits you if you want one accountable specialist leading the strategy and the hands-on SEO services. I’m based in south Chennai, and I lead the work myself."),
            ("Do you meet Chennai clients in person?", "Most work happens remotely because it is faster, but I’m based in Chennai, so a meeting is easy to arrange when a workshop, a site walk-through or a kick-off would help."),
            ("Does my Chennai business need a Google Business Profile?", "If you meet customers in person — at your premises or theirs — yes, and it is usually the fastest local win. If you only work online, Google’s guidelines make you ineligible, so the effort goes into your website and directories instead."),
            ("Should my site have Tamil pages?", "Not by default. Commercial service searches in Chennai are still mostly in English or Romanised Tamil, so check your Search Console queries first. Google’s AI Mode has supported Tamil since October 2025, so conversational Tamil questions are worth watching."),
        ],
        "services": ["local-seo", "technical-seo", "seo-consulting"],
        "industries": ["construction-mep-contractors", "professional-services"],
    },
    {
        "slug": "kerala",
        "name": "Kerala",
        "status": "Home state",
        "status_key": "home",
        "title": "SEO Expert in Kerala — Kochi, Trivandrum, Calicut",
        "description": "SEO expert from Thrissur, consulting in Malayalam or English, for Kochi, Trivandrum, Calicut, Thrissur, Malappuram, Kannur, Kollam and Palakkad.",
        "h1": "SEO expert in Kerala",
        "lede": "I’m from Thrissur and now work from Chennai, consulting in Malayalam or English. I know how Kerala businesses sell — often to people who are searching from somewhere else.",
        "short": "Where I’m from: a Kerala hub with pages for eight cities.",
        "delivery": "Remote delivery from Chennai",
        "results_city": "",
        "context_heading": "What makes Kerala search different",
        "context": [
            "Many Kerala businesses sell to people who are not in Kerala when they search: Malayalis in the Gulf looking at property, jewellery or schools back home, and domestic and foreign travellers planning stays and Ayurveda treatments weeks ahead. Targeting only “near me” searches misses that demand.",
            "That changes the work. Pages need to answer questions asked from abroad — prices, documents, visits — business details must stay consistent across every profile, and reporting should separate in-state enquiries from NRI and visitor enquiries.",
            "Healthcare, education, hospitality and real estate dominate commercial searches in the state, alongside exporters of spices, seafood and coir, and the IT parks in Thiruvananthapuram, Kochi and Kozhikode.",
        ],
        "work_heading": "Work connected to Kerala",
        "work": [
            "I don’t have a published Kerala client result yet, and I won’t invent one.",
            "What a Kerala business gets is the same method behind the results in my case study, from someone who understands the state’s businesses and its diaspora. When there is a Kerala result, it will be dated and shown here.",
        ],
        "engage_heading": "Working with Kerala businesses",
        "engage": [
            "Calls in Malayalam or English; meetings in Kerala when I travel",
            "City pages for eight Kerala cities; towns only where search demand exists",
            "Reporting that separates in-state, NRI and visitor enquiries",
        ],
        "faqs": [
            ("Who is the best SEO expert in Kerala?", "There is no official ranking, and lists in AI answers are assembled from websites and profiles, not verified results. Judge any SEO expert — including me — by dated results you can check: the page that ranked, the date it was recorded and what didn’t work."),
            ("How much does an SEO expert in Kerala cost?", "Published monthly packages from Kerala SEO providers I checked in November 2026 started between about ₹10,000 and ₹15,000, with larger plans up to ₹50,000; one agency advertised from ₹3,000. Compare what is included — technical fixes, content, reporting — not the price alone."),
            ("Should I hire an SEO company in Kerala or a dedicated SEO expert?", "An agency suits you if you need many services at once — ads, social media, design and SEO — handled by a team. A dedicated SEO expert suits you if you want one accountable specialist leading the strategy and the hands-on work. That is how I work: you deal with me directly, from audit to release."),
            ("What should I look for when hiring an SEO expert in Kerala?", "Dated results you can check — the search term, the page that ranked and the date — a written plan before any work starts, clarity on who does the work, honest timelines without ranking guarantees, and reporting tied to enquiries. Be wary of unverified “No. 1” claims and of Google Maps listings with keywords stuffed into the business name, which Google’s guidelines prohibit."),
            ("Can you improve my local Google rankings in Kerala?", "Local rankings depend mostly on your Google Business Profile, your reviews, your relevance and how close you are to the searcher. I fix the profile, build pages for the places you really serve and clean up listings elsewhere, then report Maps and organic positions separately. Nobody can promise a position; reviews from real customers matter most in the map pack."),
            ("Do you work with ecommerce businesses in Kerala?", "Yes. Kerala stores selling spices, handloom, Ayurveda products, snacks or jewellery usually need national rather than local SEO: category and product pages that can rank across India, product structured data, and fixing the crawl waste that filters and duplicate product URLs create."),
            ("Do you work with Kerala businesses remotely?", "Yes. Kerala clients work with me the same way Chennai and Bengaluru clients do — shared documents, scheduled calls in Malayalam or English and a written roadmap. I’m from Thrissur and based in Chennai, and I can meet in person when I travel to Kerala."),
            ("Should a Kerala business target NRI searches?", "If NRIs are a real share of your customers — common in real estate, jewellery, education and healthcare — yes. That usually means pages that answer questions asked from abroad and reporting by country, not a separate website."),
            ("Do you have pages for individual Kerala cities?", "Yes — for the eight cities where Google’s autocomplete shows steady demand for an SEO expert: Kochi, Trivandrum, Calicut, Thrissur, Malappuram, Kannur, Kollam and Palakkad. Each covers that city’s industries, how its customers search and what page 1 looks like there. A town gets its own page only when people search for it."),
        ],
        "services": ["local-seo", "content-strategy", "seo-consulting"],
        "industries": ["professional-services", "local-multi-location"],
    },
    {
        "slug": "tamil-nadu",
        "name": "Tamil Nadu",
        "status": "Same state",
        "status_key": "home",
        "title": "SEO Expert in Tamil Nadu | Sreejith Digital",
        "description": "SEO expert and consultant for Tamil Nadu businesses, based in Chennai, with honest city-level guidance and no invented local results.",
        "h1": "SEO expert in Tamil Nadu",
        "lede": "I’m based in Chennai, in Tamil Nadu. This hub is for businesses comparing an SEO company with a dedicated expert, and for city-level searches that need more than a name swapped into a template.",
        "short": "Same-state hub for Chennai and city-level Tamil Nadu search demand.",
        "delivery": "Based in Chennai, same state",
        "results_city": "",
        "context_heading": "Why this state hub exists",
        "context": [
            "Tamil Nadu searchers use both “SEO expert” and “SEO company” phrasing. A state hub should make the difference clear: an agency can coordinate ads, design and social, while a dedicated consultant gives one accountable specialist for strategy and technical SEO.",
            "Chennai keeps its own home-base page at /locations/chennai/. Its schema already sits inside Tamil Nadu, so the state hub links to it rather than duplicating it.",
            "A separate city page is published only when it has distinct sectors, search behaviour, localities and FAQs. Swapping the city name must make the copy false; otherwise the page stays a doorway page and does not ship.",
        ],
        "work_heading": "Work connected to Tamil Nadu",
        "work": [
            "I don’t have a published client result from Coimbatore, Madurai or Salem yet, and I won’t imply one. The published case study is from Bengaluru, where an MEP contractor reached page-one commercial positions on Google India and was cited in Google’s AI Overview for a sector query.",
            "The method is the same across states: a written baseline, one page per intent, approved proof next to each claim, clean internal links and dated reporting. When there is a Tamil Nadu city result, it will be dated and shown on that city’s page.",
        ],
        "engage_heading": "Working with Tamil Nadu teams",
        "engage": [
            "Calls in English or Malayalam",
            "Based in Chennai, same state; meetings when travelling",
            "No local office or local client result claimed",
        ],
        "faqs": [
            ("Should I hire an SEO company in Tamil Nadu or a dedicated expert?", "A company fits if you want ads, design, social media and SEO coordinated by one team. A dedicated expert fits if you want one accountable specialist leading the strategy, technical audit and reporting. I’m based in Chennai and lead every engagement myself."),
            ("Do you have an office outside Chennai in Tamil Nadu?", "No. I’m based in Chennai and can meet in person when travelling in the same state, but I don’t list offices in other cities. A fake address is a trust risk and a Google Business Profile risk."),
            ("Do you have published client results from Coimbatore, Madurai or Salem?", "No. I don’t have a published local client result from those cities, and I won’t invent one. The dated case study on this site is from other markets, with both wins and misses written up."),
            ("Can we work in Tamil?", "I consult in English or Malayalam. Tamil-language consulting is not claimed, so content and calls should be planned around those confirmed languages."),
            ("Do you have separate pages for every Tamil Nadu city?", "No. Chennai has its own home-base page. A separate city page is added only when there is real local substance, distinct demand and copy that would become false if the city name were swapped."),
        ],
        "services": ["local-seo", "technical-seo", "seo-consulting"],
        "industries": ["professional-services", "local-multi-location"],
    },
]

LOCATION_STATUS_NOTE = {
    "results": "Client results",
    "progress": "Work in progress",
    "home": "Home ground",
}

# ---------------------------------------------------------------------------
# Place hierarchy: Country > State > District > City.
# Wikipedia URLs disambiguate each place for search engines and AI systems.
# ---------------------------------------------------------------------------
WIKI = "https://en.wikipedia.org/wiki/"
COUNTRY_PLACE = {"@type": "Country", "name": "India", "sameAs": WIKI + "India"}
STATE_PLACES = {
    "Kerala": {"@type": "State", "name": "Kerala", "sameAs": WIKI + "Kerala", "containedInPlace": COUNTRY_PLACE},
    "Tamil Nadu": {"@type": "State", "name": "Tamil Nadu", "sameAs": WIKI + "Tamil_Nadu", "containedInPlace": COUNTRY_PLACE},
    "Karnataka": {"@type": "State", "name": "Karnataka", "sameAs": WIKI + "Karnataka", "containedInPlace": COUNTRY_PLACE},
    "Telangana": {"@type": "State", "name": "Telangana", "sameAs": WIKI + "Telangana", "containedInPlace": COUNTRY_PLACE},
}
# Places for the top-level location pages (used in Service.areaServed).
LOCATION_PLACES = {
    "bengaluru": {"@type": "City", "name": "Bengaluru", "alternateName": "Bangalore", "sameAs": WIKI + "Bengaluru", "containedInPlace": STATE_PLACES["Karnataka"]},
    "delhi-ncr": {"@type": "Place", "name": "Delhi NCR", "alternateName": ["National Capital Region", "Delhi", "Gurugram", "Noida"], "sameAs": WIKI + "National_Capital_Region_(India)", "containedInPlace": COUNTRY_PLACE},
    "hyderabad": {"@type": "City", "name": "Hyderabad", "sameAs": WIKI + "Hyderabad", "containedInPlace": STATE_PLACES["Telangana"]},
    "chennai": {"@type": "City", "name": "Chennai", "alternateName": "Madras", "sameAs": WIKI + "Chennai", "containedInPlace": STATE_PLACES["Tamil Nadu"]},
    "kerala": STATE_PLACES["Kerala"],
    "tamil-nadu": STATE_PLACES["Tamil Nadu"],
}

SERP_DATE = "27 November 2026"

# Kerala city pages. Gate: Google India autocomplete shows "seo expert in <city>"
# as a popular suggestion (checked 27 Nov 2026). Each page must pass the
# city-name test: swap the city name and the page becomes false.
STATE_CITIES = {
    "kerala": [
    {
        "slug": "kochi",
        "name": "Kochi",
        "crumb": "Kochi",
        "alt_names": ["Cochin", "Ernakulam"],
        "wiki": "Kochi",
        "district": "Ernakulam",
        "title": "SEO Expert in Kochi (Ernakulam) | Sreejith Digital",
        "description": "SEO for Kochi and Ernakulam businesses: Infopark tech firms, exporters, retailers, hospitals and Fort Kochi stays. Remote, with dated results, not promises.",
        "h1": "SEO expert in Kochi",
        "lede": "Kochi is Kerala’s busiest commercial market, and many of its businesses sell well beyond the city. I help Kochi firms — from Infopark product companies to Edappally retailers and Fort Kochi stays — win the searches that bring enquiries, with dated, verifiable reporting.",
        "short": "Kerala’s commercial centre: Infopark, the port, retail and tourism.",
        "economy_heading": "What Kochi businesses need from search",
        "economy": [
            ("IT and startups", "Infopark in Kakkanad and the startup campus at Kalamassery are full of firms whose buyers are in Bengaluru, the Gulf or abroad. They rarely need “Kochi” in their keywords; they need pages built around what those buyers search."),
            ("Port, logistics and exports", "Cochin Port, the Vallarpadam container terminal and the Spices Board and MPEDA head offices make Kochi an export city. Overseas buyers search by product, grade and certification, so specification pages matter more than a home page."),
            ("Retail and real estate", "From Edappally to Kakkanad, apartment projects and large stores compete for the same local searches. Project pages with registration details, and answers for NRI buyers, convert better than generic listings."),
            ("Tourism and healthcare", "Fort Kochi and Mattancherry stays compete with booking platforms, and large hospitals draw patients from across Kerala and the Gulf. Both win with their own detailed pages and a well-kept Google profile."),
        ],
        "search": [
            "Customers use three names for the same place: Kochi, Cochin and Ernakulam. A page should lead with the one your customers use — your Search Console queries will tell you — and mention the others naturally, not repeat all three in every heading.",
            "For local services, the locality often carries more intent than the city: “Kakkanad”, “Edappally” or “Vyttila” searches come from people ready to visit. Those belong in service pages and in your Google Business Profile service areas.",
        ],
        "areas": ["Kakkanad", "Edappally", "Vyttila", "Palarivattom", "Kaloor", "MG Road", "Fort Kochi", "Kalamassery", "Aluva", "Tripunithura"],
        "landscape": [
            "An AI Overview sat at the top, listing four individual consultants drawn from their own websites and profiles.",
            "The map pack showed three providers with between 10 and 80 Google reviews.",
            "Below that: personal-brand sites with a page for each city, a LinkedIn profile and free-hosted sites.",
        ],
        "faqs": [
            ("Should my Kochi business target “Kochi”, “Cochin” or “Ernakulam”?", "All three are searched. Lead with the name your customers use (check your Search Console queries), mention the others once where it reads naturally, and use locality names like Kakkanad or Edappally where you actually serve. Don’t build a separate page for each name; that is duplication."),
            ("Should I hire an SEO company in Kochi or a dedicated expert?", "If you want ads, social media, design and SEO run by one team, an agency fits. If you want one accountable person doing the strategy and the hands-on SEO, a dedicated expert fits. I lead every engagement myself and work with Kochi businesses remotely."),
            ("Can an Infopark company rank outside Kerala?", "Yes, and that is usually the right goal. Product and service firms in Kochi rarely need the city in their keywords. They need pages built around what buyers in Bengaluru, the Gulf or overseas type, plus proof those buyers trust."),
            ("How long does SEO take for a Kochi business?", "With a sound site, local service terms often move within two to three months and settle over four to six. In my published case study, five commercial terms reached page 1 in about three months — in other markets, so treat it as a reference, not a promise."),
            ("Do you have an office in Kochi?", "No. I’m from Thrissur and based in Chennai. I work with Kochi businesses remotely, in Malayalam or English, and can meet in person when I travel to Kerala. I won’t list an address I don’t have."),
        ],
        "nearby": ["thrissur", "trivandrum", "calicut"],
    },
    {
        "slug": "trivandrum",
        "name": "Thiruvananthapuram",
        "crumb": "Trivandrum",
        "query_name": "Trivandrum",
        "alt_names": ["Trivandrum", "TVM"],
        "wiki": "Thiruvananthapuram",
        "district": "Thiruvananthapuram",
        "title": "SEO Expert in Trivandrum (Thiruvananthapuram)",
        "description": "SEO for Trivandrum businesses: Technopark firms, hospitals, coaching institutes and Kovalam and Varkala stays. Remote, with dated results, no promises.",
        "h1": "SEO expert in Trivandrum",
        "lede": "Buyers in Thiruvananthapuram compare carefully: students choosing institutes, patients choosing hospitals, Technopark firms choosing vendors. I help Trivandrum businesses earn that trust in search, with clear service pages, credentials beside every claim and Google profiles that match.",
        "short": "The capital: Technopark, healthcare, coaching and coastal tourism.",
        "economy_heading": "What Trivandrum businesses need from search",
        "economy": [
            ("Technopark firms", "Technopark in Kazhakkoottam, one of India’s first IT parks, houses companies that sell to clients worldwide. Their search work is national and international B2B content, not local listings."),
            ("Healthcare and medical travel", "The city’s large hospitals and specialist centres draw patients from across south Kerala and abroad. Google holds health pages to a higher standard, so doctor credentials, reviewed content and honest claims come first."),
            ("Coaching and education", "As the state capital, Trivandrum has a deep market for civil-service, entrance and professional coaching. Demand is seasonal, so course pages with fees, schedules and results need to be live months before admissions open."),
            ("Coastal tourism and the new port", "Kovalam, Varkala and Poovar stays compete with booking platforms for direct bookings, and the Vizhinjam seaport, commissioned in 2025 and now handling export-import cargo, adds a logistics market in the south of the district."),
        ],
        "search": [
            "Searches use “Trivandrum”, “Thiruvananthapuram” and “TVM”. For searches like this one, Google’s autocomplete offers “Trivandrum”, so it belongs in titles, with the official name in the body and the structured data.",
            "Locality matters: Kazhakkoottam for Technopark-area services, Pattom, Kowdiar and Vazhuthacaud for central offices and clinics. Patients and parents often search the locality plus the specialty, not the city name.",
        ],
        "areas": ["Kazhakkoottam", "Technopark", "Pattom", "Kowdiar", "Vazhuthacaud", "Thampanoor", "Kesavadasapuram", "Peroorkada", "Kovalam", "Varkala"],
        "landscape": [
            "An AI Overview listed eight individual consultants and pointed to directories for agencies.",
            "The map pack showed providers with between 3 and 128 Google reviews, the top one in business for 15+ years.",
            "Google noted that two results had been removed from the page after copyright (DMCA) complaints.",
        ],
        "faqs": [
            ("Trivandrum or Thiruvananthapuram — which should my website use?", "Use “Trivandrum” in titles if that is what your customers type (check Search Console), and the official name in your address, body copy and structured data. Search engines understand both refer to the same city; your job is to match the words buyers use."),
            ("Do hospitals and clinics in Trivandrum need a different approach?", "Yes. Health pages are held to a higher standard. Show who wrote and reviewed each page, list doctors’ qualifications, avoid outcome promises, and keep department and doctor pages consistent with your Google Business Profile."),
            ("Is an SEO company in Trivandrum better than a dedicated SEO expert?", "It depends on what you need. Agencies bundle SEO with ads, social media and design; a dedicated expert gives you one specialist who owns the strategy and leads the work. Ask either for dated results and who will actually work on your site."),
            ("When should a coaching centre start SEO?", "At least three to four months before admissions open. Course pages need time to be crawled and ranked, and results pages from earlier batches need dates and specifics to be believed."),
            ("Do you have an office in Trivandrum?", "No. I’m from Thrissur and based in Chennai. I work with Trivandrum businesses remotely, in Malayalam or English, and can meet in person when I travel to Kerala. I won’t list an address I don’t have."),
        ],
        "nearby": ["kollam", "kochi", "thrissur"],
    },
    {
        "slug": "calicut",
        "name": "Kozhikode",
        "crumb": "Calicut",
        "query_name": "Calicut",
        "alt_names": ["Calicut"],
        "wiki": "Kozhikode",
        "district": "Kozhikode",
        "title": "SEO Expert in Calicut (Kozhikode) | Sreejith Digital",
        "description": "SEO for Calicut (Kozhikode) businesses: hospitals, traders, food brands and Cyberpark firms, many selling to the Gulf. Remote, with dated, honest reporting.",
        "h1": "SEO expert in Calicut",
        "lede": "Calicut businesses often sell to two audiences at once: customers in Kozhikode and Malayalis working in the Gulf. I help Kozhikode hospitals, traders, food brands and Cyberpark firms rank for both — on Google Maps locally and in search further afield — with dated reporting.",
        "short": "Trade, food, hospitals and Cyberpark — with a large Gulf audience.",
        "economy_heading": "What Calicut businesses need from search",
        "economy": [
            ("Trade and retail", "SM Street, the wholesale markets and the textile and timber trade still run largely on reputation and referrals. A complete Google Business Profile, category pages and WhatsApp-friendly enquiry paths turn that reputation into searches."),
            ("Hospitals", "Kozhikode’s private hospitals serve the whole of north Kerala and families in the Gulf who arrange treatment for relatives. Doctor and department pages, and booking that works across time zones, are what those searchers need."),
            ("Food brands", "Kozhikode’s halwa, banana chips and biryani have a following far beyond the city — and the city is a UNESCO City of Literature. Brands that ship need product pages that can rank nationally, not just a listing on a marketplace."),
            ("Education and IT", "IIM Kozhikode, NIT Calicut and the Cyberpark campuses bring B2B firms and training providers whose buyers are outside Kerala. Their search work is national content, not local listings."),
        ],
        "search": [
            "In English searches, people type “Calicut” far more than “Kozhikode”: on 27 November 2026, Google’s autocomplete offered “seo expert in calicut” as a popular suggestion and “kozhikode” only as a minor one. Titles should use Calicut; addresses and structured data should use Kozhikode.",
            "Gulf-based customers search on Gulf time and in English or Manglish. Pages that answer remote questions — price, delivery, appointments, documents — capture demand that “near me” targeting misses.",
        ],
        "areas": ["Mavoor Road", "Palayam", "Nadakkavu", "Eranhipalam", "West Hill", "Feroke", "Ramanattukara", "Vadakara", "Koyilandy", "Thamarassery"],
        "landscape": [
            "No AI Overview appeared; the first organic result was a consultant who also trains SEO students.",
            "The map pack’s leader had 83 Google reviews; the other two had one or two.",
            "A directory on page 1 listed 367 SEO service providers in Kozhikode.",
        ],
        "faqs": [
            ("Should my site say Calicut or Kozhikode?", "Both, in different places. Searchers mostly type “Calicut”, so use it in titles and headings where it reads naturally. Use “Kozhikode” in your address, Google Business Profile and structured data, which follow the official name."),
            ("Most of my customers’ decision-makers are in the Gulf. Can SEO reach them?", "Yes. Build pages that answer questions asked from abroad, make enquiry and payment easy across time zones, and report enquiries by country so you can see what the Gulf audience is worth."),
            ("Do I need an SEO company in Calicut, or will one expert do?", "For SEO alone, one experienced expert is usually enough for a Calicut business, and you deal directly with the person doing the work. If you also need ads, social media and design run together, a company with a team may suit you better."),
            ("Does a Calicut shop need a Google Business Profile?", "If customers visit you or you visit them, yes — it is usually the fastest local win. Keep the name exactly as it appears on your signboard; adding keywords to the name breaks Google’s guidelines and can get the profile suspended."),
            ("Do you have an office in Calicut?", "No. I’m from Thrissur and based in Chennai. I work with Calicut businesses remotely, in Malayalam or English, and can meet in person when I travel to Kerala. I won’t list an address I don’t have."),
        ],
        "nearby": ["malappuram", "kannur", "thrissur"],
    },
    {
        "slug": "thrissur",
        "name": "Thrissur",
        "crumb": "Thrissur",
        "alt_names": ["Trichur"],
        "wiki": "Thrissur",
        "district": "Thrissur",
        "title": "SEO Expert in Thrissur | Sreejith Digital",
        "description": "SEO expert from Thrissur for jewellers, banks, hospitals and Guruvayur-area hospitality. Malayalam or English, with dated, honest reporting.",
        "h1": "SEO expert in Thrissur",
        "lede": "Thrissur is my home town — and home to some of India’s best-known jewellery and banking brands, so local businesses compete with big names and big budgets. I help Thrissur firms win where size doesn’t decide: specific product and service pages, Google Maps and the trust signals buyers check.",
        "status_label": "Home town",
        "short": "My home town: jewellery, banking, hospitals and temple towns.",
        "economy_heading": "What Thrissur businesses need from search",
        "economy": [
            ("Gold and jewellery", "Thrissur is a jewellery-making centre and the headquarters of national chains. A smaller jeweller won’t outrank them for “jewellery”, but can win specific searches — bridal sets, temple jewellery, a landmark — with detailed product pages and hallmark information."),
            ("Banking and finance", "South Indian Bank, CSB Bank, Dhanlaxmi Bank, ESAF Small Finance Bank and KSFE are all headquartered in Thrissur, alongside many gold-loan and chit-fund firms. Financial pages are held to a higher standard: clear terms, regulator details and consistent branch information."),
            ("Temple towns and festivals", "Guruvayur weddings and Thrissur Pooram create sharp, predictable search peaks for hotels, halls, caterers and photographers. Pages need to be live and ranking before the season, not during it."),
            ("Healthcare and institutions", "Medical colleges, hospitals and institutions like Kerala Kalamandalam draw people from across central Kerala. Department pages and accurate profiles matter more than a long home page."),
        ],
        "search": [
            "Thrissur searchers lean heavily on Google Maps: “gold loan near me”, “jewellery shop near me” and hospital searches are decided in the map pack, where reviews and an accurate profile carry unusual weight.",
            "Searches spread across the district’s towns — Guruvayur, Chalakudy, Irinjalakuda, Kunnamkulam, Kodungallur — so a business serving them should cover each town where it really operates, not only the city.",
        ],
        "areas": ["Swaraj Round", "Punkunnam", "Ayyanthole", "Poonkunnam", "Guruvayur", "Kunnamkulam", "Irinjalakuda", "Chalakudy", "Kodungallur", "Wadakkanchery"],
        "landscape": [
            "An AI Overview listed five individual consultants and four agencies; the agencies had between 114 and 329 Google reviews.",
            "Organic results mixed consultant sites with Justdial and Sortlist directories.",
            "Two map-pack listings used the search phrase itself in the business name — a practice Google’s business-profile guidelines prohibit.",
        ],
        "faqs": [
            ("Can a small Thrissur jeweller compete with the national chains?", "Not for “jewellery”, but yes for specific searches: product types, bridal collections, hallmark questions and your locality. Detailed product pages, real photos and a strong Google profile can beat a chain’s generic page."),
            ("Is SEO different for banks and finance companies?", "Yes. Google treats financial pages as high-stakes, so they need clear terms, named authors or reviewers, regulator details and consistent branch information. Every claim should be checked by compliance before it goes live."),
            ("When should Guruvayur hotels and wedding services start?", "Several months before the main wedding dates. Pages need time to rank, and the useful ones answer specific questions — packages, capacity, distance from the temple — rather than describing the town."),
            ("Do you have an office in Thrissur?", "No office — Thrissur is my home town. I’m now based in Chennai, work with Thrissur businesses remotely in Malayalam or English, and meet in person when I’m back in Kerala. I won’t list an address I don’t have."),
        ],
        "nearby": ["kochi", "palakkad", "malappuram"],
    },
    {
        "slug": "malappuram",
        "name": "Malappuram",
        "crumb": "Malappuram",
        "alt_names": [],
        "wiki": "Malappuram",
        "district": "Malappuram",
        "title": "SEO Expert in Malappuram | Sreejith Digital",
        "description": "SEO for Malappuram businesses: education, Ayurveda, hospitals and trade, with customers at home and in the Gulf. Remote from Chennai, with dated reporting.",
        "h1": "SEO expert in Malappuram",
        "lede": "Kerala’s migration surveys have repeatedly found more emigrants from Malappuram than from any other district, so many customers here search from Dubai, Riyadh or Doha. I help Malappuram institutes, hospitals, Ayurveda brands and traders reach both the family at home and the earner abroad.",
        "short": "Education, Ayurveda, hospitals and a large Gulf audience.",
        "economy_heading": "What Malappuram businesses need from search",
        "economy": [
            ("Ayurveda", "Kottakkal, home to the Arya Vaidya Sala since 1902, anchors a cluster of Ayurveda hospitals, clinics and product makers. Treatment pages need to answer international enquiries; product pages need to rank nationally."),
            ("Education", "The University of Calicut sits in Malappuram district, and colleges, schools and job-oriented course providers compete for the same students. Course pages with fees, intakes and outcomes win over brochure-style pages."),
            ("Hospitals", "Perinthalmanna is known as a hospital town, and patients travel from neighbouring districts. Department and doctor pages, plus profiles that match, help those patients choose before they travel."),
            ("Trade, property and construction", "Gulf earnings fund much of the district’s construction and property market, and the international airport at Karipur is in the district. Buyers abroad need clear project details and remote-friendly enquiry paths."),
        ],
        "search": [
            "Many decisions are made by family members in the Gulf, on Gulf time. Pages should answer what a remote decision-maker asks — fees, documents, timelines — and enquiry forms should work well on a phone.",
            "Searches spread across the district’s towns rather than centring on Malappuram town: Manjeri, Tirur, Perinthalmanna, Kottakkal and Kondotty all have their own demand. Kottakkal already shows up in Google’s suggestions for SEO searches.",
        ],
        "areas": ["Malappuram town", "Manjeri", "Tirur", "Perinthalmanna", "Kottakkal", "Kondotty", "Nilambur", "Ponnani", "Valanchery", "Tirurangadi"],
        "landscape": [
            "An AI Overview listed seven providers, mostly with ratings and phone numbers quoted from their business profiles.",
            "Ads from national SEO companies ran above the organic results.",
            "Many page-1 titles described their owner as the “best” or “No. 1” SEO expert in Malappuram.",
        ],
        "faqs": [
            ("My customers’ families decide from the Gulf. What should the website do?", "Answer their questions without a phone call: prices or fee ranges, documents, timelines and how payment works from abroad. Then track enquiries by country, so you can see how much of your business the Gulf audience drives."),
            ("Is Malayalam content worth it in Malappuram?", "Check your Search Console queries first. If people search in Malayalam or Manglish for your services, a few well-written Malayalam pages can work; translating the whole site rarely pays off."),
            ("Do you work with businesses in Tirur, Manjeri and Perinthalmanna?", "Yes. A business that genuinely serves several towns should cover each one properly on its own site. A town gets its own page only when people search for it and the page has something specific to say."),
            ("Do you have an office in Malappuram?", "No. I’m from Thrissur and based in Chennai. I work with Malappuram businesses remotely, in Malayalam or English, and can meet in person when I travel to Kerala. I won’t list an address I don’t have."),
        ],
        "nearby": ["calicut", "palakkad", "thrissur"],
    },
    {
        "slug": "kannur",
        "name": "Kannur",
        "crumb": "Kannur",
        "alt_names": ["Cannanore"],
        "wiki": "Kannur",
        "district": "Kannur",
        "title": "SEO Expert in Kannur | Sreejith Digital",
        "description": "SEO for Kannur businesses: handloom makers, homestays, hospitals and institutes, from Thalassery to Payyanur. Remote from Chennai, with dated, honest reporting.",
        "h1": "SEO expert in Kannur",
        "lede": "Kannur’s handlooms already sell far beyond Kerala, and its international airport has opened the district to more visitors. I help Kannur makers, homestays, hospitals and institutes turn that reach into search visibility — from Thalassery to Payyanur.",
        "short": "Handloom, Theyyam-season tourism, hospitals and education.",
        "economy_heading": "What Kannur businesses need from search",
        "economy": [
            ("Handloom and home furnishings", "Kannur’s woven home furnishings are exported worldwide, but many weavers and cooperatives depend on buyers who already know them. Product pages with materials, sizes and care details can reach retail and trade buyers directly."),
            ("Theyyam season and beaches", "Visitors plan trips around the Theyyam season and beaches like Muzhappilangad. Homestays that publish useful, dated guides before the season can win bookings directly instead of paying platform commissions."),
            ("Hospitals and education", "The medical college at Pariyaram, Kannur University and private hospitals serve north Kerala. Accurate department, course and doctor pages matter more than a long home page."),
            ("Gulf-linked trade and property", "Like much of north Kerala, Kannur has a large Gulf diaspora, which shapes demand for property, gold and construction. Pages need to answer buyers who are not in Kannur when they search."),
        ],
        "search": [
            "Kannur district searches spread across several towns — Thalassery, Payyanur, Taliparamba and Mattannur near the airport — and many people search the town, not the district.",
            "Tourism searches are strongly seasonal and timed around festivals. Content published after the season starts is usually too late to rank for it.",
        ],
        "areas": ["Kannur town", "Thalassery", "Payyanur", "Taliparamba", "Mattannur", "Iritty", "Kuthuparamba", "Payyambalam", "Azhikode", "Chirakkal"],
        "landscape": [
            "An AI Overview listed seven consultants and quoted packages starting around ₹10,000 a month.",
            "The map pack showed three providers with 0 to 34 reviews; all three used the search phrase in their business name.",
            "Ads from national and overseas SEO agencies ran on the page.",
        ],
        "faqs": [
            ("Can a Kannur handloom unit sell online through search?", "Yes, if the product pages do the selling: real photos, materials, sizes, care instructions, wholesale terms and shipping details. Marketplaces help with reach; your own site builds the brand and the margin."),
            ("When should homestays publish Theyyam content?", "Well before the season — a guide that is live by early autumn has time to rank. Keep it factual and dated, and link it to the rooms and booking page."),
            ("Do you cover Thalassery, Payyanur and Taliparamba?", "Yes. I work with businesses anywhere in Kannur district, remotely. If you serve several towns, each needs proper coverage on your site, not a copied page."),
            ("Do you have an office in Kannur?", "No. I’m from Thrissur and based in Chennai. I work with Kannur businesses remotely, in Malayalam or English, and can meet in person when I travel to Kerala. I won’t list an address I don’t have."),
        ],
        "nearby": ["calicut", "malappuram", "thrissur"],
    },
    {
        "slug": "kollam",
        "name": "Kollam",
        "crumb": "Kollam",
        "alt_names": ["Quilon"],
        "wiki": "Kollam",
        "district": "Kollam",
        "title": "SEO Expert in Kollam | Sreejith Digital",
        "description": "SEO for Kollam businesses: cashew exporters, hospitals, institutes and Ashtamudi backwater stays. Remote from Chennai, with dated, honest reporting.",
        "h1": "SEO expert in Kollam",
        "lede": "Kollam is known as India’s cashew capital, and many of its firms sell to buyers who never search for “Kollam”. I help Kollam exporters, hospitals, institutes and backwater stays get found by the people who actually buy from them.",
        "short": "Cashew exports, backwaters, minerals and education.",
        "economy_heading": "What Kollam businesses need from search",
        "economy": [
            ("Cashew processing and export", "The Cashew Export Promotion Council of India is headquartered in Kollam, and processors here sell to buyers across India and overseas. Those buyers search by grade, certification and packing — so specification pages beat a company profile."),
            ("Backwater tourism", "Ashtamudi Lake and the Kollam–Alappuzha backwater route bring visitors who plan weeks ahead. Resorts and homestays win direct bookings with detailed pages on routes, timings and what is included."),
            ("Minerals and industry", "The mineral-sands industry at Chavara and industrial units around Kundara sell B2B, often nationally. Their buyers want technical detail and evidence, not local listings."),
            ("Education and healthcare", "Engineering colleges, the Amritapuri campus and the district’s hospitals draw students and patients from across south Kerala. Course and department pages need facts, fees and dates."),
        ],
        "search": [
            "Exporters’ buyers rarely type a city at all; they search the product. For them, Kollam belongs in the company story and the structured data, while titles carry the product and grade.",
            "Local searches spread across Karunagappally, Kottarakkara and Punalur, so district businesses should cover the towns they genuinely serve.",
        ],
        "areas": ["Chinnakada", "Kollam town", "Karunagappally", "Kottarakkara", "Punalur", "Paravur", "Chavara", "Kundara", "Kadappakada", "Ashtamudi"],
        "landscape": [
            "No AI Overview appeared; Google led with the map pack.",
            "Two of the three map-pack businesses were agencies with 163 and 182 Google reviews.",
            "One page-1 agency advertised SEO from ₹3,000 a month.",
        ],
        "faqs": [
            ("We export cashews. Should our website mention Kollam at all?", "Yes, in your story, address and structured data — it is part of your credibility. But your titles should carry what buyers search: the product, grade and certification. Kollam is rarely in an importer’s query."),
            ("Can a backwater homestay rank against booking platforms?", "For specific searches, yes: routes, houseboat timings, Ashtamudi activities and questions a guest asks before booking. A well-kept Google profile and your own detailed pages can win direct bookings."),
            ("Is very cheap SEO worth it?", "Check what is included. Very low monthly fees usually cover reports and a few posts, not technical fixes or content. Ask for the specific pages that will change and how results will be measured."),
            ("Do you have an office in Kollam?", "No. I’m from Thrissur and based in Chennai. I work with Kollam businesses remotely, in Malayalam or English, and can meet in person when I travel to Kerala. I won’t list an address I don’t have."),
        ],
        "nearby": ["trivandrum", "kochi", "thrissur"],
    },
    {
        "slug": "palakkad",
        "name": "Palakkad",
        "crumb": "Palakkad",
        "alt_names": ["Palghat"],
        "wiki": "Palakkad",
        "district": "Palakkad",
        "title": "SEO Expert in Palakkad | Sreejith Digital",
        "description": "SEO for Palakkad businesses: Kanjikode manufacturers, rice and agri brands, hospitals and institutes, with Coimbatore next door. Remote, with dated reporting.",
        "h1": "SEO expert in Palakkad",
        "lede": "Palakkad sits on the Palakkad Gap, the main road and rail route between Kerala and Tamil Nadu, and its businesses often sell into Coimbatore as much as Kochi. I help Palakkad manufacturers, agri brands, hospitals and institutes rank across that corridor.",
        "short": "Manufacturing, agri brands and the Coimbatore corridor.",
        "economy_heading": "What Palakkad businesses need from search",
        "economy": [
            ("Manufacturing at Kanjikode", "The Kanjikode industrial area hosts public-sector and private manufacturers that sell to buyers across south India. B2B buyers search by product and specification, so technical pages and downloadable data sheets matter."),
            ("Rice and agri brands", "Palakkad is known as Kerala’s rice bowl, and Palakkadan Matta rice carries a geographical indication. Brands that pack and ship need product pages that rank nationally and explain origin and quality."),
            ("Education", "IIT Palakkad and the district’s colleges and coaching centres draw students from both sides of the border. Course pages with fees, intakes and outcomes win over brochures."),
            ("Healthcare and Ayurveda", "Hospitals and Ayurveda centres serve patients from Palakkad and western Tamil Nadu. Pages need to answer both audiences clearly."),
        ],
        "search": [
            "Palakkad’s market runs across a state border. Many customers are in Coimbatore, Pollachi or Tiruppur, so service pages should name the areas you really serve on both sides.",
            "Parts of the district are bilingual, and some searches are in Tamil as well as Malayalam and English. Check Search Console before adding language pages; build them only where real queries exist.",
        ],
        "areas": ["Palakkad town", "Kanjikode", "Ottapalam", "Shoranur", "Chittur", "Mannarkkad", "Alathur", "Pattambi", "Kalpathy", "Walayar"],
        "landscape": [
            "No AI Overview appeared; the map pack showed three individual consultants with 5 to 17 reviews.",
            "A directory on page 1 listed 36+ SEO consultants in Palakkad.",
            "Most organic results were individual consultant sites, one on a free hosting subdomain.",
        ],
        "faqs": [
            ("Should a Palakkad manufacturer target Coimbatore too?", "If you sell there, yes. Name the areas you really supply on your service and product pages, and make sure the specifications Coimbatore buyers compare are on the page, not only in a brochure."),
            ("Is Tamil content useful in Palakkad?", "Sometimes. Parts of the district are bilingual and some buyers search in Tamil. Check your Search Console queries first and add Tamil pages only where people are searching that way."),
            ("Can a rice or agri brand sell online through search?", "Yes, with proper product pages: origin, variety, packing sizes, shipping and certifications. Product structured data helps search engines understand prices and availability."),
            ("Do you have an office in Palakkad?", "No. I’m from Thrissur and based in Chennai. I work with Palakkad businesses remotely, in Malayalam or English, and can meet in person when I travel to Kerala. I won’t list an address I don’t have."),
        ],
        "nearby": ["thrissur", "malappuram", "kochi"],
    },
    ],
    "tamil-nadu": [{'slug': 'coimbatore',
          'name': 'Coimbatore',
          'crumb': 'Coimbatore',
          'alt_names': ['Kovai'],
          'wiki': 'Coimbatore',
          'district': 'Coimbatore',
          'status_label': 'Same state',
          'title': 'SEO Expert in Coimbatore | Sreejith Digital',
          'description': 'SEO expert in Coimbatore for textile, pump, foundry, IT park and hospital firms: '
                         'city-specific research, no local office and no invented client results.',
          'h1': 'SEO expert in Coimbatore',
          'lede': 'Coimbatore’s buyers range from textile-mill procurement teams and pump exporters to TIDEL Park '
                  'software firms and hospital departments. I help those businesses build pages around the questions '
                  'their buyers actually ask, from Chennai in the same state.',
          'short': 'Textile mills, pumps, IT parks and hospitals in the Kovai market.',
          'economy_heading': 'What Coimbatore businesses need from search',
          'economy': [('Textiles and knitwear',
                       'Coimbatore has large and small textile mills, textile research institutes and a nearby '
                       'Tiruppur knitwear export cluster. Spinning mills and machinery suppliers need specification '
                       'pages for buyers, while garment exporters need category and certification detail rather than '
                       'a generic city page.'),
                      ('Pumps, motors and foundries',
                       'The district is known for pump and motor manufacturing, foundries and engineering goods. '
                       'Industrial suppliers are often compared on capacity, materials, standards and delivery '
                       'areas, so product and service pages should answer those checks before asking for an '
                       'enquiry.'),
                      ('IT parks and B2B services',
                       'TIDEL Park and other IT parks support software and B2B teams whose customers may be in '
                       'Chennai, Bengaluru or overseas. Their search work is usually national or export-led: '
                       'solution pages, comparison content and proof, not a stack of locality pages.'),
                      ('Hospitals and healthcare',
                       'Government and private hospitals serve patients from the district and nearby towns. '
                       'Department pages, doctor credentials, appointment routes and accurate profile information '
                       'matter more than broad claims, especially for treatment-related searches.')],
          'search': ['Coimbatore searchers often use two names for the same place: Coimbatore and Kovai. Lead with '
                     'the name your customers use in Search Console, mention the other once where it reads '
                     'naturally, and do not build a separate page for each name.',
                     'Locality intent is strong around Gandhipuram, Peelamedu, Singanallur and Saravanampatti. For a '
                     'clinic or showroom, those belong in service areas and profile details; for an exporter selling '
                     'outside Tamil Nadu, they usually should not lead the page at all.'],
          'areas': ['Gandhipuram',
                    'RS Puram',
                    'Tatabad',
                    'Race Course',
                    'Peelamedu',
                    'Singanallur',
                    'Saravanampatti',
                    'Kalapatti',
                    'Ganapathy',
                    'Saibaba Colony'],
          'landscape': ['On 27 November 2026, logged-out Google India searches for “seo expert in coimbatore” and '
                        '“seo company in coimbatore” detected Coimbatore, Tamil Nadu and reported about 54 and 53 '
                        'results respectively.',
                        'The local pack for the expert query showed BAA GROUPS (4.9, 744 reviews), Keywordit (4.9, '
                        '293) and CLOUD DREAMS (4.8, 493); the company query showed BAA GROUPS, Webnox Technologies '
                        '(4.8, 451) and CLOUD DREAMS.',
                        'AI Mode replies summarised local agencies, while web results included Webnox’s AI SEO '
                        'services page, an Upwork consultant listing and a OneCity local comparison page. Results '
                        'change daily, so the checklist beside this asks for dated evidence.'],
          'faqs': [('Should I hire an SEO company in Coimbatore or a dedicated expert?',
                    'If a textile machinery exporter needs a new website, ads, social media and SEO coordinated by '
                    'one team, a company can fit. If a pump manufacturer wants one person to audit specification '
                    'pages, fix indexation and report enquiries, a dedicated expert fits. I lead the work '
                    'from Chennai.'),
                   ('Can a TIDEL Park software firm target buyers outside Coimbatore?',
                    'Yes, and that is usually the right goal. Buyers in Chennai, Bengaluru or overseas rarely search '
                    'for a Coimbatore address; they search for the problem, integration, pricing model or proof. '
                    'Build solution pages around those queries and keep the city as context.'),
                   ('Do you have a Coimbatore office or a published local client result?',
                    'No. I am based in Chennai, in the same state, and can meet in person when travelling. I do not '
                    'list a Coimbatore office, and I do not have a published Coimbatore client result. The dated '
                    'case study on this site is from other markets.'),
                   ('Should my Coimbatore pages use Kovai as well?',
                    'Only where real query data supports it. Use the spelling your customers already search, mention '
                    'the alternate name once in useful copy, and avoid creating duplicate pages for Coimbatore and '
                    'Kovai. Search Console should settle which name leads.'),
                   ('Do you offer Tamil-language SEO consulting in Coimbatore?',
                    'I consult in English or Malayalam. Tamil-language consulting is not claimed, so content, calls '
                    'and reporting are planned around the confirmed languages rather than an unverified '
                    'capability.')],
          'nearby': ['madurai', 'salem'],
          'answer': 'Sreejith CU is an SEO consultant based in Chennai who works with Coimbatore textile '
                    'mills, pump and motor exporters, TIDEL Park teams and hospital departments remotely in English '
                    'or Malayalam. His dated case study is from Bengaluru, not Coimbatore. No Coimbatore office, '
                    'local client result or Tamil-language consulting is claimed.'},
         {'slug': 'madurai',
          'name': 'Madurai',
          'crumb': 'Madurai',
          'wiki': 'Madurai',
          'district': 'Madurai',
          'status_label': 'Same state',
          'title': 'SEO Company in Madurai | Sreejith Digital',
          'description': 'SEO company in Madurai advice for temple tourism, textiles, eye care and colleges, with '
                         'verified local context and a consultant based in Chennai.',
          'h1': 'SEO company in Madurai',
          'lede': 'Madurai’s search demand is shaped by visitors planning a temple trip, families comparing colleges '
                  'and hospitals, and textile buyers checking product detail. I help those organisations separate '
                  'visitor, local and admission enquiries instead of chasing one generic city keyword.',
          'short': 'Temple tourism, textiles, eye care and colleges around the Vaigai city.',
          'economy_heading': 'What Madurai businesses need from search',
          'economy': [('Temple and visitor economy',
                       'The Meenakshi Sundareswarar Temple is the landmark around which the city’s visitor economy '
                       'is organised. Hotels, guides and retailers need pages that answer dates, routes, check-in, '
                       'accessibility and nearby areas before the booking question.'),
                      ('Textiles and readymade garments',
                       'The district’s industries include cotton textiles, hosiery, silk weaving and integrated '
                       'textile parks. Exporters and retailers need product, fabric, sizing and wholesale pages; a '
                       'location-only page rarely answers a buyer’s comparison.'),
                      ('Eye care and medical travel',
                       'Aravind Eye Hospital began in Madurai and remains the headquarters of its eye-care system. '
                       'Clinic and department pages need reviewed medical information, practitioner credentials and '
                       'clear appointment paths, not broad promotional copy.'),
                      ('Education and institutions',
                       'Madurai Kamaraj University, medical and arts colleges, and training institutes draw students '
                       'from beyond the district. Course pages need fees, dates, eligibility and outcome '
                       'information, with enquiries separated from local service calls.')],
          'search': ['Madurai queries split by intent: temple visitors ask about timings, routes and stays; students '
                     'ask about courses, fees and eligibility; textile buyers ask about fabric, minimum order and '
                     'dispatch. One page with one H1 cannot serve all three jobs well.',
                     'Area names such as Anna Nagar, KK Nagar, Goripalayam, SS Colony and Thiruparankundram often '
                     'carry local intent. They belong in profile service areas and contact pages. A separate page '
                     'for each area is justified only when its own query data and content are distinct.'],
          'areas': ['Anna Nagar',
                    'KK Nagar',
                    'Tallakulam',
                    'Goripalayam',
                    'Simmakkal',
                    'Arapalayam',
                    'SS Colony',
                    'Thiruparankundram',
                    'Alagar Kovil Road',
                    'Vilangudi'],
          'landscape': ['On 27 November 2026, logged-out Google India searches for “seo expert in madurai” and “seo '
                        'company in madurai” detected Madurai, Tamil Nadu and reported about 58 and 55 results '
                        'respectively.',
                        'The local pack for the expert query showed Rank You Higher (4.8, 337 reviews), Digital Hari '
                        '(5.0, 98) and Findway Digital (5.0, 268); the company query showed SEO Business Company '
                        '(4.8, 46), Findway Digital and Century Minds (4.9, 191).',
                        'AI Mode replies named local agencies, while web results included Lavish Technologies’ '
                        'specialist page, a Moris Media small-business guide and a 10SEOS directory page. Results '
                        'change daily; that is why this page asks for the URL, date and method behind any claim.'],
          'faqs': [('Should I hire an SEO company in Madurai or a dedicated expert?',
                    'A company suits a hotel group that wants design, paid campaigns, social content and SEO '
                    'coordinated together. A dedicated expert suits a textile exporter or college that wants one '
                    'accountable specialist for structure, technical fixes and reporting. I lead every engagement '
                    'from Chennai.'),
                   ('Can a hotel near Meenakshi Temple rank for visitor searches?',
                    'Yes, but the page has to answer the visitor’s actual questions: distance and route to the '
                    'temple, check-in times, parking, family rooms and festival dates. A page that only repeats the '
                    'city name rarely beats a useful itinerary or stay page.'),
                   ('Do you have a Madurai office or a published local client result?',
                    'No. I am based in Chennai, in the same state, and can meet in person when travelling. I do not '
                    'list a Madurai office, and I do not have a published Madurai client result. The dated case '
                    'study on this site is from other markets.'),
                   ('How should a college or hospital structure its Madurai pages?',
                    'Give each course, department or treatment its own evidence-backed page, then connect it to one '
                    'clear Madurai hub. Medical and education pages need reviewed facts, dates and credentials; '
                    'reporting should separate admission, appointment and general enquiries.'),
                   ('Do you offer Tamil-language SEO consulting in Madurai?',
                    'I consult in English or Malayalam. Tamil-language consulting is not claimed, so content, calls '
                    'and reporting are planned around the confirmed languages rather than an unverified '
                    'capability.')],
          'nearby': ['coimbatore', 'salem'],
          'answer': 'Sreejith CU is an SEO consultant based in Chennai who works with Madurai visitor, '
                    'textile, eye-care and education pages remotely in English or Malayalam. The Meenakshi Temple '
                    'visitor economy, cotton textile units, Aravind Eye Hospital and university colleges shape the '
                    'page structure here. No Madurai office, local client result or Tamil-language consulting is '
                    'claimed.'},
         {'slug': 'salem',
          'name': 'Salem',
          'crumb': 'Salem',
          'wiki': 'Salem,_Tamil_Nadu',
          'district': 'Salem',
          'status_label': 'Same state',
          'title': 'SEO Company in Salem | Sreejith Digital',
          'description': 'SEO company in Salem for steel, sago, handloom, mango and transport businesses: local '
                         'search research, English or Malayalam consulting, and honest status.',
          'h1': 'SEO company in Salem',
          'lede': 'Salem is a manufacturing and distribution city: steel, sago, handloom, mangoes and road–rail '
                  'links all shape what buyers search. I help Salem firms turn those supply-chain details into '
                  'specification pages, service areas and enquiry reporting that a generic city template cannot '
                  'provide.',
          'short': 'Steel, sago, handloom, mango and transport searches in the Steel City.',
          'economy_heading': 'What Salem businesses need from search',
          'economy': [('Steel and minerals',
                       'The Salem Steel Plant and local magnesite, bauxite and iron-ore deposits support metal, '
                       'refractory and engineering suppliers. Their buyers compare grades, dimensions, tolerances '
                       'and delivery regions, so specification pages and downloadable data sheets matter more than '
                       'broad location copy.'),
                      ('Sago, starch and mangoes',
                       'Salem is known for sago and for Malgova mangoes; Sagoserve and GI-tag material document the '
                       'district’s tapioca and produce economy. Food brands need origin, pack size, season, shipping '
                       'and certification pages, with enquiries split by wholesale and retail.'),
                      ('Handloom and textiles',
                       'The district’s handloom industry produces silk and cotton sarees and dhoties alongside '
                       'spinning and garment units. Weavers and retailers need fabric, weave, care and dispatch '
                       'detail, plus product structured data where inventory and prices are reliable.'),
                      ('Transport and logistics',
                       'Salem Junction, national highways and bus routes make the city a transit point for South '
                       'India. Logistics and service firms need clear coverage pages, depot information and contact '
                       'routes; a map pack alone will not answer an out-of-state buyer’s question.')],
          'search': ['Salem queries often combine a product with a place: sago manufacturer, steel sheet supplier, '
                     'handloom saree, mango wholesale or transport service. The strongest pages answer the product '
                     'question first, then name the areas actually served.',
                     'Local names such as Fairlands, Suramangalam, Hasthampatti, Ammapet and Omalur Road matter for '
                     'service businesses and profiles. For a steel or sago exporter, buyer location and shipping '
                     'terms usually matter more, so reporting should separate Salem enquiries from other districts.'],
          'areas': ['Fairlands',
                    'Suramangalam',
                    'Hasthampatti',
                    'Ammapet',
                    'Alagapuram',
                    'Arisipalayam',
                    'Nethimedu',
                    'Kondalampatti',
                    'Chinna Thirupathi',
                    'Swarnapuri'],
          'landscape': ['On 27 November 2026, logged-out Google India searches for “seo expert in salem” and “seo '
                        'company in salem” detected Salem, Tamil Nadu and reported about 43 and 54 results '
                        'respectively.',
                        'The local pack for the expert query showed First Success Technologies (4.8, 1.8K reviews), '
                        'a local SEO consultant listing, Vijay SEO Expert (5.0, 3) and SEO Expert with no reviews; the '
                        'company query showed First Success Technologies, OctaDigi (5.0, 56) and Vijay Digital India '
                        '(5.0, 3).',
                        'An AI Overview was unavailable on both queries, while web results included a Justdial '
                        'directory listing, a Moris Media small-business guide and Doozy Info’s company page. Dated '
                        'observations are useful context, not a ranking promise.'],
          'faqs': [('Should I hire an SEO company in Salem or a dedicated expert?',
                    'A company fits a textile retailer that wants website design, paid ads, social media and SEO run '
                    'by one team. A dedicated expert fits a sago exporter or steel supplier that wants one person '
                    'to fix product-page architecture, indexation and enquiry tracking. I lead the work from '
                    'Chennai.'),
                   ('Can a Salem sago or mango brand rank outside the district?',
                    'Yes, if the page answers the buyer’s commercial checks: origin, variety, pack sizes, season, '
                    'minimum order, shipping and certification. Buyers in other states rarely search only for Salem; '
                    'they search for the product and then check the supplier.'),
                   ('Do you have a Salem office or a published local client result?',
                    'No. I am based in Chennai, in the same state, and can meet in person when travelling. I do not '
                    'list a Salem office, and I do not have a published Salem client result. The dated case study on '
                    'this site is from other markets.'),
                   ('Should a Salem logistics firm create a page for every route?',
                    'Only when each route has real demand and distinct content. Start with one clear coverage page, '
                    'name the corridors you actually serve, add depot and contact detail, then split routes out once '
                    'Search Console shows separate queries and you have something true to say about each.'),
                   ('Do you offer Tamil-language SEO consulting in Salem?',
                    'I consult in English or Malayalam. Tamil-language consulting is not claimed, so content, calls '
                    'and reporting are planned around the confirmed languages rather than an unverified '
                    'capability.')],
          'nearby': ['coimbatore', 'madurai'],
          'answer': 'Sreejith CU is an SEO consultant based in Chennai who works with Salem steel, sago, '
                    'handloom, mango and transport businesses remotely in English or Malayalam. Product '
                    'specifications, dispatch regions and route pages matter more here than a repeated city name. No '
                    'Salem office, local client result or Tamil-language consulting is claimed.'}],
}

KERALA_CITIES = STATE_CITIES["kerala"]
STATE_CITY_STATE_NAMES = {
    "kerala": "Kerala",
    "tamil-nadu": "Tamil Nadu",
}
STATE_CITY_BY_SLUG = {
    state_slug: {city["slug"]: city for city in cities}
    for state_slug, cities in STATE_CITIES.items()
}
KERALA_CITY_BY_SLUG = STATE_CITY_BY_SLUG["kerala"]


def city_place(city: dict, state_slug: str = "kerala") -> dict:
    """Country > State > District > City, for Service.areaServed."""
    place = {
        "@type": "City",
        "name": city["name"],
        "sameAs": WIKI + city["wiki"],
        "containedInPlace": {
            "@type": "AdministrativeArea",
            "name": f'{city["district"]} district',
            "sameAs": WIKI + f'{city["district"]}_district',
            "containedInPlace": STATE_PLACES[STATE_CITY_STATE_NAMES[state_slug]],
        },
    }
    if city.get("alt_names"):
        place["alternateName"] = city["alt_names"]
    return place


def city_label(city: dict) -> str:
    """The name searchers use, e.g. Calicut rather than Kozhikode."""
    return city.get("query_name", city["name"])

RESOURCES = [
    {
        "slug": "technical-seo-audit-checklist",
        "name": "A Technical SEO Audit Checklist That Leads to Action",
        "short": "A practical sequence for turning crawl findings into implementation-ready work.",
        "description": "A technical SEO audit checklist covering crawlability, indexation, rendering, performance, structured data, and verification.",
        "category": "Technical SEO",
        "reading": "8 min read",
        "intro": "A useful technical audit is not a folder of exports. It is a prioritised set of decisions with evidence, owners, and acceptance criteria.",
        "sections": [
            {
                "heading": "Start with the business question",
                "paragraphs": [
                    "Before opening a crawler, define what the site needs search engines to do: discover important pages, understand the offers, and index the right version of each template. This prevents a long list of low-impact warnings from becoming the roadmap.",
                    "Write down the primary conversions, the templates that support them, and any recent releases or migrations. Those details usually explain more than a generic health score.",
                ],
                "bullets": [],
            },
            {
                "heading": "Check crawlability and indexation together",
                "paragraphs": [
                    "Crawlability asks whether search engines can reach a page. Indexation asks whether the page deserves to be selected as the canonical result. Review them together so you do not fix one while worsening the other.",
                ],
                "bullets": [
                    "Compare sitemap URLs with indexable internal links and important templates.",
                    "Review robots directives, status codes, redirect chains, and canonical tags as a group.",
                    "Look for parameter URLs, faceted navigation, and near-duplicate templates creating competing versions.",
                    "Confirm that important content is present in the rendered page, not hidden behind an unnecessary interaction.",
                ],
            },
            {
                "heading": "Turn findings into engineering-ready work",
                "paragraphs": [
                    "Every recommendation should include the affected template, the evidence, the expected effect, a severity, and a way to verify the fix. That format makes trade-offs visible and avoids a cycle of repeated audits.",
                ],
                "bullets": [
                    "Group root-cause fixes separately from one-off URL corrections.",
                    "Add acceptance criteria that can be checked after release.",
                    "Record the date of implementation so later changes in search data can be interpreted.",
                ],
            },
            {
                "heading": "Verify after release",
                "paragraphs": [
                    "An audit is only complete when the expected change is confirmed. Recrawl affected templates, inspect rendered output, validate structured data, and watch coverage and performance signals over a sensible window.",
                ],
                "bullets": [],
                "callout": "Prioritise fixes that unlock important templates. A small number of root-cause changes usually beats a long tail of cosmetic warnings.",
            },
        ],
    },
    {
        "slug": "choosing-seo-keywords-that-convert",
        "name": "Choosing SEO Keywords That Actually Convert",
        "short": "Move from search volume to intent, business fit, and a clear page owner.",
        "description": "A framework for selecting SEO keywords based on commercial fit, intent, SERP evidence, and the page that should own the query.",
        "category": "Strategy",
        "reading": "7 min read",
        "intro": "High search volume is not a strategy. A keyword is useful only when the intent, your offer, and the page designed to serve it line up.",
        "sections": [
            {
                "heading": "Begin with the decision, not the phrase",
                "paragraphs": [
                    "List the decisions a prospective customer makes: understanding a problem, comparing approaches, evaluating providers, and taking action. Keywords are simply one visible expression of those decisions.",
                    "For each decision, ask what evidence would make the next step easier. That question leads to a better page than a spreadsheet sorted by volume.",
                ],
                "bullets": [],
            },
            {
                "heading": "Read the search results as evidence",
                "paragraphs": [
                    "The current results show what search engines believe the intent to be. Note the page types, the depth of information, the commercial signals, and the questions that competitors leave unanswered.",
                ],
                "bullets": [
                    "Are results dominated by product pages, guides, directories, comparisons, or local listings?",
                    "Do pages answer the query directly or force the visitor to assemble the answer?",
                    "Is there a clear gap in proof, implementation detail, or pricing context?",
                    "Can your business credibly satisfy the intent behind the query?",
                ],
            },
            {
                "heading": "Assign one primary owner",
                "paragraphs": [
                    "Keyword cannibalisation is usually an architecture problem. For each priority intent, choose one primary URL and define the supporting pages that link to it. This gives internal links, briefs, and reporting a stable reference point.",
                ],
                "bullets": [
                    "Map each keyword cluster to a single primary page.",
                    "Give supporting pages a distinct question or angle.",
                    "Use descriptive internal links to reinforce the hierarchy.",
                ],
            },
            {
                "heading": "Score opportunity honestly",
                "paragraphs": [
                    "Combine search evidence with business value, current capability, and effort. A lower-volume query with clear purchase intent and a weak set of results may be a better first move than a broad head term.",
                ],
                "bullets": [],
                "callout": "A keyword-to-URL map is the simplest way to expose overlap. If two pages need the same primary keyword, the site architecture needs a decision.",
            },
        ],
    },
    {
        "slug": "local-seo-foundation-checklist",
        "name": "The Local SEO Foundation Checklist",
        "short": "The data, profile, page, and reputation basics that make local visibility durable.",
        "description": "A local SEO checklist covering business profiles, consistent data, useful location pages, reviews, structured data, and measurement.",
        "category": "Local SEO",
        "reading": "6 min read",
        "intro": "Local SEO is built on consistency and usefulness. The goal is not to publish dozens of near-identical city pages, but to make every legitimate location easy to verify and choose.",
        "sections": [
            {
                "heading": "Create one source of truth",
                "paragraphs": [
                    "Document the accurate business name, address, phone number, opening hours, service areas, categories, and profile URLs. Use that source everywhere so updates do not drift across platforms.",
                ],
                "bullets": [
                    "Use the same core business details on the site and priority listings.",
                    "Choose primary categories carefully; do not add every loosely related category.",
                    "Keep a record of profile ownership and update dates.",
                ],
            },
            {
                "heading": "Build location pages with real substance",
                "paragraphs": [
                    "A useful location page explains what is available in that area, who the team serves, and what the visitor should do next. Swapping a city name in the same paragraph does not create local relevance.",
                ],
                "bullets": [
                    "Include genuinely area-specific services, availability, or context.",
                    "Link to relevant service and industry pages.",
                    "Add clear contact and conversion actions.",
                    "Avoid claiming a physical presence that does not exist.",
                ],
            },
            {
                "heading": "Earn trust with a repeatable process",
                "paragraphs": [
                    "Reviews work best when the request is part of normal customer service, not a one-off campaign. Ask consistently, follow platform policies, and respond in a way that is useful to future readers.",
                ],
                "bullets": [
                    "Make the review request easy to find after a completed service.",
                    "Never gate or incentivise reviews in ways that violate platform rules.",
                    "Use responses to add context, not defensiveness.",
                ],
            },
            {
                "heading": "Measure local actions",
                "paragraphs": [
                    "Track actions that reflect local intent: qualified enquiries, calls, direction requests, profile interactions, and location-page conversions. Keep branded demand visible so it does not mask non-branded growth.",
                ],
                "bullets": [],
                "callout": "Treat the location hub as architecture, not decoration. It should help people and search engines understand how every service area fits together.",
            },
        ],
    },
    {
        "slug": "practical-seo-measurement",
        "name": "A Practical SEO Measurement Setup",
        "short": "Define conversions, build a compact dashboard, and report decisions instead of noise.",
        "description": "A practical guide to SEO measurement: conversion definitions, tracking QA, dashboards, attribution context, and monthly decision notes.",
        "category": "Measurement",
        "reading": "7 min read",
        "intro": "SEO reporting becomes useful when the team agrees on what a good outcome looks like and which evidence can be trusted.",
        "sections": [
            {
                "heading": "Define outcomes before metrics",
                "paragraphs": [
                    "Start with the business action: a qualified enquiry, a trial, a purchase, or another meaningful event. Then choose supporting metrics that explain movement toward that action.",
                    "Separate primary conversions from helpful but weaker signals. A newsletter signup and a sales-qualified enquiry should not carry the same weight.",
                ],
                "bullets": [],
            },
            {
                "heading": "Validate the data",
                "paragraphs": [
                    "Before interpreting a trend, confirm that tracking fires once, values are consistent, internal traffic is filtered appropriately, and recent site changes have not broken events.",
                ],
                "bullets": [
                    "Test key forms and calls to action end to end.",
                    "Check that conversions are attributed to the right page or journey where possible.",
                    "Keep a release log so sudden changes can be explained.",
                    "Use Search Console for search-query context, not as a complete conversion model.",
                ],
            },
            {
                "heading": "Design one decision-focused view",
                "paragraphs": [
                    "A dashboard should help someone choose the next action. Keep definitions visible, use consistent date comparisons, and avoid charts that nobody uses to make a decision.",
                ],
                "bullets": [
                    "Show primary conversions next to qualified organic sessions or visits.",
                    "Include work completed, not just outcomes, so activity and impact can be read together.",
                    "Annotate releases, migrations, seasonality, and major algorithm updates.",
                ],
            },
            {
                "heading": "Report the interpretation",
                "paragraphs": [
                    "Numbers do not speak for themselves. Each reporting cycle should state what changed, the most plausible explanation, confidence level, and the decision that follows.",
                ],
                "bullets": [],
                "callout": "Be explicit about attribution limits. Honest context builds more trust than a precise-looking chart based on uncertain data.",
            },
        ],
    },
    {
        "slug": "seo-cost-india",
        "name": "SEO Cost in India: A Practical Pricing Guide for 2026",
        "short": "Understand pricing models, scope variables and the questions to ask before comparing quotes.",
        "description": "A practical guide to SEO pricing in India covering retainers, audits, projects, scope, deliverables and proposal red flags without unverified price claims.",
        "category": "SEO Strategy",
        "reading": "7 min read",
        "intro": "SEO quotes are difficult to compare because two proposals with the same monthly fee can describe completely different work. Start by comparing scope, evidence and ownership.",
        "sections": [
            {
                "heading": "Start with the engagement model",
                "paragraphs": [
                    "A one-time audit, an advisory retainer, a technical implementation project and a full organic growth programme solve different problems. Asking for a single SEO price before defining the model usually produces an unreliable comparison.",
                ],
                "bullets": [
                    "Audit: a bounded review that ends with prioritised findings and recommendations.",
                    "Consulting: recurring strategy, QA and decision support for an in-house team.",
                    "Project: a defined build such as a migration, information architecture or measurement setup.",
                    "Programme: ongoing strategy, implementation support, content planning and reporting.",
                ],
            },
            {
                "heading": "What genuinely changes the scope",
                "paragraphs": [
                    "The right scope depends on the site, the market and the team—not just the number of keywords on a proposal.",
                ],
                "bullets": [
                    "Site size, template complexity and existing technical debt.",
                    "Competitive intensity and the maturity of current content.",
                    "Number of services, industries and real service areas.",
                    "Available writing, design and development capacity.",
                    "Quality of current analytics and conversion tracking.",
                ],
            },
            {
                "heading": "Questions to ask before comparing proposals",
                "paragraphs": [
                    "A useful proposal should make the work visible. If deliverables are vague, the fee is impossible to evaluate.",
                ],
                "bullets": [
                    "What will be reviewed in the first thirty days?",
                    "Who owns implementation, and how are recommendations written?",
                    "Which deliverables remain with the business after the engagement?",
                    "How are conversions defined and reported?",
                    "What is explicitly out of scope?",
                ],
            },
            {
                "heading": "Red flags",
                "paragraphs": [
                    "Low-cost SEO can become expensive when it creates technical debt, duplicate pages or reporting that hides poor-quality enquiries.",
                ],
                "bullets": [
                    "Guaranteed rankings or fixed-position promises.",
                    "Bulk backlink packages with no editorial rationale.",
                    "Large volumes of near-identical city pages.",
                    "Reports made only of screenshots and vanity metrics.",
                    "No written scope, owner or measurement definition.",
                ],
                "callout": "Compare proposals on transparent scope, decision-quality reporting and what your team keeps afterwards—not the cheapest headline fee.",
            },
        ],
    },
    {
        "slug": "choose-seo-consultant-india",
        "name": "How to Choose an SEO Consultant in India",
        "short": "A due-diligence framework for evaluating expertise, process, evidence and working fit.",
        "description": "A practical framework for choosing an SEO consultant in India, covering goals, diagnostics, evidence, communication, reporting and red flags.",
        "category": "SEO Strategy",
        "reading": "8 min read",
        "intro": "The best consultant for one business may be wrong for another. Evaluate the fit between your goals, internal capacity and the consultant’s actual working method.",
        "sections": [
            {
                "heading": "Define the outcome before shortlisting",
                "paragraphs": [
                    "Write down the business action you want more of: qualified enquiries, demos, purchases, local visits or another measurable event. Also list the team capacity available for implementation.",
                    "That brief makes it much easier to distinguish a strategist, a technical specialist, a local SEO practitioner and a full-service team.",
                ],
                "bullets": [],
            },
            {
                "heading": "Evaluate the diagnostic approach",
                "paragraphs": [
                    "Ask how the first month would work. A credible process should include discovery, evidence gathering, root-cause analysis and prioritisation—not an instant list of generic fixes.",
                ],
                "bullets": [
                    "What data and access would be requested?",
                    "How are technical issues separated from content and conversion problems?",
                    "How are recommendations prioritised and assigned owners?",
                    "What would count as a completed fix?",
                ],
            },
            {
                "heading": "Ask for evidence without demanding guarantees",
                "paragraphs": [
                    "Case studies are useful when they explain the starting constraint, the decisions made, the work shipped and the measurement limits. Ranking guarantees are not evidence; they are a warning sign.",
                ],
                "bullets": [
                    "Look for original examples and clear before/after context.",
                    "Ask what did not work and how the approach changed.",
                    "Check whether results are tied to qualified outcomes, not just traffic.",
                    "Verify that any confidential client details are shared with permission.",
                ],
            },
            {
                "heading": "Confirm the working model",
                "paragraphs": [
                    "Good working relationships are explicit about communication, documentation, approvals and handover. These details matter as much as the initial strategy.",
                ],
                "bullets": [
                    "Who is the day-to-day point of contact?",
                    "What documentation and artefacts are handed over?",
                    "How often are priorities reviewed?",
                    "What happens when engineering or content capacity changes?",
                ],
                "callout": "Choose the consultant who can explain trade-offs clearly. Confidence without a visible process is not expertise.",
            },
        ],
    },
    {
        "slug": "local-seo-indian-businesses",
        "name": "Local SEO Strategy for Indian Businesses",
        "short": "A practical foundation for profiles, location pages, reviews and local measurement.",
        "description": "A local SEO strategy for Indian businesses covering business data, Google Business Profiles, useful location pages, reviews, structured data and measurement.",
        "category": "Local SEO",
        "reading": "7 min read",
        "intro": "Local SEO works when a business is easy to verify, easy to understand and easy to contact. Consistency and genuinely useful pages matter more than publishing a page for every nearby pin code.",
        "sections": [
            {
                "heading": "Create one source of truth for business data",
                "paragraphs": [
                    "Document the accurate name, address, phone number, hours, service areas, categories and profile URLs. Use that source across the website, business profiles and priority listings so updates do not drift.",
                ],
                "bullets": [
                    "Keep a record of who owns each profile.",
                    "Use primary categories deliberately rather than adding every loosely related option.",
                    "Record the date of every material business-information change.",
                ],
            },
            {
                "heading": "Build location pages with real local substance",
                "paragraphs": [
                    "A useful location page explains what is available in that area, who the business serves, and what the visitor should do next. Swapping only the city name is not a local strategy.",
                ],
                "bullets": [
                    "Add area-specific services, availability or context.",
                    "Link to relevant service and industry pages.",
                    "Use consistent contact details and clear conversion actions.",
                    "Avoid claiming a physical presence that does not exist.",
                ],
            },
            {
                "heading": "Make reputation a repeatable process",
                "paragraphs": [
                    "Reviews work best when requests are part of normal customer service and responses are useful to future readers. Follow platform policies and never gate or incentivise reviews improperly.",
                ],
                "bullets": [
                    "Ask after a completed service through a simple, consistent workflow.",
                    "Respond with context rather than defensiveness.",
                    "Watch for duplicate profiles and inconsistent business details.",
                ],
            },
            {
                "heading": "Measure local actions separately",
                "paragraphs": [
                    "Track qualified enquiries, calls, direction requests, profile interactions and location-page conversions. Keep branded demand visible so it does not mask growth in non-branded local discovery.",
                ],
                "bullets": [],
                "callout": "A location hub should be architecture, not decoration. It should help people and search engines understand how each genuine service area fits together.",
            },
        ],
    },
    {
        "slug": "seo-vs-google-ads-india",
        "name": "SEO vs Google Ads for Indian Businesses: How to Decide",
        "short": "Choose channels based on intent, timeline, budget control and the quality of measurement.",
        "description": "A practical comparison of SEO and Google Ads for Indian businesses, including time horizons, intent, budget control, landing pages and measurement.",
        "category": "Paid & Organic",
        "reading": "6 min read",
        "intro": "SEO and Google Ads are not competing ideologies. They are different ways to capture demand, and the right mix depends on timing, margins and how reliably conversions can be measured.",
        "sections": [
            {
                "heading": "Understand the different jobs",
                "paragraphs": [
                    "Organic search builds durable visibility across research, comparison and decision-stage queries. Paid search buys immediate presence on selected queries, with much tighter control over budget and targeting.",
                ],
                "bullets": [
                    "SEO is better suited to compounding content, technical improvements and broader intent coverage.",
                    "Google Ads is useful for launches, seasonal demand and testing message-market fit.",
                    "Both depend on a landing page that matches the query and makes the next action clear.",
                ],
            },
            {
                "heading": "Consider timeline and budget control",
                "paragraphs": [
                    "Paid search can generate traffic quickly but stops when spend stops. Organic work usually takes longer to show movement, but useful pages and technical improvements can keep paying off after the initial work.",
                ],
                "bullets": [
                    "Use paid search when a date-specific campaign needs immediate visibility.",
                    "Use SEO when the business can invest in durable architecture and content.",
                    "Review margin and conversion value before judging either channel on traffic alone.",
                ],
            },
            {
                "heading": "Use shared evidence",
                "paragraphs": [
                    "Search-term reports, conversion language and landing-page behaviour from paid campaigns can inform SEO priorities. Organic query data can reveal gaps worth testing in paid search.",
                ],
                "bullets": [
                    "Compare high-converting paid queries with organic content coverage.",
                    "Use the same conversion definitions wherever possible.",
                    "Keep brand and non-brand demand separated in reporting.",
                ],
            },
            {
                "heading": "A simple decision framework",
                "paragraphs": [
                    "Start with the business question, not the channel. If the need is immediate and measurable, paid search may lead. If the constraint is weak architecture or thin decision-stage content, SEO should lead.",
                ],
                "bullets": [],
                "callout": "The strongest programmes use clean measurement and shared landing-page learning across both channels.",
            },
        ],
    },
]

RESOURCES.insert(
    0,
    {
        "slug": "location-pages-without-doorway-risk",
        "name": "City Pages Without Doorway Risk: The Test I Use",
        "short": "One question decides whether a city page should exist — and what to do with the ones that shouldn’t.",
        "description": "How to build city and service-area pages Google treats as useful, not doorways: the city-name test, what each page needs, and when to merge or hold a page back.",
        "category": "Local SEO",
        "reading": "7 min read",
        "intro": "Most multi-city sites don’t have too few location pages. They have too many that say the same thing. This is the test I apply before any city page goes live, and what I do with the pages that fail it.",
        "sections": [
            {
                "heading": "What Google actually objects to",
                "paragraphs": [
                    "Google’s spam policies describe doorway pages as pages created to rank for similar, specific searches — for example a set of city pages that all funnel visitors to the same place, or near-identical pages that sit closer to search results than to a useful, browsable site. The problem is not having city pages. It is having city pages with nothing different to say.",
                    "The same policies cover scaled content: publishing many pages mainly to manipulate rankings, whether they are written by hand, generated from a template or produced with AI. A shared template is fine. A template where only the city name changes is not.",
                ],
                "bullets": [],
            },
            {
                "heading": "The city-name test",
                "paragraphs": [
                    "Before a city page ships, swap the city name for another city and read the page again. Is it still true?",
                    "If the page is still true with a different city in it, it is a doorway page wearing a city name and it should not be published yet. If the swap makes sentences false — the wrong authority, the wrong sectors, the wrong projects — the page is genuinely about that place.",
                ],
                "bullets": [],
                "callout": "Swap the city name. If the page is still true, it isn’t ready. If the swap makes it false, it’s a real city page.",
            },
            {
                "heading": "What a real city page needs",
                "paragraphs": [
                    "Three things, in this order of importance:",
                ],
                "bullets": [
                    "A local fact that is not the city name: the authority that issues an approval, the sectors that dominate, how people there actually search.",
                    "An honest statement of where the work was done. No local project yet? Say so plainly — it costs far less trust than a vague claim.",
                    "A reason to get in touch from that city: how you deliver there, what you need to quote, and what happens next.",
                ],
            },
            {
                "heading": "When one regional page beats three city pages",
                "paragraphs": [
                    "Regions like Delhi NCR are the clearest case. Delhi, Gurugram and Noida are searched separately, but for most businesses the honest content is the same. One regional page that covers each city properly is stronger than three thin pages competing with one another.",
                    f"In one client programme, a single Delhi NCR page reached #4 on Google for its main term ({RESULTS_DATE} check) without a published local project. It ranked on structure, clarity and proof from other cities.",
                ],
                "bullets": [],
            },
            {
                "heading": "What to do with pages that fail",
                "paragraphs": [
                    "Don’t leave them live and hope. Choose one of three actions:",
                ],
                "bullets": [
                    "Merge: 301-redirect the thin page to the strongest relevant page and move anything genuinely useful across.",
                    "Hold back: keep the page out of the index and out of navigation until it has distinct content.",
                    "Earn it: add the local facts, proof and next step that make it pass the test, then publish.",
                ],
                "callout": "On this site, the Mumbai and Pune pages were redirected and the Kochi page became one Kerala page on 27 November 2026. The five remaining city pages each pass the test.",
            },
            {
                "heading": "Keep the home page out of the fight",
                "paragraphs": [
                    "A common self-inflicted problem: the home page targets the same city as the city page, so the two compete and neither ranks well. Let the home page claim the country or the category, and let each city page own its city.",
                ],
                "bullets": [],
            },
        ],
    },
)

RESOURCE_SERVICE_LINKS = {
    "location-pages-without-doorway-risk": ["local-seo", "content-strategy", "seo-consulting"],
    "technical-seo-audit-checklist": ["technical-seo", "seo-services", "analytics-reporting"],
    "choosing-seo-keywords-that-convert": ["content-strategy", "seo-consulting", "analytics-reporting"],
    "local-seo-foundation-checklist": ["local-seo", "website-design", "analytics-reporting"],
    "practical-seo-measurement": ["analytics-reporting", "seo-consulting", "google-ads-management"],
    "seo-cost-india": ["seo-consulting", "seo-services", "analytics-reporting"],
    "choose-seo-consultant-india": ["seo-consulting", "technical-seo", "analytics-reporting"],
    "local-seo-indian-businesses": ["local-seo", "website-design", "analytics-reporting"],
    "seo-vs-google-ads-india": ["google-ads-management", "seo-services", "analytics-reporting"],
}

STATIC_LABELS = {
    "about": "About",
    "services": "Services",
    "industries": "Industries",
    "locations": "Locations",
    "resources": "Resources",
    "case-studies": "Case studies",
    "free-seo-review": "Free SEO review",
    "contact": "Contact",
    "thank-you": "Thank you",
    "privacy": "Privacy Policy",
    "terms": "Terms",
}

CASE_STUDIES = [
    {
        "slug": "mindtech-solutions-mep-seo",
        "name": "Multi-city SEO for an MEP contractor",
        "crumb": "Mindtech Solutions",
        "client": "Mindtech Solutions",
        "client_url": "https://mindtechsolutions.co.in/",
        "sector": "MEP, HVAC and fit-out contracting",
        "markets": "Bengaluru, Hyderabad, Chennai, Delhi NCR — and India nationally",
        "role": "SEO strategy, website, lead tracking and release management",
        "period": "August to November 2026 (ongoing)",
        "short": "From brand-only searches to page 1 for five commercial terms — and a national Google AI Overview citation.",
        "title": "Case Study: Multi-City SEO for an MEP Contractor",
        "description": "How an MEP contractor went from brand-only Google visibility to page 1 for five commercial terms in about three months, plus a national AI Overview citation.",
        "h1": "From brand-only searches to page 1: multi-city SEO for an MEP contractor",
        "lede": (
            "Mindtech Solutions is an MEP, HVAC and fit-out contractor working across India. "
            "When the baseline was recorded in August 2026, Google showed the site almost only "
            "to people who already knew the name. By November it held page-1 positions in two "
            "markets and appeared in Google’s AI Overview for MEP contractors in India."
        ),
        "start": [
            "Google Search Console showed the site mainly for brand searches — people typing the company name.",
            "None of the client’s 15 priority commercial keywords had produced a single reportable impression.",
            "Search Console still listed several commercial pages as discovered but not yet indexed.",
            "Enquiries arrived by phone and email with no record of which page or search produced them.",
        ],
        "timeline": [
            ("Aug 2026", "Indexation and keyword baseline", "Audited crawl and indexation, confirmed every commercial page had one H1, a self-referencing canonical and sitemap inclusion, and recorded a keyword baseline before changing anything."),
            ("Aug 2026", "Money-page metadata", "Aligned titles, descriptions and H1s on the four priority service pages, then verified the live pages byte-for-byte against the approved source."),
            ("Sep 2026", "Privacy-safe lead tracking", "Consent-based GA4 and Microsoft Clarity, a reference number on every enquiry and source and landing-page fields — proved end to end with controlled test enquiries."),
            ("Sep 2026", "Commercial SEO on the money pages", "Rewrote the commercial pages around buyer intent and added the sections buyers look for before they ask for a quote."),
            ("Oct 2026", "Proof beside the claim", "Approved project cards, an ISO 9001:2015 certification link and FAQs with matching structured data on the Bengaluru MEP page, plus contextual links from related pages. A project write-up gained Article and VideoObject structured data."),
            ("Oct–Nov 2026", "Design system and safe releases", "A design-token system with automated consistency checks, then release automation with a tested rollback, so SEO changes could ship often without breaking the site."),
            ("Nov 2026", "City pages that pass the test", "Hyderabad, Chennai and Delhi NCR pages built on local authorities, local sectors and an honest line about where work was done. Thin service × city combinations were held back or redirected instead of published."),
            ("Nov 2026", "Home page goes national", "Retargeted the home page to India with a headline that names no city, so it stopped competing with the Bengaluru page for the same searches."),
            ("Nov 2026", "AI search corroboration", "When a business directory appeared among the sources of the AI Overview, the client was submitted to it to strengthen third-party corroboration."),
        ],
        "method": [
            {"tag": "01", "title": "One page per intent", "text": "Each service and city page has a single job. The home page claims India; each city page claims its city."},
            {"tag": "02", "title": "The city-name test", "text": "A city page ships only if swapping the city name would make it false. Otherwise it is held back or merged."},
            {"tag": "03", "title": "Proof next to claims", "text": "Approved projects, certifications and video sit on the page that makes the claim, mirrored in structured data."},
            {"tag": "04", "title": "Releases with evidence", "text": "Every change goes through a reviewed pull request, automated checks, a staging preview and a rollback point."},
        ],
        "differently": [
            "Start third-party corroboration earlier. The AI Overview’s sources included a business directory and an industry list; listings like that take weeks to approve, so they should begin alongside the on-page work, not after it.",
            "Collect Google Business Profile facts in week one. The client is not yet in any map pack, and profile work depends on business inputs that take time to gather.",
        ],
    },
]

LABEL_LOOKUP = dict(STATIC_LABELS)
for collection in (SERVICES, INDUSTRIES, LOCATIONS, RESOURCES, CASE_STUDIES, *STATE_CITIES.values()):
    for item in collection:
        LABEL_LOOKUP[item["slug"]] = item.get("crumb", item["name"])

SERVICE_BY_SLUG = {item["slug"]: item for item in SERVICES}
INDUSTRY_BY_SLUG = {item["slug"]: item for item in INDUSTRIES}
LOCATION_BY_SLUG = {item["slug"]: item for item in LOCATIONS}
RESOURCE_BY_SLUG = {item["slug"]: item for item in RESOURCES}

SERVICE_SEO_TITLES = {
    "seo-consulting": "SEO Consulting Services India | Senior SEO Consultant",
    "technical-seo": "Technical SEO Consultant India | Audits & Implementation",
    "local-seo": "Local SEO Services India | Profiles & Location Pages",
    "ai-search-optimization": "AI SEO Expert India | AI Search Optimisation (AEO, GEO)",
    "seo-services": "SEO Services India | Organic Growth Programme",
    "content-strategy": "SEO Content Strategy India | Topic Clusters & Briefs",
    "analytics-reporting": "SEO Analytics & Reporting India | GA4 & Search Console",
    "google-ads-management": "Google Ads Management India | Paid Search Consulting",
    "website-design": "SEO-Ready Website Design India | Fast Static Sites",
}

INDUSTRY_SEO_TITLES = {
    "construction-mep-contractors": "SEO for Construction & MEP Contractors | Sreejith Digital",
    "b2b-saas": "B2B & SaaS SEO India | Sreejith Digital",
    "professional-services": "SEO for Professional Services Firms | Sreejith Digital",
    "ecommerce": "Ecommerce SEO India | Category & Technical SEO",
    "local-multi-location": "Multi-Location SEO India | Sreejith Digital",
}


INDUSTRY_H1 = {
    "construction-mep-contractors": "SEO for construction & MEP contractors",
    "b2b-saas": "SEO for B2B and SaaS companies",
    "professional-services": "SEO for professional services firms",
    "ecommerce": "Ecommerce SEO for Indian online stores",
    "local-multi-location": "SEO for local and multi-location businesses",
}


def branded(title: str, limit: int = 62) -> str:
    """Append the brand only when the title stays readable in results."""
    suffix = f" | {SITE_NAME}"
    if SITE_NAME in title or len(title) + len(suffix) > limit:
        return title
    return title + suffix


def child_links(root: str, label: str, items: list[dict], overview: str) -> list[dict]:
    links = [{
        "label": f"All {label.lower()}",
        "href": root,
        "description": overview,
        "featured": True,
    }]
    for item in items:
        links.append(
            {
                "label": item["name"],
                "href": f"{root}{item['slug']}/",
                "description": item["short"],
            }
        )
    return links


NAV_ITEMS = [
    {"label": "About", "href": "/about/"},
    {
        "label": "Services",
        "href": "/services/",
        "children": child_links(
            "/services/", "Services", SERVICES, "See every service and how they connect"
        ),
    },
    {"label": "Work", "href": "/case-studies/"},
    {
        "label": "Industries",
        "href": "/industries/",
        "children": child_links(
            "/industries/", "Industries", INDUSTRIES, "See sector-specific search approaches"
        ),
    },
    {
        "label": "Locations",
        "href": "/locations/",
        "children": child_links(
            "/locations/", "Locations", LOCATIONS, "Where I work and what I’ve done there"
        ),
    },
    {
        "label": "Resources",
        "href": "/resources/",
        "children": child_links(
            "/resources/", "Resources", RESOURCES, "Browse practical guides and checklists"
        ),
    },
    {"label": "Contact", "href": "/contact/"},
]


def is_active(href: str, current: str) -> bool:
    if href == "/":
        return current == "/"
    return current == href or current.startswith(href)


def render_nav(current: str) -> str:
    output = []
    for item in NAV_ITEMS:
        active = is_active(item["href"], current)
        if item.get("children"):
            group_active = any(is_active(child["href"], current) for child in item["children"])
            children = []
            for child in item["children"]:
                current_attr = ' aria-current="page"' if current == child["href"] else ""
                link_class = (
                    "nav-panel__link nav-panel__link--overview"
                    if child.get("featured")
                    else "nav-panel__link"
                )
                children.append(
                    f'<a class="{link_class}" href="{e(child["href"])}"{current_attr}>'
                    f'<strong>{e(child["label"])}</strong>'
                    f'<span>{e(child["description"])}</span></a>'
                )
            output.append(
                f'''<li>
  <details class="nav-group"{' data-active="true"' if group_active else ''}>
    <summary class="nav-link"{' data-current="true"' if active else ''}>
      {e(item["label"])}<span class="nav-chevron" aria-hidden="true">⌄</span>
    </summary>
    <div class="nav-panel">
      <p class="nav-panel__label">Explore {e(item["label"])}</p>
      {''.join(children)}
    </div>
  </details>
</li>'''
            )
        else:
            current_attr = ' aria-current="page"' if active else ""
            output.append(
                f'<li><a class="nav-link" href="{e(item["href"])}"{current_attr}>{e(item["label"])}</a></li>'
            )
    return f'<ul class="nav-list">{"".join(output)}</ul>'


def render_header(current: str) -> str:
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header" data-header>
  <div class="container header-inner">
    <a class="brand" href="/" aria-label="{e(SITE_NAME)} home">
      <span class="brand__mark" aria-hidden="true"><span></span></span>
      <span class="brand__text">SREEJITH <span>DIGITAL</span></span>
    </a>
    <nav class="primary-nav" id="primary-nav" data-primary-nav aria-label="Primary navigation">
      {render_nav(current)}
    </nav>
    <a class="btn btn--small btn--primary header-cta" href="/free-seo-review/">Free SEO review <span aria-hidden="true">→</span></a>
    <button class="nav-toggle" type="button" data-nav-toggle aria-controls="primary-nav" aria-expanded="false" aria-label="Open navigation">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>'''


def analytics_enabled() -> bool:
    return bool(GTM_CONTAINER_ID or GA4_MEASUREMENT_ID or CLARITY_PROJECT_ID)


def render_footer() -> str:
    service_links = "".join(
        f'<li><a href="/services/{e(item["slug"])}/">{e(item["name"])}</a></li>'
        for item in SERVICES[:6]
    )
    explore_links = "".join(
        f'<li><a href="{e(href)}">{e(label)}</a></li>'
        for label, href in [
            ("About", "/about/"),
            ("Case studies", "/case-studies/"),
            ("Industries", "/industries/"),
            ("Locations", "/locations/"),
            ("Resources", "/resources/"),
            ("Free SEO review", "/free-seo-review/"),
            ("Contact", "/contact/"),
        ]
    )
    cookie_link = (
        '<li><button class="footer-link-button" type="button" data-consent-open>Cookie settings</button></li>'
        if analytics_enabled()
        else ""
    )
    return f'''<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-intro">
      <a class="brand" href="/" aria-label="{e(SITE_NAME)} home">
        <span class="brand__mark" aria-hidden="true"><span></span></span>
        <span class="brand__text">SREEJITH <span>DIGITAL</span></span>
      </a>
      <p>Senior SEO consulting by {e(OWNER_NAME)}. Based in {e(OWNER_BASE_CITY)}, working with businesses across India. Dated results, no ranking promises.</p>
      <a class="footer-email" href="mailto:{e(CONTACT_EMAIL)}">{e(CONTACT_EMAIL)}</a>
    </div>
    <div class="footer-column">
      <h2>Services</h2>
      <ul>{service_links}</ul>
    </div>
    <div class="footer-column">
      <h2>Explore</h2>
      <ul>{explore_links}</ul>
    </div>
    <div class="footer-column">
      <h2>Company</h2>
      <ul>
        <li><a href="/privacy/">Privacy Policy</a></li>
        <li><a href="/terms/">Terms</a></li>
        {cookie_link}
      </ul>
    </div>
  </div>
  <div class="container footer-bottom">
    <p>© <span data-year>2026</span> {e(SITE_NAME)} · {e(OWNER_NAME)}</p>
    <p>{e(OWNER_BASE_CITY)}, India · Remote-first across India</p>
  </div>
</footer>'''


def breadcrumb_items(path: str) -> list[tuple[str, str | None]]:
    if path == "/":
        return [("Home", None)]
    parts = [part for part in path.strip("/").split("/") if part]
    crumbs: list[tuple[str, str | None]] = [("Home", "/")]
    accumulated = ""
    for index, part in enumerate(parts):
        accumulated += f"/{part}"
        label = LABEL_LOOKUP.get(part, part.replace("-", " ").title())
        is_last = index == len(parts) - 1
        crumbs.append((label, None if is_last else accumulated + "/"))
    return crumbs


def breadcrumb_schema(path: str) -> dict:
    crumbs = breadcrumb_items(path)
    elements = []
    for index, (label, href) in enumerate(crumbs, start=1):
        item = {
            "@type": "ListItem",
            "position": index,
            "name": label,
        }
        item["item"] = BASE_URL + (href if href else path)
        elements.append(item)
    return {
        "@type": "BreadcrumbList",
        "@id": BASE_URL + path + "#breadcrumb",
        "itemListElement": elements,
    }


def render_breadcrumbs(path: str) -> str:
    crumbs = breadcrumb_items(path)
    parts = []
    for label, href in crumbs:
        if href:
            parts.append(f'<li><a href="{e(href)}">{e(label)}</a></li>')
        else:
            parts.append(f'<li aria-current="page">{e(label)}</li>')
    return f'<nav class="breadcrumbs" aria-label="Breadcrumb"><ol>{"".join(parts)}</ol></nav>'


def person_node() -> dict:
    person = {
        "@type": "Person",
        "@id": PERSON_ID,
        "name": OWNER_NAME,
        "jobTitle": OWNER_JOB_TITLE,
        "url": BASE_URL + "/about/",
        "worksFor": {"@id": BUSINESS_ID},
        "homeLocation": {"@type": "Place", "name": "Chennai, Tamil Nadu, India"},
        "knowsAbout": OWNER_KNOWS_ABOUT,
    }
    if OWNER_PHOTO:
        person["image"] = BASE_URL + OWNER_PHOTO
    if OWNER_PROFILES:
        person["sameAs"] = OWNER_PROFILES
    if OWNER_LANGUAGES:
        person["knowsLanguage"] = OWNER_LANGUAGES
    return person


def business_node() -> dict:
    return {
        "@type": "ProfessionalService",
        "@id": BUSINESS_ID,
        "name": SITE_NAME,
        "url": BASE_URL + "/",
        "description": DEFAULT_DESCRIPTION,
        "email": CONTACT_EMAIL,
        "image": BASE_URL + OG_IMAGE,
        "logo": {
            "@type": "ImageObject",
            "url": BASE_URL + "/assets/img/icon-512.png",
            "width": 512,
            "height": 512,
        },
        "founder": {"@id": PERSON_ID},
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Chennai",
            "addressRegion": "Tamil Nadu",
            "addressCountry": "IN",
        },
        "areaServed": [
            {"@type": place["@type"], "name": place["name"], "sameAs": place["sameAs"]}
            for place in [COUNTRY_PLACE, *LOCATION_PLACES.values()]
        ] + [
            {"@type": "City", "name": city["name"], "sameAs": WIKI + city["wiki"]}
            for cities in STATE_CITIES.values()
            for city in cities
        ],
        "knowsAbout": OWNER_KNOWS_ABOUT,
    }


def base_schema(path: str, title: str, description: str, page_type: str, about_id: str) -> list[dict]:
    web_site = {
        "@type": "WebSite",
        "@id": WEBSITE_ID,
        "url": BASE_URL + "/",
        "name": SITE_NAME,
        "publisher": {"@id": BUSINESS_ID},
        "inLanguage": "en-IN",
    }
    web_page = {
        "@type": page_type,
        "@id": BASE_URL + path + "#webpage",
        "url": BASE_URL + path,
        "name": title,
        "description": description,
        "isPartOf": {"@id": WEBSITE_ID},
        "about": {"@id": about_id},
        "inLanguage": "en-IN",
        "dateModified": LAST_UPDATED,
    }
    if page_type == "ProfilePage":
        web_page["mainEntity"] = {"@id": PERSON_ID}
    graph = [business_node(), person_node(), web_site, web_page]
    if path != "/" and not path.endswith(".html"):
        crumbs = breadcrumb_schema(path)
        web_page["breadcrumb"] = {"@id": crumbs["@id"]}
        graph.append(crumbs)
    return graph


def faq_schema(faqs: list[tuple[str, str]]) -> dict:
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": question,
                "acceptedAnswer": {"@type": "Answer", "text": answer},
            }
            for question, answer in faqs
        ],
    }


def analytics_head() -> str:
    if not analytics_enabled():
        return ""
    config = json.dumps({"gtm": GTM_CONTAINER_ID, "ga4": GA4_MEASUREMENT_ID, "clarity": CLARITY_PROJECT_ID})
    return f"  <script>window.SD_ANALYTICS = {config};</script>\n"


def consent_banner() -> str:
    if not analytics_enabled():
        return ""
    return '''<div class="consent-banner" data-consent-banner hidden role="region" aria-label="Analytics choice">
  <p>May I use analytics (Google Analytics and Microsoft Clarity) to see which pages help visitors? Nothing loads unless you allow it. <a href="/privacy/">Privacy policy</a></p>
  <div class="consent-actions">
    <button class="btn btn--small btn--primary" type="button" data-consent="granted">Allow analytics</button>
    <button class="btn btn--small btn--secondary" type="button" data-consent="denied">No thanks</button>
  </div>
</div>'''


def mobile_cta() -> str:
    return '''<div class="mobile-cta" data-mobile-cta>
  <a class="btn btn--primary" href="/free-seo-review/">Get a free SEO review <span aria-hidden="true">→</span></a>
</div>'''


def render_page(
    *,
    path: str,
    title: str,
    description: str,
    main: str,
    schema_extra: list[dict] | None = None,
    body_class: str = "",
    robots: str = "index, follow",
    og_type: str = "website",
    page_type: str = "WebPage",
    about_id: str = BUSINESS_ID,
    show_mobile_cta: bool = True,
) -> str:
    if len(re.findall(r"<h1\b", main)) != 1:
        raise ValueError(f"Expected exactly one H1 on {path}")
    article_meta = ""
    if og_type == "article":
        article_meta = (
            f'  <meta property="article:published_time" content="{LAST_UPDATED}">\n'
            f'  <meta property="article:modified_time" content="{LAST_UPDATED}">\n'
            f'  <meta property="article:author" content="{e(OWNER_NAME)}">\n'
        )
    canonical = BASE_URL + path
    graph = base_schema(path, title, description, page_type, about_id)
    if schema_extra:
        graph.extend(schema_extra)
    structured_data = json.dumps(
        {"@context": "https://schema.org", "@graph": graph},
        ensure_ascii=False,
        indent=2,
    ).replace("</", "<\\/")
    classes = [body_class] if body_class else []
    if show_mobile_cta:
        classes.append("has-mobile-cta")
    body_class_attr = f' class="{e(" ".join(classes))}"' if classes else ""
    canonical_tag = f'  <link rel="canonical" href="{e(canonical)}">\n' if "noindex" not in robots else ""
    return f'''<!doctype html>
<html lang="en-IN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#050706">
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}">
  <meta name="author" content="{e(OWNER_NAME)}">
  <meta name="robots" content="{e(robots)}">
{canonical_tag}  <meta property="og:type" content="{e(og_type)}">
  <meta property="og:site_name" content="{e(SITE_NAME)}">
  <meta property="og:locale" content="en_IN">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(description)}">
  <meta property="og:url" content="{e(canonical)}">
  <meta property="og:image" content="{BASE_URL}{OG_IMAGE}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Sreejith Digital — SEO consulting, Chennai and across India">
{article_meta}  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{e(title)}">
  <meta name="twitter:description" content="{e(description)}">
  <meta name="twitter:image" content="{BASE_URL}{OG_IMAGE}">
  <link rel="icon" href="/favicon.ico" sizes="48x48">
  <link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <link rel="stylesheet" href="/assets/css/styles.css?v={SITE_VERSION}">
  <script type="application/ld+json">
{structured_data}
  </script>
{analytics_head()}  <script src="/assets/js/main.js?v={SITE_VERSION}" defer></script>
</head>
<body{body_class_attr}>
{render_header(path)}
<main id="main">
{main}
</main>
{render_footer()}
{mobile_cta() if show_mobile_cta else ""}
{consent_banner()}
</body>
</html>
'''


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def output_path(url_path: str) -> Path:
    if url_path == "/":
        return SITE_ROOT / "index.html"
    return SITE_ROOT / url_path.strip("/") / "index.html"


GENERATED_PATHS: list[str] = []
SITEMAP_EXCLUDE = {"/thank-you/"}


def write_page(**kwargs: object) -> None:
    path = str(kwargs["path"])
    GENERATED_PATHS.append(path)
    write_text(output_path(path), render_page(**kwargs))  # type: ignore[arg-type]


def section_header(eyebrow: str, title: str, text: str = "", link: tuple[str, str] | None = None) -> str:
    link_html = ""
    if link:
        link_html = f'<a class="text-link" href="{e(link[1])}">{e(link[0])} <span aria-hidden="true">→</span></a>'
    text_html = f'<p class="section-intro">{e(text)}</p>' if text else ""
    return f'''<div class="section-head">
  <div>
    <p class="eyebrow">{e(eyebrow)}</p>
    <h2>{e(title)}</h2>
    {text_html}
  </div>
  {link_html}
</div>'''


def card_grid(cards: list[dict], columns: int = 3) -> str:
    items = []
    for card in cards:
        tag = ""
        if card.get("status"):
            tag = status_tag(card["status"], card["tag"])
        elif card.get("tag"):
            tag = f'<span class="card__tag">{e(card["tag"])}</span>'
        link = card.get("href")
        link_html = (
            f'<a class="card__link" href="{e(link)}">{e(card.get("link_label", "Learn more"))} <span aria-hidden="true">→</span></a>'
            if link
            else ""
        )
        items.append(
            f'''<article class="card">
  {tag}
  <h3>{e(card["title"])}</h3>
  <p>{e(card["text"])}</p>
  {link_html}
</article>'''
        )
    return f'<div class="card-grid card-grid--{columns}">{"".join(items)}</div>'


def check_list(items: list[str]) -> str:
    return '<ul class="check-list">' + "".join(
        f'<li><span aria-hidden="true">✓</span><span>{e(item)}</span></li>' for item in items
    ) + "</ul>"


def numbered_steps(steps: list[tuple[str, str]]) -> str:
    items = []
    for index, (title, text) in enumerate(steps, start=1):
        items.append(
            f'''<li class="step">
  <span class="step__number">{index:02d}</span>
  <div><h3>{e(title)}</h3><p>{e(text)}</p></div>
</li>'''
        )
    return f'<ol class="steps">{"".join(items)}</ol>'


def faq_html(faqs: list[tuple[str, str]]) -> str:
    items = []
    for question, answer in faqs:
        items.append(
            f'<details class="faq-item"><summary>{e(question)}</summary><div><p>{e(answer)}</p></div></details>'
        )
    return f'<div class="faq-list">{"".join(items)}</div>'


def dash_list(items: list[str]) -> str:
    """Neutral list for problems and open items (ticks would signal success)."""
    return '<ul class="dash-list">' + "".join(f"<li>{e(item)}</li>" for item in items) + "</ul>"


def status_tag(key: str, label: str) -> str:
    return f'<span class="status-tag status-tag--{e(key)}">{e(label)}</span>'


def answer_block(text: str, label: str = "In short") -> str:
    return f'''<div class="answer-block">
  <p class="eyebrow">{e(label)}</p>
  <p>{e(text)}</p>
</div>'''


def rankings_table(rows: list[dict], caption: str) -> str:
    body = "".join(
        f'<tr><td>{e(row["term"])}</td><td>{e(row["city"])}</td><td class="num"><span class="rank">#{row["position"]}</span></td></tr>'
        for row in rows
    )
    return f'''<div class="table-wrap">
  <table class="data-table">
    <caption class="visually-hidden">{e(caption)}</caption>
    <thead><tr><th scope="col">Search term (topic)</th><th scope="col">Market</th><th scope="col" class="num">Google position</th></tr></thead>
    <tbody>{body}</tbody>
  </table>
</div>
<p class="table-note">{e(caption)} Rankings move daily; this is a dated snapshot, not a guarantee.</p>'''


def proof_strip() -> str:
    return f'''<div class="proof-strip">
  <div class="proof-stat"><strong>#1</strong><span>Client’s retail fit-out page, Bengaluru — Google India, {e(RESULTS_DATE)}</span></div>
  <div class="proof-stat"><strong>5 terms</strong><span>On page 1 within about three months of a brand-only baseline</span></div>
  <div class="proof-stat"><strong>AI Overview</strong><span>Client cited for “MEP contractors in India” — {e(AI_CITATION_DATE)}</span></div>
</div>'''


def timeline_html(items: list[tuple[str, str, str]]) -> str:
    entries = "".join(
        f'<li><span class="timeline__date">{e(date)}</span><h3>{e(title)}</h3><p>{e(text)}</p></li>'
        for date, title, text in items
    )
    return f'<ol class="timeline">{entries}</ol>'


def case_study_cards() -> str:
    study = CASE_STUDIES[0]
    return card_grid(
        [
            {"tag": "Starting point", "title": "Brand-only visibility", "text": "In August 2026, none of the client’s 15 priority keywords showed in Search Console; Google mostly showed the site for its own name."},
            {"tag": "What we did", "title": "Structure, proof, tracking", "text": "Technical fixes, one page per intent, approved project proof beside claims, consent-based lead tracking and careful releases."},
            {"tag": "Outcome", "title": "Page 1 + AI Overview", "text": f"#1, #3, #4, #5 and #8 for commercial terms ({RESULTS_DATE}) and a national AI Overview citation ({AI_CITATION_DATE}).", "href": f"/case-studies/{study['slug']}/", "link_label": "Read the case study"},
        ],
        3,
    )


def cta_section(
    title: str = "Want a clear, honest view of your search potential?",
    text: str = "Send your website and your goal. You’ll get the three changes I’d make first and a straight answer on whether SEO is the right channel for you now.",
) -> str:
    return f'''<section class="section cta-section">
  <div class="container cta-panel">
    <div>
      <p class="eyebrow">Next step</p>
      <h2>{e(title)}</h2>
      <p>{e(text)}</p>
    </div>
    <div class="cta-actions">
      <a class="btn btn--primary" href="/free-seo-review/">Get a free SEO review <span aria-hidden="true">→</span></a>
      <a class="btn btn--secondary" href="{CASE_STUDY_URL}">See the case study</a>
    </div>
  </div>
</section>'''


def page_hero(
    *,
    path: str,
    eyebrow: str,
    title: str,
    lede: str,
    meta: list[str] | None = None,
    aside: str = "",
    tag_html: str = "",
) -> str:
    meta_html = ""
    if meta:
        meta_html = '<div class="page-hero__meta">' + "".join(
            f'<span>{e(item)}</span>' for item in meta
        ) + "</div>"
    grid_class = " page-hero__grid--aside" if aside else ""
    aside_html = f'<aside class="hero-aside">{aside}</aside>' if aside else ""
    return f'''<section class="page-hero">
  <div class="container">
    {render_breadcrumbs(path)}
    <div class="page-hero__grid{grid_class}">
      <div>
        <p class="eyebrow">{e(eyebrow)}</p>
        {tag_html}
        <h1>{e(title)}</h1>
        <p class="page-hero__lede">{e(lede)}</p>
        {meta_html}
      </div>
      {aside_html}
    </div>
  </div>
</section>'''


def service_cards(items: list[dict], columns: int = 3) -> str:
    return card_grid(
        [
            {
                "tag": "Service",
                "title": item["name"],
                "text": item["short"],
                "href": f'/services/{item["slug"]}/',
                "link_label": "View service",
            }
            for item in items
        ],
        columns,
    )


def location_cards(items: list[dict], columns: int = 3) -> str:
    return card_grid(
        [
            {
                "status": item["status_key"],
                "tag": item["status"],
                "title": item["name"],
                "text": item["short"],
                "href": f'/locations/{item["slug"]}/',
                "link_label": f'SEO in {item["name"]}',
            }
            for item in items
        ],
        columns,
    )


BUDGET_OPTIONS = [
    "Not sure yet",
    "Under ₹15,000 per month",
    "₹15,000 – ₹40,000 per month",
    "₹40,000 – ₹1,00,000 per month",
    "Above ₹1,00,000 per month",
    "One-off project or audit",
]


def enquiry_form(*, offer: str, form_location: str, message_required: bool, website_required: bool, submit_label: str) -> str:
    service_options = "".join(
        f'<option value="{e(item["name"])}">{e(item["name"])}</option>' for item in SERVICES
    )
    budget_options = "".join(f'<option value="{e(value)}">{e(value)}</option>' for value in BUDGET_OPTIONS)
    star = ' <span aria-hidden="true">*</span>'
    message_label = "What would you like to improve?" + ("" if message_required else " (optional)")
    return f'''<form class="contact-form" id="enquiry-form" data-enquiry-form data-contact-email="{e(CONTACT_EMAIL)}" action="{e(ENQUIRY_ENDPOINT)}" method="post">
  <input type="hidden" name="offer" value="{e(offer)}">
  <input type="hidden" name="form_location" value="{e(form_location)}">
  <input type="hidden" name="started_at" value="" data-started-at>
  <div class="form-trap" aria-hidden="true">
    <label for="company_url">Leave this field empty</label>
    <input id="company_url" name="company_url" type="text" tabindex="-1" autocomplete="off">
  </div>
  <div class="form-grid">
    <div class="field">
      <label for="name">Name{star}</label>
      <input id="name" name="name" type="text" autocomplete="name" maxlength="100" required>
    </div>
    <div class="field">
      <label for="email">Business email{star}</label>
      <input id="email" name="email" type="email" autocomplete="email" maxlength="200" required>
    </div>
    <div class="field">
      <label for="website">Website{star if website_required else ""}</label>
      <input id="website" name="website" type="url" placeholder="https://" autocomplete="url" maxlength="300"{" required" if website_required else ""}>
    </div>
    <div class="field">
      <label for="service">What do you need?</label>
      <select id="service" name="service">
        <option value="Not sure yet">Not sure yet</option>
        {service_options}
        <option value="Something else">Something else</option>
      </select>
    </div>
    <div class="field field--full">
      <label for="budget">Monthly marketing budget</label>
      <select id="budget" name="budget">
        {budget_options}
      </select>
    </div>
    <div class="field field--full">
      <label for="message">{e(message_label)}{star if message_required else ""}</label>
      <textarea id="message" name="message" rows="5" maxlength="4000"{" required" if message_required else ""} placeholder="Your main goal, the cities or customers you want, and anything already tried."></textarea>
    </div>
  </div>
  <label class="checkbox-field">
    <input type="checkbox" name="consent" value="yes" required>
    <span>I agree that {e(SITE_NAME)} may use these details to reply to my enquiry. See the <a href="/privacy/">privacy policy</a>.</span>
  </label>
  <div class="form-actions">
    <button class="btn btn--primary" type="submit">{e(submit_label)} <span aria-hidden="true">→</span></button>
    <p class="form-note">I read every enquiry myself and usually reply within one business day.</p>
  </div>
  <p class="form-status" data-form-status role="status" aria-live="polite"></p>
</form>
<noscript><p class="form-note">If the form does not send, email <a href="mailto:{e(CONTACT_EMAIL)}">{e(CONTACT_EMAIL)}</a> with your website and goal.</p></noscript>'''


def home_page() -> None:
    service_slugs = ["seo-consulting", "technical-seo", "local-seo", "ai-search-optimization", "content-strategy", "website-design"]
    industry_cards_data = [
        {
            "tag": "Proven" if item.get("proof") else "Industry",
            "title": item["name"],
            "text": item["short"],
            "href": f'/industries/{item["slug"]}/',
            "link_label": "View approach",
        }
        for item in INDUSTRIES
    ]
    resource_cards_data = [
        {
            "tag": item["category"],
            "title": item["name"],
            "text": item["short"],
            "href": f'/resources/{item["slug"]}/',
            "link_label": "Read guide",
        }
        for item in (RESOURCE_BY_SLUG["location-pages-without-doorway-risk"], RESOURCE_BY_SLUG["seo-cost-india"], RESOURCE_BY_SLUG["choose-seo-consultant-india"])
    ]
    approach_steps = [
        ("Baseline", "Record where you stand today — Search Console, rankings, AI answers and enquiries — before changing anything."),
        ("Fix the foundation", "Crawl, indexation, structure and tracking first, because everything else depends on them."),
        ("Build distinct pages", "One page per intent, proof beside every claim, and no page that would still be true with another city’s name."),
        ("Release and measure", "Ship through checked releases, then report what moved, what didn’t, and what comes next — with dates."),
    ]
    why_items = [
        "You work directly with the person doing the work",
        "Dated, verifiable results — including what hasn’t moved yet",
        "Strategy and hands-on technical delivery in one place",
        "Consent-based tracking that counts real enquiries",
        "Careful releases with checks and a rollback point",
        "No ranking guarantees, no invented case studies",
    ]
    homepage_faqs = [
        ("What does an SEO consultant do?", "An SEO consultant finds what is stopping a website from being found and trusted, sets priorities, and helps ship the fixes — technical, content and local — then measures the effect on enquiries. You deal with one accountable specialist rather than an account manager."),
        ("Do you work with businesses outside Chennai?", "Yes. I’m based in Chennai and work remotely with businesses across India. I have pages for Bengaluru, Delhi NCR, Hyderabad, Chennai, Kerala and Tamil Nadu — plus eight Kerala cities and Coimbatore, Madurai and Salem — each with an honest status."),
        ("Do you guarantee rankings?", "No. Nobody controls Google’s rankings. What I show instead is dated client results — including the terms that haven’t reached page 1 yet — and the method behind them."),
        ("How long does SEO take for a business like mine?", "Brand searches and niche long-tail terms can move within weeks to a few months; competitive city terms usually take six months or more. The case study shows one client reaching page 1 for five terms in about three months, but every market is different."),
        ("What is AI search optimisation, and do I need it?", "It is making sure Google’s AI Overviews and assistants like ChatGPT can identify your business and cite it. Google says it is still SEO; the extra emphasis is entity clarity and third-party mentions. If your buyers ask AI tools for shortlists, it matters."),
    ]
    results_rows = "".join(
        f'<div><span>{e(row["term"])} · {e(row["city"])}</span><b>#{row["position"]}</b><i class="bar {"bar--high" if row["position"] <= 1 else "bar--mid" if row["position"] <= 4 else "bar--low"}" aria-hidden="true"></i></div>'
        for row in CLIENT_RANKINGS
    )
    main = f'''<section class="hero">
  <div class="hero__glow" aria-hidden="true"></div>
  <div class="container hero-grid">
    <div class="hero-copy">
      <p class="eyebrow eyebrow--pill">Senior SEO consultant · Chennai · Across India</p>
      <h1>SEO expert in India</h1>
      <p class="hero-tagline">For businesses that need enquiries, not just traffic.</p>
      <p class="hero-lede">I’m {e(OWNER_NAME)} — originally from Thrissur, Kerala, based in Chennai. I combine SEO strategy with hands-on technical work, and I show dated results instead of ranking promises.</p>
      <div class="hero-actions">
        <a class="btn btn--primary" href="/free-seo-review/">Get a free SEO review <span aria-hidden="true">→</span></a>
        <a class="btn btn--secondary" href="{CASE_STUDY_URL}">See the case study</a>
      </div>
      <ul class="hero-proof">
        <li><strong>#1 on Google</strong><span>Client page, retail fit-out, Bengaluru</span></li>
        <li><strong>5 page-1 terms</strong><span>In about three months</span></li>
        <li><strong>AI Overview</strong><span>Client cited nationally</span></li>
      </ul>
    </div>
    <div class="hero-visual" aria-label="Snapshot of client ranking results, {e(RESULTS_DATE)}">
      <div class="visual-card">
        <div class="visual-card__top">
          <span class="status-dot" aria-hidden="true"></span>
          <div><strong>Client results</strong><span>MEP contractor · Google India</span></div>
          <span class="visual-badge">Dated</span>
        </div>
        <div class="visual-score">
          <div><span>Page 1</span><strong>5 commercial terms</strong></div>
          <div class="score-ring" aria-hidden="true"><span>#1</span></div>
        </div>
        <div class="visual-rows">{results_rows}</div>
        <div class="visual-footer"><span>Recorded {e(RESULTS_DATE)}</span><span aria-hidden="true">↗</span></div>
      </div>
      <div class="floating-note"><span aria-hidden="true">✦</span><p><strong>Honest reporting.</strong><br>Every result has a date and a method.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container prose-layout">
    <div class="prose">
      <p class="lead">Most websites don’t have a keyword problem. They have pages that can’t prove what they claim, structures that confuse Google, and enquiries nobody can trace back to a search.</p>
      <h2>SEO that connects search visibility with real enquiries</h2>
      <p>I start with a baseline, fix the foundation, then build pages that each have one clear job — with proof next to every claim. Changes ship through checked releases, so the site keeps working while it improves.</p>
      <p>You work with me directly, from the first review to the monthly report. When something works, you’ll see the date and the evidence. When something hasn’t moved yet, you’ll see that too.</p>
    </div>
    <aside class="aside-panel">
      <p class="eyebrow">What you can expect</p>
      <h3>Qualified enquiries, not vanity traffic</h3>
      {check_list([
        "A written baseline before any change",
        "One page per search intent",
        "Proof beside every claim",
        "Consent-based enquiry tracking",
        "Monthly, plain-language reporting",
      ])}
      <a class="btn btn--secondary btn--full" href="/free-seo-review/">Request a free review <span aria-hidden="true">→</span></a>
    </aside>
  </div>
</section>

<section class="section section--surface">
  <div class="container">
    {section_header("Recent work", "An MEP contractor, page 1 in about three months", "One detailed case study, with dates, the method and the misses.", ("Read the case study", CASE_STUDY_URL))}
    {case_study_cards()}
  </div>
</section>

<section class="section">
  <div class="container">
    {section_header("Services", "Choose the right entry point", "Start with one focused service, or combine strategy, technical work, local search and AI search into one programme.", ("All services", "/services/"))}
    {service_cards([SERVICE_BY_SLUG[slug] for slug in service_slugs], 3)}
  </div>
</section>

<section class="section section--surface">
  <div class="container">
    {section_header("Where I work", "Six markets, each with an honest status", "Client results, work in progress, home ground or same-state hub — every location page says which. I work remotely with businesses anywhere in India.", ("All locations", "/locations/"))}
    {location_cards(LOCATIONS, 3)}
    <p class="section-intro">SEO expert in Kerala, city by city: {" · ".join(f'<a href="/locations/kerala/{city["slug"]}/">{e(city_label(city))}</a>' for city in KERALA_CITIES)}</p>
    <p class="section-intro">SEO company intent in Tamil Nadu, city by city: {" · ".join(f'<a href="/locations/tamil-nadu/{city["slug"]}/">{e(city_label(city))}</a>' for city in STATE_CITIES["tamil-nadu"])}</p>
  </div>
</section>

<section class="section">
  <div class="container">
    {section_header("Industries", "Strategy shaped by how customers buy", "The method is consistent; the page structure follows how your buyers research and decide.", ("All industries", "/industries/"))}
    {card_grid(industry_cards_data, 3)}
  </div>
</section>

<section class="section section--surface">
  <div class="container split-section">
    <div>
      {section_header("How I work", "Baseline, foundation, distinct pages, measured releases")}
      {numbered_steps(approach_steps)}
    </div>
    <aside class="aside-panel">
      <p class="eyebrow">Why work with me</p>
      <h3>Built around evidence</h3>
      {check_list(why_items)}
      <a class="btn btn--secondary btn--full" href="/about/">About {e(OWNER_NAME)} <span aria-hidden="true">→</span></a>
    </aside>
  </div>
</section>

<section class="section">
  <div class="container">
    {section_header("Questions", "Useful answers before you get in touch")}
    {faq_html(homepage_faqs)}
  </div>
</section>

<section class="section section--surface">
  <div class="container">
    {section_header("Resources", "Guides written from real work", "Practical explanations for Indian businesses evaluating SEO, city pages, pricing and consultants.", ("All resources", "/resources/"))}
    {card_grid(resource_cards_data, 3)}
  </div>
</section>

{cta_section()}
'''
    write_page(
        path="/",
        title="SEO Expert in India | Sreejith Digital",
        description=DEFAULT_DESCRIPTION,
        main=main,
        body_class="page-home",
        schema_extra=[faq_schema(homepage_faqs)],
    )


def about_page() -> None:
    principles = [
        {"title": "Baseline before change", "text": "Every engagement starts with a written record of where things stand, so results can be measured honestly."},
        {"title": "Evidence over folklore", "text": "Use data and observed behaviour, and say clearly when the evidence is incomplete."},
        {"title": "Architecture first", "text": "A clean structure makes content, city pages, internal links and reporting easier to scale."},
        {"title": "Report the misses", "text": "Show what hasn’t moved alongside what has. A results page that only shows wins means nothing."},
    ]
    models = [
        {"tag": "01", "title": "Audit & roadmap", "text": "A focused review that ends with a prioritised, implementation-ready plan."},
        {"tag": "02", "title": "Consulting retainer", "text": "Ongoing strategy, implementation review, releases and monthly reporting."},
        {"tag": "03", "title": "Build project", "text": "A defined build — site structure, city pages, schema or tracking — with clear acceptance checks."},
    ]
    experience_items = "".join(
        f'''<li><span class="timeline__date">{e(item["period"])}</span><h3>{e(item["org"])}</h3><p><strong>{e(item["role"])}.</strong> {e(item["summary"])}{f' <a href="{e(item["href"])}">Read the case study</a>.' if item.get("href") else ""}</p></li>'''
        for item in EXPERIENCE
    )
    profiles_html = ""
    if OWNER_PROFILES:
        profiles_html = '<p class="profile-links">Also on: ' + " · ".join(
            f'<a href="{e(url)}" rel="me">{e(url.split("//")[-1].split("/")[0])}</a>' for url in OWNER_PROFILES
        ) + "</p>"
    glance = [
        f"From {OWNER_ORIGIN}, based in {OWNER_BASE_CITY}",
        "Works remotely with businesses across India",
        "Strategy and hands-on technical delivery",
        "No ranking guarantees",
    ]
    if OWNER_LANGUAGES:
        glance.insert(2, "Works in " + ", ".join(OWNER_LANGUAGES))
    main = f'''{page_hero(
        path="/about/",
        eyebrow="About",
        title=f"{OWNER_NAME}, SEO consultant",
        lede=f"I run {SITE_NAME}: SEO strategy plus the technical work that makes it stick — site structure, structured data, enquiry tracking and careful releases. From {OWNER_ORIGIN}, based in {OWNER_BASE_CITY}, working with businesses across India.",
        meta=[f"From {OWNER_ORIGIN} · based in {OWNER_BASE_CITY}", "Senior-led practice", "Strategy + delivery"],
    )}

<section class="section">
  <div class="container prose-layout">
    <div class="prose">
      <p class="lead">Most SEO problems I see aren’t a missing keyword. They are sites that can’t prove what they say, page structures that compete with themselves, and enquiries nobody can trace back to a search.</p>
      <h2>One person, end to end</h2>
      <p>You work with the person doing the work. I plan the strategy, write the page briefs, implement the technical changes and report the results myself, so nothing gets lost between an account manager and a junior team.</p>
      <h2>Release discipline, borrowed from engineering</h2>
      <p>Every change I ship to a client site goes through a reviewed pull request, automated checks, a staging preview and a rollback point. It is unusual in SEO, and it is why client sites keep working while they improve quickly.</p>
      <h2>Honest about results</h2>
      <p>I show dated results with the method behind them, including the terms that haven’t reached page 1 yet. If a channel other than SEO would serve you better right now, I’ll say so.</p>
      {profiles_html}
    </div>
    <aside class="aside-panel">
      <p class="eyebrow">At a glance</p>
      <h3>{e(OWNER_NAME)}</h3>
      {check_list(glance)}
      <a class="btn btn--secondary btn--full" href="{CASE_STUDY_URL}">See recent work <span aria-hidden="true">→</span></a>
    </aside>
  </div>
</section>

<section class="section section--surface">
  <div class="container">
    {section_header("Work history", "Where I’ve worked and what I did", "Confirmed engagements only. Detailed results are on the case-study pages.")}
    <ol class="timeline">{experience_items}</ol>
  </div>
</section>

<section class="section">
  <div class="container">
    {section_header("Principles", "How the work is approached", "A few rules keep the engagement useful and the reporting credible.")}
    {card_grid(principles, 4)}
  </div>
</section>

<section class="section section--surface">
  <div class="container">
    {section_header("Engagement models", "A scope that fits your team", "The shape of the work follows your goals and your team’s capacity, not a fixed package.")}
    {card_grid(models, 3)}
  </div>
</section>

{cta_section("Have a project in mind?", "Share the current site, the goal and the constraint. I’ll come back with the most useful next step — even if it isn’t working with me.")}
'''
    write_page(
        path="/about/",
        title=f"About {OWNER_NAME} — SEO Consultant, Chennai",
        description=f"{OWNER_NAME} runs {SITE_NAME}, an SEO practice based in Chennai: strategy, technical SEO and careful releases for businesses across India.",
        main=main,
        page_type="ProfilePage",
        about_id=PERSON_ID,
    )


def services_hub() -> None:
    main = f'''{page_hero(
        path="/services/",
        eyebrow="Services",
        title="SEO services that connect strategy and delivery",
        lede="Use one focused service, or combine consulting, technical SEO, local search, AI search, content and measurement into a single programme.",
        meta=[f"{len(SERVICES)} focused services", "Strategy + implementation", "No fixed packages"],
    )}

<section class="section">
  <div class="container">
    {section_header("Explore services", "Choose the work you need now", "Each page explains what is covered, who it suits, deliverables, process and common questions.")}
    {service_cards(SERVICES, 3)}
  </div>
</section>

<section class="section section--surface">
  <div class="container split-section">
    <div>
      {section_header("How services connect", "Avoid isolated fixes", "A technical issue, a content gap and a weak enquiry path often share one root cause. The services are designed to combine without competing priorities.")}
      {numbered_steps([
        ("Establish the foundation", "Technical SEO and analytics define what can be trusted and measured."),
        ("Clarify demand", "Content strategy and keyword-to-URL mapping give each page a distinct job."),
        ("Capture intent", "Local SEO, AI search and Google Ads connect the offer to the moment of action."),
        ("Keep it accountable", "Consulting and reporting turn activity into a maintained roadmap."),
      ])}
    </div>
    <aside class="aside-panel">
      <p class="eyebrow">Not sure where to start?</p>
      <h3>Start with a free review</h3>
      <p>A short written review is usually enough to tell whether you need an audit, a strategy, hands-on delivery or something else entirely.</p>
      <a class="btn btn--primary" href="/free-seo-review/">Get a free SEO review <span aria-hidden="true">→</span></a>
    </aside>
  </div>
</section>

{cta_section()}
'''
    write_page(
        path="/services/",
        title="SEO Services: Consulting, Technical, Local & AI Search",
        description="SEO services from a senior consultant: consulting, technical, local and AI search, content strategy, reporting, Google Ads and website builds.",
        main=main,
        page_type="CollectionPage",
    )


def service_page(service: dict) -> None:
    path = f'/services/{service["slug"]}/'
    related = [item for item in SERVICES if item["slug"] != service["slug"]][:3]
    included_cards = [
        {"tag": f"{index:02d}", "title": title, "text": text}
        for index, (title, text) in enumerate(service["included"], start=1)
    ]
    related_cards = [
        {
            "tag": "Related service",
            "title": item["name"],
            "text": item["short"],
            "href": f'/services/{item["slug"]}/',
            "link_label": "View service",
        }
        for item in related
    ]
    service_schema = {
        "@type": "Service",
        "@id": BASE_URL + path + "#service",
        "name": service["name"],
        "serviceType": service["name"],
        "description": service["description"],
        "provider": {"@id": BUSINESS_ID},
        "areaServed": {"@type": "Country", "name": "India"},
        "url": BASE_URL + path,
    }
    proof_html = ""
    if service["slug"] in SERVICE_PROOF:
        proof_html = f'''<section class="section">
  <div class="container split-section">
    <div>
      {section_header("Evidence", "This service in real work", SERVICE_PROOF[service["slug"]], ("Read the case study", CASE_STUDY_URL))}
    </div>
    <aside class="aside-panel">
      <p class="eyebrow">Client results · {e(RESULTS_DATE)}</p>
      <h3>MEP contractor, Google India</h3>
      {check_list([f'#{row["position"]} — {row["term"]}, {row["city"]}' for row in CLIENT_RANKINGS[:3]])}
      <a class="btn btn--secondary btn--full" href="{CASE_STUDY_URL}">See the method <span aria-hidden="true">→</span></a>
    </aside>
  </div>
</section>'''
    aside = f'''<p class="eyebrow">Best for</p>
<p>{e(service["audience"])}</p>
<a class="btn btn--primary btn--full" href="/free-seo-review/">Get a free SEO review <span aria-hidden="true">→</span></a>'''
    main = f'''{page_hero(
        path=path,
        eyebrow="Service",
        title=service["name"],
        lede=service["intro"],
        meta=["Focused scope", "Practical deliverables", "Clear handover"],
        aside=aside,
    )}

<section class="section section--tight">
  <div class="container">
    {answer_block(SERVICE_ANSWERS[service["slug"]])}
  </div>
</section>

<section class="section">
  <div class="container">
    {section_header("What is covered", "Practical work, clearly scoped", service["description"])}
    {card_grid(included_cards, 3)}
  </div>
</section>

{proof_html}

<section class="section section--surface">
  <div class="container split-section split-section--reverse">
    <aside class="aside-panel">
      <p class="eyebrow">Deliverables</p>
      <h3>What you keep</h3>
      {check_list(service["deliverables"])}
    </aside>
    <div>
      {section_header("Process", "A straightforward sequence", "The exact scope is agreed before work begins, but the shape stays consistent.")}
      {numbered_steps(service["process"])}
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    {section_header("Common questions", "Useful detail before you get in touch")}
    {faq_html(service["faq"])}
  </div>
</section>

<section class="section section--surface">
  <div class="container">
    {section_header("Related services", "Work that often connects", "Combine only what supports the current goal.", ("All services", "/services/"))}
    {card_grid(related_cards, 3)}
  </div>
</section>

{cta_section("Want this scoped for your site?", "Send your website and goal. The free review will tell you whether this service is the right place to start.")}
'''
    write_page(
        path=path,
        title=SERVICE_SEO_TITLES[service["slug"]],
        description=service["description"],
        main=main,
        schema_extra=[service_schema, faq_schema(service["faq"])],
    )


def industries_hub() -> None:
    cards = [
        {
            "tag": "Proven" if item.get("proof") else "Industry",
            "title": item["name"],
            "text": item["short"],
            "href": f'/industries/{item["slug"]}/',
            "link_label": "View approach",
        }
        for item in INDUSTRIES
    ]
    main = f'''{page_hero(
        path="/industries/",
        eyebrow="Industries",
        title="SEO shaped by how your customers buy",
        lede="Different business models create different search problems. These pages explain the common constraints and how the work is structured around them.",
        meta=["Contractors", "B2B & SaaS", "Professional services", "Ecommerce", "Multi-location"],
    )}

<section class="section">
  <div class="container">
    {section_header("Explore industries", "A starting point, not a template", "“Proven” marks the sector with a published case study. The others share the same method.")}
    {card_grid(cards, 3)}
  </div>
</section>

<section class="section section--surface">
  <div class="container">
    {section_header("Shared foundation", "What every industry engagement starts with")}
    {check_list([
      "A clear commercial outcome and a realistic time horizon",
      "One primary URL for each priority search intent",
      "Technical foundations that support the content",
      "Enquiry tracking the whole team can trust",
      "A page structure that can grow without overlap",
    ])}
  </div>
</section>

{cta_section("Need an industry-specific view?", "Tell me the business model and the current bottleneck. I’ll suggest the most useful starting point.")}
'''
    write_page(
        path="/industries/",
        title="SEO by Industry: Contractors, B2B, Ecommerce & Services",
        description="SEO approaches for construction and MEP contractors, B2B and SaaS, professional services, ecommerce and multi-location businesses in India.",
        main=main,
        page_type="CollectionPage",
    )


def industry_page(industry: dict) -> None:
    path = f'/industries/{industry["slug"]}/'
    approach_cards = [
        {"tag": f"{index:02d}", "title": title, "text": text}
        for index, (title, text) in enumerate(industry["approach"], start=1)
    ]
    service_links = [
        {
            "tag": "Useful service",
            "title": SERVICE_BY_SLUG[slug]["name"],
            "text": SERVICE_BY_SLUG[slug]["short"],
            "href": f"/services/{slug}/",
            "link_label": "View service",
        }
        for slug in industry["services"]
    ]
    proof_html = ""
    if industry.get("proof"):
        proof_html = f'''<section class="section section--surface">
  <div class="container">
    {section_header("Evidence", "This approach in real work", "A multi-city MEP contractor, from brand-only visibility to page 1 — with dates and the misses.", ("Read the case study", CASE_STUDY_URL))}
    {case_study_cards()}
  </div>
</section>'''
    main = f'''{page_hero(
        path=path,
        eyebrow="Industry",
        title=INDUSTRY_H1[industry["slug"]],
        lede=industry["intro"],
        meta=["Context-led strategy", "No generic template"] + (["Published case study"] if industry.get("proof") else []),
    )}

<section class="section">
  <div class="container split-section">
    <div>
      {section_header("Common constraints", "What usually gets in the way", industry["description"])}
      <div class="prose"><p class="lead">{e(industry["intro"])}</p></div>
    </div>
    <aside class="aside-panel">
      <p class="eyebrow">Watch for</p>
      <h3>Common search friction</h3>
      {check_list(industry["challenges"])}
    </aside>
  </div>
</section>

{proof_html}

<section class="section">
  <div class="container">
    {section_header("Approach", "How the work is structured", "A practical sequence that keeps pages, content and measurement aligned.")}
    {card_grid(approach_cards, 3)}
  </div>
</section>

<section class="section section--surface">
  <div class="container">
    {section_header("Useful starting points", "Services that often fit", "Common combinations, not fixed bundles.", ("All services", "/services/"))}
    {card_grid(service_links, 3)}
  </div>
</section>

{cta_section()}
'''
    write_page(
        path=path,
        title=INDUSTRY_SEO_TITLES[industry["slug"]],
        description=industry["description"],
        main=main,
    )


def locations_item_list() -> dict:
    """Every location page, in hierarchy order, for search engines and AI systems."""
    entries = [(f'SEO expert in {item["name"]}', f'/locations/{item["slug"]}/') for item in LOCATIONS]
    entries += [
        (f"SEO expert in {city_label(city)}", f'/locations/{state_slug}/{city["slug"]}/')
        for state_slug, cities in STATE_CITIES.items()
        for city in cities
    ]
    return {
        "@type": "ItemList",
        "@id": BASE_URL + "/locations/#list",
        "name": "Location pages",
        "itemListElement": [
            {"@type": "ListItem", "position": index, "name": name, "url": BASE_URL + href}
            for index, (name, href) in enumerate(entries, start=1)
        ],
    }


def locations_hub() -> None:
    main = f'''{page_hero(
        path="/locations/",
        eyebrow="Locations",
        title="Where I work — and what I’ve done there",
        lede="India first, then states and cities: six markets with an honest status each, eight Kerala cities and three Tamil Nadu cities with their own pages. A city gets a page only when people search for it and there is something true and useful to say.",
        meta=["Based in Chennai", "Remote across India", "No invented local offices"],
    )}

<section class="section">
  <div class="container">
    {section_header("Markets", "City pages with real substance", "Each page carries local context, the work actually done there and a reason to get in touch.", ("Local SEO service", "/services/local-seo/"))}
    {location_cards(LOCATIONS, 3)}
  </div>
</section>

<section class="section">
  <div class="container">
    {section_header("Kerala", "Kerala, city by city", "Pages for the eight Kerala cities where Google’s autocomplete shows steady demand for an SEO expert.", ("Kerala overview", "/locations/kerala/"))}
    {state_city_cards("kerala", KERALA_CITIES, 4)}
  </div>
</section>

<section class="section section--surface">
  <div class="container">
    {section_header("Tamil Nadu", "Tamil Nadu, city by city", "Three city pages where “SEO company” intent is common, each with its own sectors, localities, FAQs and dated page-1 observations.", ("Tamil Nadu overview", "/locations/tamil-nadu/"))}
    {state_city_cards("tamil-nadu", STATE_CITIES["tamil-nadu"], 3)}
  </div>
</section>

<section class="section">
  <div class="container prose-layout">
    <div class="prose">
      <p class="lead">I work remotely with businesses anywhere in India. These pages exist because each one has real work or real local knowledge behind it.</p>
      <h2>The rule behind these pages</h2>
      <p>Before a city page is published, I swap the city name for another city and read it again. If it is still true, it isn’t a city page — it is a doorway page wearing a city name, and it doesn’t go live. The same rule applies to client sites.</p>
      <h2>Honest status, always</h2>
      <p>Bengaluru and Delhi NCR show client results with dates. Hyderabad shows work in progress. Chennai and Kerala are home ground; the Kerala city pages and the new Tamil Nadu city pages say plainly that no local client result is published yet. When the status changes, the page changes.</p>
      <p><a href="/resources/location-pages-without-doorway-risk/">Read the full city-page guide →</a></p>
    </div>
    <aside class="aside-panel">
      <p class="eyebrow">Architecture rule</p>
      <h3>One page, one job</h3>
      {check_list([
        "A hub for navigation",
        "A page only for a genuine market",
        "Service pages for the offer",
        "Industry pages for context",
        "Case studies for proof",
      ])}
    </aside>
  </div>
</section>

{cta_section("Planning city pages for your own business?", "A short review can prevent months of duplicated pages and overlapping keywords.")}
'''
    write_page(
        path="/locations/",
        title="Where I Work: SEO Consulting by City | Sreejith Digital",
        description="SEO pages for India by state and city: Chennai, Bengaluru, Delhi NCR, Hyderabad, Kerala, Tamil Nadu and eleven city guides with an honest status.",
        main=main,
        page_type="CollectionPage",
        schema_extra=[locations_item_list()],
    )


def location_page(location: dict) -> None:
    path = f'/locations/{location["slug"]}/'
    results = [row for row in CLIENT_RANKINGS if location.get("results_city") and row["city"] == location["results_city"]]
    service_schema = {
        "@type": "Service",
        "@id": BASE_URL + path + "#service",
        "name": f'SEO consulting for {location["name"]}',
        "serviceType": "SEO consulting",
        "description": location["description"],
        "provider": {"@id": BUSINESS_ID},
        "areaServed": LOCATION_PLACES[location["slug"]],
        "url": BASE_URL + path,
    }
    if results:
        status_panel = f'''<p class="eyebrow">Client results · {e(RESULTS_DATE)}</p>
<h3>Google India positions</h3>
{check_list([f'#{row["position"]} — {row["term"]}' for row in results])}
<a class="btn btn--secondary btn--full" href="{CASE_STUDY_URL}">See how <span aria-hidden="true">→</span></a>'''
    else:
        status_panel = f'''<p class="eyebrow">Status</p>
<h3>{e(LOCATION_STATUS_NOTE[location["status_key"]])}</h3>
{check_list(location["engage"])}
<a class="btn btn--secondary btn--full" href="{CASE_STUDY_URL}">See the method in action <span aria-hidden="true">→</span></a>'''
    cities_html = ""
    if location["slug"] == "kerala":
        cities_html = f'''<section class="section section--surface">
  <div class="container">
    {section_header("Across the state", "SEO expert in each Kerala city", "Eight city pages, each with that city’s industries, how its customers search and what page 1 looked like on " + SERP_DATE + ".")}
    {state_city_cards("kerala", KERALA_CITIES, 4)}
  </div>
</section>'''
    elif location["slug"] == "tamil-nadu":
        cities_html = f'''<section class="section section--surface">
  <div class="container">
    {section_header("Across the state", "SEO company in each Tamil Nadu city", "Three city pages, each with that city’s sectors, search behaviour, localities, FAQs and dated page-1 observations.")}
    {state_city_cards("tamil-nadu", STATE_CITIES["tamil-nadu"], 3)}
    <div class="prose"><p><a class="text-link" href="/locations/chennai/">Read the Chennai home-base page <span aria-hidden="true">→</span></a></p></div>
  </div>
</section>'''
    results_html = ""
    if results:
        results_html = rankings_table(results, f"Client pages, Google India, recorded {RESULTS_DATE}.")
    work_first = f"<p>{e(location['work'][0])}</p>"
    work_rest = "".join(f"<p>{e(paragraph)}</p>" for paragraph in location["work"][1:])
    context_paragraphs = "".join(f"<p>{e(paragraph)}</p>" for paragraph in location["context"])
    other_locations = [item for item in LOCATIONS if item["slug"] != location["slug"]]
    related_cards = [
        {"tag": "Service", "title": SERVICE_BY_SLUG[slug]["name"], "text": SERVICE_BY_SLUG[slug]["short"], "href": f"/services/{slug}/", "link_label": "View service"}
        for slug in location["services"]
    ] + [
        {"tag": "Industry", "title": INDUSTRY_BY_SLUG[slug]["name"], "text": INDUSTRY_BY_SLUG[slug]["short"], "href": f"/industries/{slug}/", "link_label": "View approach"}
        for slug in location["industries"][:1]
    ]
    main = f'''{page_hero(
        path=path,
        eyebrow=f'Location · {location["name"]}',
        title=location["h1"],
        lede=location["lede"],
        meta=[location["status"], location["delivery"], "Dated, honest reporting"],
        tag_html=status_tag(location["status_key"], location["status"]),
    )}

<section class="section">
  <div class="container split-section">
    <div class="prose">
      <h2>{e(location["context_heading"])}</h2>
      {context_paragraphs}
    </div>
    <aside class="aside-panel">
      {status_panel}
    </aside>
  </div>
</section>

{cities_html}

<section class="section{' section--surface' if location['slug'] not in {'kerala', 'tamil-nadu'} else ''}">
  <div class="container split-section split-section--reverse">
    <aside class="aside-panel">
      <p class="eyebrow">{e(location["engage_heading"])}</p>
      <h3>How it works</h3>
      {check_list(location["engage"])}
      <a class="btn btn--primary btn--full" href="/free-seo-review/">Get a free SEO review <span aria-hidden="true">→</span></a>
    </aside>
    <div class="prose">
      <h2>{e(location["work_heading"])}</h2>
      {work_first}
      {results_html}
      {work_rest}
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    {section_header("Questions", f'SEO in {location["name"]}: common questions')}
    {faq_html(location["faqs"])}
  </div>
</section>

<section class="section section--surface">
  <div class="container">
    {section_header("Relevant services", "Connect the market to the offer", "The services and approach that fit businesses here most often.", ("All services", "/services/"))}
    {card_grid(related_cards, 4)}
  </div>
</section>

<section class="section">
  <div class="container">
    {section_header("Other markets", "Where else I work", "Each market page has its own context and status.", ("All locations", "/locations/"))}
    {location_cards(other_locations, 4)}
  </div>
</section>

{cta_section(f'Growing in {location["name"]}?', "Send your website and the cities you serve. You’ll get the three changes I’d make first.")}
'''
    write_page(
        path=path,
        title=location["title"],
        description=location["description"],
        main=main,
        schema_extra=[service_schema, faq_schema(location["faqs"])],
    )


def state_city_cards(state_slug: str, items: list[dict], columns: int = 4) -> str:
    return card_grid(
        [
            {
                "tag": f'{item["district"]} district',
                "title": city_label(item),
                "text": item["short"],
                "href": f'/locations/{state_slug}/{item["slug"]}/',
                "link_label": f"SEO expert in {city_label(item)}",
            }
            for item in items
        ],
        columns,
    )


def city_answer(city: dict) -> str:
    """Entity-first answer for AI Overviews and assistants (about 55 words)."""
    label = city_label(city)
    return (
        f"{OWNER_NAME} is an SEO consultant from Thrissur, Kerala, based in Chennai, who works with "
        f"{label} businesses remotely, in Malayalam or English. His published work took an MEP contractor to #1 on Google India "
        f"in Bengaluru ({RESULTS_DATE}) and into Google’s AI Overview for “MEP contractors in India” "
        f"({AI_CITATION_DATE}). No {label} client result is published yet."
    )


def state_city_answer(state_slug: str, city: dict) -> str:
    """Entity-first answer; Kerala keeps its original wording."""
    if state_slug == "kerala":
        return city_answer(city)
    return str(city["answer"])


def state_city_page(state_slug: str, city: dict) -> None:
    path = f'/locations/{state_slug}/{city["slug"]}/'
    label = city_label(city)
    state_label = STATE_CITY_STATE_NAMES[state_slug]
    other_names = [name for name in [city["name"], *city.get("alt_names", [])] if name != label]
    aka = f' ({", ".join(other_names)})' if other_names else ""
    service_schema = {
        "@type": "Service",
        "@id": BASE_URL + path + "#service",
        "name": f"SEO services in {label}",
        "serviceType": "Search engine optimization",
        "description": city["description"],
        "provider": {"@id": BUSINESS_ID},
        "areaServed": city_place(city, state_slug),
        "url": BASE_URL + path,
    }
    nearby = [STATE_CITY_BY_SLUG[state_slug][slug] for slug in city["nearby"]]
    district_heading = (
        f'Across {city["district"]} district' if city["district"] != city["name"] else f"Across {label} and nearby towns"
    )
    economy_cards = [{"tag": "Sector", "title": title, "text": text} for title, text in city["economy"]]
    search_paragraphs = "".join(f"<p>{e(paragraph)}</p>" for paragraph in city["search"])
    if state_slug == "kerala":
        serp_heading = f'What page 1 looked like for “SEO expert in {label}”'
        serp_intro = f"Google India, logged out, with Google placing the search in {label}, checked on {SERP_DATE}:"
        gap_html = (
            f'<p>I don’t have a published {e(label)} client result yet, and I won’t invent one. My published work is in other markets: '
            f'an MEP contractor’s pages reached #1, #3, #4, #5 and #8 on Google India for commercial terms ({e(RESULTS_DATE)}), '
            f'and the client was cited in Google’s AI Overview for “MEP contractors in India” ({e(AI_CITATION_DATE)}).</p>'
        )
        working_together_items = [
            "A written baseline before any change",
            "Calls in Malayalam or English; meetings when I’m in Kerala",
            "Reporting that separates local, NRI and visitor enquiries",
        ]
        nearby_heading = "Other Kerala cities"
        nearby_intro = "Each city page has its own market, search patterns and page-1 snapshot."
    else:
        serp_heading = f'What page 1 looked like for “SEO expert / company in {label}”'
        serp_intro = (
            f"Google India, logged out (gl=in, pws=0), with the location detected as {label}, "
            f"{state_label}, checked on {SERP_DATE}:"
        )
        gap_html = (
            f'<p>I don’t have a published {e(label)} client result yet, and I won’t invent one. The published case study is '
            f'from Bengaluru, where an MEP contractor reached page-one commercial positions on Google India '
            f'({e(RESULTS_DATE)}) and was cited in Google’s AI Overview for “MEP contractors in India” '
            f'({e(AI_CITATION_DATE)}). There is no {e(label)} office, and no local result is implied.</p>'
        )
        working_together_items = [
            "A written baseline before any change",
            "Calls in English or Malayalam; no Tamil-language claim",
            "Based in Chennai, same state; meetings when travelling",
            "Reporting that separates city, state and national enquiries",
        ]
        nearby_heading = "Other Tamil Nadu cities"
        nearby_intro = "Each city page has its own market, search patterns and dated page-1 observations."
    main = f'''{page_hero(
        path=path,
        eyebrow=f"{state_label} · {label}{aka}",
        title=city["h1"],
        lede=city["lede"],
        meta=[f'{city["district"]} district', "Remote from Chennai" if state_slug == "kerala" else "Chennai, same state", "Dated, honest reporting"],
        tag_html=status_tag("home", city.get("status_label", "Home state")),
    )}

<section class="section section--tight">
  <div class="container">
    {answer_block(state_city_answer(state_slug, city))}
  </div>
</section>

<section class="section">
  <div class="container">
    {section_header("Local market", city["economy_heading"], f"The search work that pays off depends on how {label} businesses sell — and to whom.")}
    {card_grid(economy_cards, 4)}
  </div>
</section>

<section class="section section--surface">
  <div class="container split-section">
    <div class="prose">
      <h2>How people in {e(label)} search</h2>
      {search_paragraphs}
    </div>
    <aside class="aside-panel">
      <p class="eyebrow">Areas covered</p>
      <h3>{e(district_heading)}</h3>
      {check_list(city["areas"])}
      <p class="table-note">A town gets its own page only when people search for it and there is something specific to say.</p>
    </aside>
  </div>
</section>

<section class="section">
  <div class="container split-section split-section--reverse">
    <aside class="aside-panel">
      <p class="eyebrow">Hiring checklist</p>
      <h3>Ask any SEO expert — including me</h3>
      {check_list(["The URL that ranked", "The date it was recorded", "What didn’t work, and why"])}
      <a class="btn btn--primary btn--full" href="/free-seo-review/">Get a free SEO review <span aria-hidden="true">→</span></a>
    </aside>
    <div class="prose">
      <h2>{e(serp_heading)}</h2>
      <p>{e(serp_intro)}</p>
      {dash_list(city["landscape"])}
      <p>Results change daily, and lists in AI answers are assembled from websites and profiles, not verified results. That is why the checklist beside this asks for evidence rather than adjectives.</p>
    </div>
  </div>
</section>

<section class="section section--surface">
  <div class="container prose-layout">
    <div class="prose">
      <h2>Published results — and the honest gap</h2>
      {gap_html}
      <p><a href="{CASE_STUDY_URL}">Read how it was done, including what hasn’t reached page 1 →</a></p>
    </div>
    <aside class="aside-panel">
      <p class="eyebrow">Working together</p>
      <h3>SEO services in {e(label)}, from Chennai</h3>
      {check_list(working_together_items)}
    </aside>
  </div>
</section>

<section class="section">
  <div class="container">
    {section_header("Questions", f"SEO in {label}: common questions")}
    {faq_html(city["faqs"])}
  </div>
</section>

<section class="section section--surface">
  <div class="container">
    {section_header("Nearby", nearby_heading, nearby_intro, (f"{state_label} overview", f"/locations/{state_slug}/"))}
    {state_city_cards(state_slug, nearby, 3)}
  </div>
</section>

{cta_section(f"Growing in {label}?", "Send your website and the areas you serve. You’ll get the three changes I’d make first.")}
'''
    write_page(
        path=path,
        title=city["title"],
        description=city["description"],
        main=main,
        schema_extra=[service_schema, faq_schema(city["faqs"])],
    )


def resources_hub() -> None:
    cards = [
        {
            "tag": item["category"],
            "title": item["name"],
            "text": item["short"],
            "href": f'/resources/{item["slug"]}/',
            "link_label": "Read guide",
        }
        for item in RESOURCES
    ]
    main = f'''{page_hero(
        path="/resources/",
        eyebrow="Resources",
        title="Practical SEO guides, written from real work",
        lede="Short, useful explanations of the decisions behind technical SEO, city pages, keyword strategy, local search, pricing and measurement.",
        meta=["Guides", "Checklists", "Frameworks"],
    )}

<section class="section">
  <div class="container">
    {section_header("India-focused guides", "Start with a useful question", "For Indian businesses evaluating SEO, local search, measurement and paid-versus-organic decisions.")}
    {card_grid(cards, 3)}
  </div>
</section>

{cta_section("Prefer to have it applied to your site?", "A free review turns the relevant checklist into the three changes that matter most for you.")}
'''
    write_page(
        path="/resources/",
        title="SEO Guides & Checklists for Indian Businesses",
        description="Practical SEO guides for Indian businesses: city pages without doorway risk, technical audits, pricing, choosing a consultant, local search and measurement.",
        main=main,
        page_type="CollectionPage",
    )


def resource_page(resource: dict) -> None:
    path = f'/resources/{resource["slug"]}/'
    sections = []
    toc = []
    for index, section in enumerate(resource["sections"], start=1):
        anchor = f'section-{index}'
        toc.append(f'<li><a href="#{anchor}">{e(section["heading"])}</a></li>')
        paragraphs = "".join(f'<p>{e(paragraph)}</p>' for paragraph in section["paragraphs"])
        bullets = check_list(section["bullets"]) if section["bullets"] else ""
        callout = (
            f'<div class="callout"><strong>Worth remembering</strong><p>{e(section["callout"])}</p></div>'
            if section.get("callout")
            else ""
        )
        sections.append(
            f'''<section class="prose-section" id="{anchor}">
  <h2>{e(section["heading"])}</h2>
  {paragraphs}
  {bullets}
  {callout}
</section>'''
        )
    related = [item for item in RESOURCES if item["slug"] != resource["slug"]][:3]
    related_cards = [
        {
            "tag": item["category"],
            "title": item["name"],
            "text": item["short"],
            "href": f'/resources/{item["slug"]}/',
            "link_label": "Read guide",
        }
        for item in related
    ]
    related_service_cards = [
        {
            "tag": "Related service",
            "title": SERVICE_BY_SLUG[slug]["name"],
            "text": SERVICE_BY_SLUG[slug]["short"],
            "href": f"/services/{slug}/",
            "link_label": "View service",
        }
        for slug in RESOURCE_SERVICE_LINKS.get(resource["slug"], [])
    ]
    article_schema = {
        "@type": "TechArticle",
        "@id": BASE_URL + path + "#article",
        "headline": resource["name"],
        "description": resource["description"],
        "about": resource["category"],
        "datePublished": LAST_UPDATED,
        "dateModified": LAST_UPDATED,
        "author": {"@id": PERSON_ID},
        "publisher": {"@id": BUSINESS_ID},
        "mainEntityOfPage": {"@id": BASE_URL + path + "#webpage"},
        "image": BASE_URL + OG_IMAGE,
        "inLanguage": "en-IN",
    }
    main = f'''{page_hero(
        path=path,
        eyebrow=resource["category"],
        title=resource["name"],
        lede=resource["intro"],
        meta=[resource["category"], resource["reading"], f"Updated {LAST_UPDATED}"],
    )}

<section class="section">
  <div class="container article-layout">
    <article class="prose article-prose">
      <p class="byline">By <a href="/about/">{e(OWNER_NAME)}</a>, SEO consultant · Updated {e(LAST_UPDATED)}</p>
      {''.join(sections)}
      <div class="article-end"><span aria-hidden="true">✦</span><p>Written by <a href="/about/"><strong>{e(OWNER_NAME)}</strong></a> · Practical SEO guidance from real client work.</p></div>
    </article>
    <aside class="article-aside">
      <div class="aside-panel aside-panel--sticky">
        <p class="eyebrow">On this page</p>
        <h3>Contents</h3>
        <ol class="toc">{''.join(toc)}</ol>
        <a class="btn btn--secondary btn--full" href="/free-seo-review/">Get a free SEO review <span aria-hidden="true">→</span></a>
      </div>
    </aside>
  </div>
</section>

<section class="section">
  <div class="container">
    {section_header("Apply the guide", "Services that connect to this topic", "Use these pages when you need the work scoped and implemented.", ("All services", "/services/"))}
    {card_grid(related_service_cards, 3)}
  </div>
</section>

<section class="section section--surface">
  <div class="container">
    {section_header("Keep reading", "Related guides", "A few more practical starting points.", ("All resources", "/resources/"))}
    {card_grid(related_cards, 3)}
  </div>
</section>

{cta_section("Want this applied to your site?", "A free review turns the checklist into the three changes that matter most for you.")}
'''
    write_page(
        path=path,
        title=branded(resource["name"]),
        description=resource["description"],
        main=main,
        schema_extra=[article_schema],
        og_type="article",
    )


def case_studies_hub() -> None:
    cards = [
        {
            "tag": study["sector"],
            "title": study["name"],
            "text": study["short"],
            "href": f'/case-studies/{study["slug"]}/',
            "link_label": "Read the case study",
        }
        for study in CASE_STUDIES
    ]
    experience_items = "".join(
        f'''<li><span class="timeline__date">{e(item["period"])}</span><h3>{e(item["org"])}</h3><p><strong>{e(item["role"])}.</strong> {e(item["summary"])}</p></li>'''
        for item in EXPERIENCE
    )
    main = f'''{page_hero(
        path="/case-studies/",
        eyebrow="Work",
        title="Work and results",
        lede="Where I’ve worked, what we did, how we did it and what happened — with dates, and including what hasn’t moved yet. Case studies are published only with real data.",
        meta=["Dated results", "Method included", "Misses included"],
    )}

<section class="section">
  <div class="container">
    {proof_strip()}
  </div>
</section>

<section class="section section--surface">
  <div class="container">
    {section_header("Case studies", "Detailed write-ups", "Each one covers the starting point, the work, the outcome and what I’d do differently.")}
    {card_grid(cards, 2)}
  </div>
</section>

<section class="section">
  <div class="container">
    {section_header("Work history", "Engagements", "Confirmed engagements only.", ("About me", "/about/"))}
    <ol class="timeline">{experience_items}</ol>
  </div>
</section>

{cta_section("Want results like these for your business?", "Send your website and your goal. You’ll get an honest first view, free.")}
'''
    write_page(
        path="/case-studies/",
        title="SEO Case Studies: Work, Method & Results | Sreejith Digital",
        description="SEO case studies from a senior consultant in India: where I worked, what we did, how, and dated outcomes — including what hasn’t moved yet.",
        main=main,
        page_type="CollectionPage",
    )


def case_study_page(study: dict) -> None:
    path = f'/case-studies/{study["slug"]}/'
    facts = [
        ("Client", f'<a href="{e(study["client_url"])}">{e(study["client"])}</a>'),
        ("Sector", e(study["sector"])),
        ("Markets", e(study["markets"])),
        ("My role", e(study["role"])),
        ("Period", e(study["period"])),
    ]
    facts_html = "<dl class=\"fact-list\">" + "".join(f"<div><dt>{label}</dt><dd>{value}</dd></div>" for label, value in facts) + "</dl>"
    not_yet = dash_list(CLIENT_NOT_YET)
    differently = "".join(f"<p>{e(paragraph)}</p>" for paragraph in study["differently"])
    article_schema = {
        "@type": "Article",
        "@id": BASE_URL + path + "#article",
        "headline": study["h1"],
        "description": study["description"],
        "datePublished": LAST_UPDATED,
        "dateModified": LAST_UPDATED,
        "author": {"@id": PERSON_ID},
        "publisher": {"@id": BUSINESS_ID},
        "mainEntityOfPage": {"@id": BASE_URL + path + "#webpage"},
        "image": BASE_URL + OG_IMAGE,
        "about": {"@type": "Organization", "name": study["client"], "url": study["client_url"]},
        "inLanguage": "en-IN",
    }
    main = f'''{page_hero(
        path=path,
        eyebrow="Case study · MEP contractor",
        title=study["h1"],
        lede=study["lede"],
        meta=["Baseline: Aug 2026", f"Results: {RESULTS_DATE}", f"AI Overview: {AI_CITATION_DATE}"],
        aside=f'<p class="eyebrow">Snapshot</p>{facts_html}',
    )}

<section class="section">
  <div class="container">
    {proof_strip()}
  </div>
</section>

<section class="section section--surface">
  <div class="container split-section">
    <div class="prose">
      <h2>The starting point</h2>
      <p>The site existed and Google could reach it, but almost nobody found it without already knowing the company’s name.</p>
      {dash_list(study["start"])}
    </div>
    <aside class="aside-panel">
      <p class="eyebrow">The goal</p>
      <h3>Rank for every core service in each target city</h3>
      <p>Seven services — MEP, HVAC, fire protection, electrical, HVAC AMC, building automation and retail fit-out — across Bengaluru, Hyderabad, Chennai and Delhi NCR, plus visibility as a national contractor.</p>
    </aside>
  </div>
</section>

<section class="section">
  <div class="container narrow">
    {section_header("What we did", "The work, in the order it happened", "Each step shipped through a reviewed release with automated checks.")}
    {timeline_html(study["timeline"])}
  </div>
</section>

<section class="section section--surface">
  <div class="container">
    {section_header("How it worked", "The method behind the results")}
    {card_grid(study["method"], 4)}
  </div>
</section>

<section class="section">
  <div class="container split-section">
    <div class="prose">
      <h2>Outcomes</h2>
      <h3>Google positions, {e(RESULTS_DATE)}</h3>
      {rankings_table(CLIENT_RANKINGS, f"Client pages, Google India, recorded {RESULTS_DATE}.")}
      <h3>Google AI Overview, {e(AI_CITATION_DATE)}</h3>
      <p>A logged-out Google search for “MEP contractors in India” showed an AI Overview listing five “Top Pan-India MEP Contractors”: Sterling and Wilson, Blue Star, UMPESL (Voltas), L&amp;T Construction — and Mindtech Solutions, with a citation link to its website. The description Google generated matched the services, sectors and India-wide coverage stated in the site’s structured data and FAQs.</p>
    </div>
    <aside class="aside-panel">
      <p class="eyebrow">Not there yet</p>
      <h3>What hasn’t reached page 1</h3>
      {not_yet}
      <p class="table-note">Reported because results pages that only show wins mean nothing.</p>
    </aside>
  </div>
</section>

<section class="section section--surface">
  <div class="container prose-layout">
    <div class="prose">
      <h2>What I’d do differently</h2>
      {differently}
      <h2>How the results were measured</h2>
      <p>Positions are Google India results recorded on {e(RESULTS_DATE)}. Rankings move daily, so treat them as a dated snapshot rather than a guarantee. The AI Overview was observed in a logged-out session on {e(AI_CITATION_DATE)}. The client’s private analytics are not published here.</p>
    </div>
    <aside class="aside-panel">
      <p class="eyebrow">Related</p>
      <h3>Go deeper</h3>
      <div class="stacked-links">
        <a class="text-link" href="/resources/location-pages-without-doorway-risk/">City pages without doorway risk <span aria-hidden="true">→</span></a>
        <a class="text-link" href="/industries/construction-mep-contractors/">SEO for construction &amp; MEP contractors <span aria-hidden="true">→</span></a>
        <a class="text-link" href="/services/ai-search-optimization/">AI search optimisation (AEO &amp; GEO) <span aria-hidden="true">→</span></a>
      </div>
    </aside>
  </div>
</section>

{cta_section("Want this method applied to your business?", "Send your website and the markets you want. You’ll get the three changes I’d make first — free.")}
'''
    write_page(
        path=path,
        title=study["title"],
        description=study["description"],
        main=main,
        schema_extra=[article_schema],
        og_type="article",
    )


def free_review_page() -> None:
    faqs = [
        ("Is the review actually free?", "Yes. It is a short written review, not a full audit. If a full audit or ongoing work makes sense, I’ll explain what it would involve and you decide. No pressure either way."),
        ("What do you need from me?", "Your website address and your main goal. Later, if we work together, read-only access to Search Console helps. I never need passwords."),
        ("Do you guarantee rankings?", "No. I’ll show you dated results from real work and tell you what is realistic in your market."),
        ("How quickly will I hear back?", "I read every enquiry myself and usually reply within one business day."),
    ]
    main = f'''{page_hero(
        path="/free-seo-review/",
        eyebrow="Free SEO review",
        title="Get a free SEO review of your website",
        lede="Send your website and your goal. I’ll reply with the three changes I’d make first and an honest view on whether SEO is the right channel for you right now.",
        meta=["Free, no obligation", "Reviewed by me, not a tool", "Reply usually within one business day"],
    )}

<section class="section section--tight">
  <div class="container">
    {card_grid([
        {"tag": "01", "title": "The three biggest blockers", "text": "What is most likely holding your site back in Google right now — technical, content or structure."},
        {"tag": "02", "title": "A channel reality check", "text": "Whether SEO, local search, AI search or paid ads is the right place to start for your market."},
        {"tag": "03", "title": "A clear next step", "text": "What I’d do in the first month, so you can act on it with me or without me."},
    ], 3)}
  </div>
</section>

<section class="section">
  <div class="container contact-layout">
    <div class="contact-form-wrap">
      <div class="contact-form-head">
        <p class="eyebrow">Request your review</p>
        <h2>Tell me about the site</h2>
        <p>Website and email are enough. The rest helps me make the review specific.</p>
      </div>
      {enquiry_form(offer="Free SEO review", form_location="free-seo-review", message_required=False, website_required=True, submit_label="Request my free review")}
    </div>
    <aside class="contact-aside">
      <div class="aside-panel">
        <p class="eyebrow">Recent client results</p>
        <h3>MEP contractor · {e(RESULTS_DATE)}</h3>
        {check_list([f'#{row["position"]} — {row["term"]}, {row["city"]}' for row in CLIENT_RANKINGS])}
        <a class="btn btn--secondary btn--full" href="{CASE_STUDY_URL}">Read the case study <span aria-hidden="true">→</span></a>
      </div>
      <div class="aside-panel">
        <p class="eyebrow">How it works</p>
        <h3>Three steps</h3>
        <ol class="mini-steps">
          <li><span>01</span><p><strong>Send</strong><br>Your website and goal.</p></li>
          <li><span>02</span><p><strong>Review</strong><br>I look at the site, the search results and your competitors.</p></li>
          <li><span>03</span><p><strong>Decide</strong><br>You get a written reply. Act on it however you like.</p></li>
        </ol>
      </div>
    </aside>
  </div>
</section>

<section class="section section--surface">
  <div class="container">
    {section_header("Questions", "Before you send it")}
    {faq_html(faqs)}
  </div>
</section>
'''
    write_page(
        path="/free-seo-review/",
        title="Free SEO Review for Indian Businesses | Sreejith Digital",
        description="Get a free, written SEO review from a senior consultant: the three changes to make first and an honest view on whether SEO is right for you now.",
        main=main,
        schema_extra=[faq_schema(faqs)],
        show_mobile_cta=False,
    )


def contact_page() -> None:
    main = f'''{page_hero(
        path="/contact/",
        eyebrow="Contact",
        title="Tell me what you’re trying to grow",
        lede="Share a little context and I’ll come back with the most useful next step. No sales script, no obligation and no ranking promises.",
        meta=["Direct reply from me", "Usually within one business day", "Based in Chennai"],
    )}

<section class="section">
  <div class="container contact-layout">
    <div class="contact-form-wrap">
      <div class="contact-form-head">
        <p class="eyebrow">Enquiry</p>
        <h2>Start with the essentials</h2>
        <p>Your details go straight to my inbox. Nothing is shared or sold.</p>
      </div>
      {enquiry_form(offer="General enquiry", form_location="contact", message_required=True, website_required=False, submit_label="Send enquiry")}
    </div>
    <aside class="contact-aside">
      <div class="aside-panel">
        <p class="eyebrow">Prefer email?</p>
        <h3>Write directly</h3>
        <a class="contact-email-lg" href="mailto:{e(CONTACT_EMAIL)}">{e(CONTACT_EMAIL)}</a>
        <p>Include your website and one sentence about the goal. That is enough to start.</p>
      </div>
      <div class="aside-panel">
        <p class="eyebrow">What happens next</p>
        <h3>A useful first exchange</h3>
        <ol class="mini-steps">
          <li><span>01</span><p><strong>Context</strong><br>I review the goal, the current site and the constraints.</p></li>
          <li><span>02</span><p><strong>Reply</strong><br>I confirm fit and suggest the most useful next step.</p></li>
          <li><span>03</span><p><strong>Scope</strong><br>We agree a focused scope only if there is a clear reason to proceed.</p></li>
        </ol>
      </div>
    </aside>
  </div>
</section>
'''
    write_page(
        path="/contact/",
        title="Contact an SEO Consultant | Sreejith Digital",
        description=f"Contact {OWNER_NAME} about SEO consulting, technical SEO, local or AI search, or a website project. Based in Chennai, working across India.",
        main=main,
        page_type="ContactPage",
        show_mobile_cta=False,
    )


def thank_you_page() -> None:
    main = f'''<section class="section error-page">
  <div class="container">
    <p class="eyebrow eyebrow--pill">Enquiry received</p>
    <h1>Thank you — your enquiry is in.</h1>
    <p class="page-hero__lede">I read every enquiry myself and usually reply within one business day. If it’s urgent, reply to my email when it arrives.</p>
    <p class="enquiry-ref" data-enquiry-ref hidden>Your reference: <strong></strong></p>
    <div class="error-actions">
      <a class="btn btn--primary" href="{CASE_STUDY_URL}">Read the case study <span aria-hidden="true">→</span></a>
      <a class="btn btn--secondary" href="/resources/">Browse the guides</a>
    </div>
  </div>
</section>'''
    write_page(
        path="/thank-you/",
        title="Thank You — Enquiry Received | Sreejith Digital",
        description="Thanks for sending your enquiry. Keep the reference number shown below and check your inbox for the next step.",
        main=main,
        robots="noindex, follow",
        body_class="page-thank-you",
        show_mobile_cta=False,
    )


def privacy_page() -> None:
    main = f'''{page_hero(
        path="/privacy/",
        eyebrow="Legal",
        title="Privacy Policy",
        lede="What this website collects, why, and the choices you have.",
        meta=[f"Last updated {LAST_UPDATED}"],
    )}

<section class="section">
  <div class="container prose-layout">
    <div class="prose">
      <p class="lead">This site collects only what you choose to send, and it loads analytics only if you allow them.</p>
      <h2>Who is responsible</h2>
      <p>{e(OWNER_NAME)}, trading as {e(SITE_NAME)}, Chennai, India, is responsible for personal data collected through this website. Contact: <a href="mailto:{e(CONTACT_EMAIL)}">{e(CONTACT_EMAIL)}</a>.</p>
      <h2>Information you send</h2>
      <p>The enquiry and free-review forms ask for your name, email, website, the service you need, a budget range and an optional message. They are used only to reply to you and, if you ask for one, to prepare your review. You give consent by ticking the box on the form, as required by India’s Digital Personal Data Protection Act, 2023.</p>
      <p>Form submissions are processed by Cloudflare, which hosts this site, and delivered to my inbox. If the form cannot reach the server, your own email app prepares the message instead, and your email provider processes it under its own terms.</p>
      <h2>How long it is kept</h2>
      <p>Enquiries are kept only as long as needed to respond and follow up — normally no longer than 12 months — unless we start working together, in which case they are kept for the length of the engagement and any period the law requires.</p>
      <h2>Analytics and cookies</h2>
      <p>Analytics are off by default. Google Tag Manager, Google Analytics 4 and Microsoft Clarity load only after you choose “Allow analytics”, and Google Analytics and Clarity then set cookies to measure visits and how pages are used. Advertising cookies stay off. You can change your choice at any time with “Cookie settings” in the footer. The site’s own scripts store only that choice in your browser.</p>
      <h2>Technical information</h2>
      <p>The hosting provider may process routine technical data such as IP addresses, request times and requested URLs to deliver the site, keep it secure and prevent abuse. This data is not used for advertising.</p>
      <h2>Your rights</h2>
      <p>You can ask to see, correct or delete the personal data I hold about you, withdraw consent, or raise a concern, by emailing <a href="mailto:{e(CONTACT_EMAIL)}">{e(CONTACT_EMAIL)}</a>. I will respond within a reasonable time.</p>
      <h2>Changes</h2>
      <p>If the way this site handles data changes, this page will be updated before the change takes effect.</p>
    </div>
    <aside class="aside-panel">
      <p class="eyebrow">In short</p>
      <h3>Minimal by design</h3>
      {check_list([
        "Only what you choose to send",
        "Used only to reply to you",
        "Analytics only with your permission",
        "No advertising pixels",
        "Ask any time to see or delete your data",
      ])}
    </aside>
  </div>
</section>
'''
    write_page(
        path="/privacy/",
        title="Privacy Policy | Sreejith Digital",
        description="How the Sreejith Digital website handles enquiries, consent, analytics, cookies and your rights under India’s DPDP Act.",
        main=main,
        show_mobile_cta=False,
    )


def terms_page() -> None:
    main = f'''{page_hero(
        path="/terms/",
        eyebrow="Legal",
        title="Terms of Use",
        lede="Basic terms for using the information published on this website.",
        meta=[f"Last updated {LAST_UPDATED}"],
    )}

<section class="section">
  <div class="container prose-layout">
    <div class="prose">
      <p class="lead">These terms cover this website only. The scope, deliverables, fees, timelines and responsibilities for any consulting engagement are set out in a separate written agreement.</p>
      <h2>Informational content</h2>
      <p>Guides, case studies and service pages are provided for general information. They are not a guarantee of search rankings, traffic, revenue or any specific commercial outcome. Search systems, competitors and business conditions change.</p>
      <h2>Results shown on this site</h2>
      <p>Client results are dated snapshots of publicly observable search results, published with context. They describe what happened for that client at that time, not what will happen for you.</p>
      <h2>No professional relationship by browsing</h2>
      <p>Reading this website, sending an enquiry or receiving a free review does not create a consulting relationship. Work begins only when both parties agree a defined scope in writing.</p>
      <h2>Intellectual property</h2>
      <p>Site copy, design and original diagrams may be linked to and quoted with attribution. They may not be republished as your own.</p>
      <h2>Third-party names</h2>
      <p>Names of third-party products and companies appear for clarity. They remain the property of their owners and do not imply endorsement or partnership.</p>
      <h2>Availability</h2>
      <p>The site is provided as-is. Reasonable care is taken to keep it accurate and available, but uninterrupted access is not guaranteed.</p>
      <h2>Contact</h2>
      <p>Questions about these terms can be sent to <a href="mailto:{e(CONTACT_EMAIL)}">{e(CONTACT_EMAIL)}</a>.</p>
    </div>
    <aside class="aside-panel">
      <p class="eyebrow">Engagements</p>
      <h3>Separate written scope</h3>
      {check_list([
        "Goals and success measures",
        "Deliverables and responsibilities",
        "Timeline and fees",
        "Access and data handling",
        "Review and approval steps",
      ])}
    </aside>
  </div>
</section>
'''
    write_page(
        path="/terms/",
        title="Terms of Use | Sreejith Digital",
        description="Terms for using the Sreejith Digital website, its guides, case studies and free review.",
        main=main,
        show_mobile_cta=False,
    )


def not_found_page() -> None:
    main = f'''<section class="section error-page">
  <div class="container">
    <p class="eyebrow eyebrow--pill">404 · Page not found</p>
    <h1>That URL has moved, or never had a page.</h1>
    <p class="page-hero__lede">These are the best places to start instead.</p>
    <div class="error-actions">
      <a class="btn btn--primary" href="/">Return home <span aria-hidden="true">→</span></a>
      <a class="btn btn--secondary" href="/free-seo-review/">Get a free SEO review</a>
    </div>
    {card_grid([
        {"tag": "Services", "title": "What I do", "text": "Consulting, technical, local and AI search.", "href": "/services/", "link_label": "Open services"},
        {"tag": "Work", "title": "What I’ve done", "text": "Case studies with dated results.", "href": "/case-studies/", "link_label": "Open case studies"},
        {"tag": "Locations", "title": "Where I work", "text": "Six markets, each with an honest status.", "href": "/locations/", "link_label": "Open locations"},
    ], 3)}
  </div>
</section>'''
    write_text(
        SITE_ROOT / "404.html",
        render_page(
            path="/404.html",
            title="Page Not Found | Sreejith Digital",
            description="The requested page could not be found. Explore services, case studies and locations instead.",
            main=main,
            robots="noindex, follow",
        ),
    )


def sitemap_paths() -> list[str]:
    paths = [path for path in GENERATED_PATHS if path not in SITEMAP_EXCLUDE]
    return sorted(set(paths), key=lambda value: (value.count("/"), value))


def write_sitemap() -> None:
    entries = "".join(
        f'''  <url>
    <loc>{BASE_URL}{e(path)}</loc>
    <lastmod>{LAST_UPDATED}</lastmod>
  </url>
'''
        for path in sitemap_paths()
    )
    content = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{entries}</urlset>
'''
    write_text(SITE_ROOT / "sitemap.xml", content)


def write_version_marker() -> None:
    content = "\n".join([
        f"release: {SITE_VERSION}",
        f"updated: {LAST_UPDATED}",
        f"indexable-pages: {len(sitemap_paths())}",
        "homepage-title: SEO Expert in India | Sreejith Digital",
        f"locations: {', '.join(item['name'] for item in LOCATIONS)}",
        f"kerala-cities: {', '.join(city_label(item) for item in KERALA_CITIES)}",
        f"tamil-nadu-cities: {', '.join(city_label(item) for item in STATE_CITIES['tamil-nadu'])}",
        "",
    ])
    write_text(SITE_ROOT / "version.txt", content)


def remove_stale_pages() -> None:
    """Delete generated page folders that no longer exist in the generator."""
    expected = {output_path(path).resolve() for path in GENERATED_PATHS}
    for section in ("services", "industries", "locations", "resources", "case-studies"):
        section_dir = SITE_ROOT / section
        if not section_dir.exists():
            continue
        for index_file in section_dir.glob("*/index.html"):
            if index_file.resolve() not in expected:
                index_file.unlink()
                try:
                    index_file.parent.rmdir()
                except OSError:
                    pass
                print(f"Removed stale page: /{index_file.parent.relative_to(SITE_ROOT)}/")


def main() -> None:
    home_page()
    about_page()
    services_hub()
    for service in SERVICES:
        service_page(service)
    industries_hub()
    for industry in INDUSTRIES:
        industry_page(industry)
    locations_hub()
    for location in LOCATIONS:
        location_page(location)
    for state_slug, cities in STATE_CITIES.items():
        for city in cities:
            state_city_page(state_slug, city)
    resources_hub()
    for resource in RESOURCES:
        resource_page(resource)
    case_studies_hub()
    for study in CASE_STUDIES:
        case_study_page(study)
    free_review_page()
    contact_page()
    thank_you_page()
    privacy_page()
    terms_page()
    not_found_page()
    remove_stale_pages()
    write_sitemap()
    write_version_marker()
    print(f"Generated {len(sitemap_paths())} indexable pages plus thank-you, 404.html, sitemap.xml and version.txt")


if __name__ == "__main__":
    main()
