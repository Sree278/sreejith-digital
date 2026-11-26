#!/usr/bin/env python3
"""Generate the static HTML website for sreejithdigital.com.

The generated files are committed to public/, which is the static asset
directory used by both Cloudflare Workers static assets and Cloudflare Pages.
Run this script from anywhere to regenerate every page and the sitemap:

    python3 scripts/generate_site.py
"""

from __future__ import annotations

import json
from html import escape
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = REPO_ROOT / "public"
BASE_URL = "https://sreejithdigital.com"
SITE_NAME = "Sreejith Digital"
CONTACT_EMAIL = "hello@sreejithdigital.com"
LAST_UPDATED = "2026-11-26"
SITE_VERSION = "2026-11-26.1"
DEFAULT_DESCRIPTION = (
    "Independent SEO consultant in India helping businesses grow through technical "
    "SEO, local SEO, strategic content and organic search optimization. Get a "
    "practical SEO growth roadmap."
)


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
            ("Independent audit", "An unbiased review of current performance, technical debt, and content gaps."),
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

LOCATIONS = [
    {
        "slug": "chennai",
        "name": "Chennai",
        "short": "Search strategy shaped around Chennai’s local and regional intent.",
        "description": "Remote-first SEO consulting for organisations targeting Chennai and surrounding service areas.",
        "intro": "Build clear local relevance for Chennai searches while keeping the wider site architecture easy to manage.",
        "market": "Chennai searches often blend city-level discovery with specific service, neighbourhood, and business-profile intent.",
        "focus": [
            "Location-aware service and sector pages",
            "Business profile categories and content",
            "Local trust signals and review workflows",
            "Internal links from relevant service pages",
        ],
    },
    {
        "slug": "bengaluru",
        "name": "Bengaluru",
        "short": "Organic search support for competitive technology and B2B markets.",
        "description": "Remote-first SEO consulting for organisations competing for search visibility in Bengaluru.",
        "intro": "Differentiate expertise and offer clarity in a market where generic category pages are rarely enough.",
        "market": "Bengaluru’s technology and professional-service searches can be competitive, so page specificity and credible proof matter.",
        "focus": [
            "Distinct positioning for product and service pages",
            "Comparison and evaluation content",
            "Technical foundations for fast-growing sites",
            "Conversion paths suited to longer buying cycles",
        ],
    },
    {
        "slug": "kochi",
        "name": "Kochi",
        "short": "Local search foundations for growing service and destination businesses.",
        "description": "Remote-first SEO consulting for organisations serving Kochi and nearby markets.",
        "intro": "Make local offers easy to understand across search results, profiles, and useful location pages.",
        "market": "Kochi businesses often need a clean local presence that works for both nearby customers and visitors researching in advance.",
        "focus": [
            "Clear service-area and location-page structure",
            "Business profile and citation consistency",
            "Content that answers pre-enquiry questions",
            "Measurement of calls, directions, and enquiries",
        ],
    },
    {
        "slug": "mumbai",
        "name": "Mumbai",
        "short": "Structured search visibility for high-competition metro searches.",
        "description": "Remote-first SEO consulting for organisations targeting Mumbai’s dense, competitive search market.",
        "intro": "Use a deliberate architecture and reliable local signals to compete without publishing thin city pages.",
        "market": "Mumbai searches can be broad and highly competitive, making clear page roles, strong internal links, and trustworthy data essential.",
        "focus": [
            "Service, industry, and location page relationships",
            "Consistent multi-location business information",
            "Technical improvements for larger websites",
            "Reporting that separates branded and non-branded demand",
        ],
    },
    {
        "slug": "delhi-ncr",
        "name": "Delhi NCR",
        "short": "One coherent search architecture for a multi-city business region.",
        "description": "Remote-first SEO consulting for organisations targeting Delhi, Gurugram, Noida and the wider NCR market.",
        "intro": "Build one coherent search architecture for a region where city, satellite-city and sector queries frequently overlap.",
        "market": "Delhi NCR searches often span several business districts, so page roles, internal links and consistent business data matter more than a stack of near-identical city pages.",
        "focus": [
            "Distinct roles for Delhi, Gurugram and Noida content where genuinely needed",
            "Service and industry pages that support regional intent",
            "Business profile and citation consistency",
            "Reporting that separates local, regional and branded demand",
        ],
    },
    {
        "slug": "hyderabad",
        "name": "Hyderabad",
        "short": "Technical and content-led SEO for technology and growth-stage teams.",
        "description": "Remote-first SEO consulting for organisations targeting Hyderabad’s technology, professional-service and growth-stage business searches.",
        "intro": "Combine technical clarity with useful decision-stage content in a market where generic service pages rarely differentiate a business.",
        "market": "Hyderabad has a mix of technology, enterprise and fast-growing service searches, making site architecture, proof and conversion paths especially important.",
        "focus": [
            "Technical foundations for expanding websites",
            "Evaluation-stage content for considered purchases",
            "Clear service-to-industry page relationships",
            "Conversion tracking for qualified enquiries",
        ],
    },
    {
        "slug": "pune",
        "name": "Pune",
        "short": "Search foundations for startups, manufacturers and professional services.",
        "description": "Remote-first SEO consulting for startups, manufacturers and professional-service teams targeting Pune.",
        "intro": "Create a maintainable search foundation for teams that need qualified enquiries without an oversized marketing site.",
        "market": "Pune searches often combine startup, manufacturing, education and local-service intent, so the site needs a clear hierarchy rather than broad, unfocused pages.",
        "focus": [
            "Lean information architecture for smaller teams",
            "Distinct service and sector landing pages",
            "Local profile and business-data consistency",
            "Measurement of calls, forms and qualified enquiries",
        ],
    },
]

LOCATION_TIERS = {
    "chennai": "Priority 1 · Core market",
    "bengaluru": "Priority 1 · Core market",
    "mumbai": "Priority 1 · Core market",
    "delhi-ncr": "Priority 1 · Core market",
    "hyderabad": "Priority 1 · Core market",
    "kochi": "Priority 2 · Expansion market",
    "pune": "Priority 2 · Expansion market",
}

PLANNED_LOCATIONS = [
    "Kolkata",
    "Ahmedabad",
    "Jaipur",
    "Coimbatore",
    "Gurugram",
    "Noida",
    "Thiruvananthapuram",
    "Indore",
]

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

RESOURCE_SERVICE_LINKS = {
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
    "contact": "Contact",
    "privacy": "Privacy Policy",
    "terms": "Terms",
}

LABEL_LOOKUP = dict(STATIC_LABELS)
for collection in (SERVICES, INDUSTRIES, LOCATIONS, RESOURCES):
    for item in collection:
        LABEL_LOOKUP[item["slug"]] = item["name"]

SERVICE_BY_SLUG = {item["slug"]: item for item in SERVICES}
INDUSTRY_BY_SLUG = {item["slug"]: item for item in INDUSTRIES}
LOCATION_BY_SLUG = {item["slug"]: item for item in LOCATIONS}
RESOURCE_BY_SLUG = {item["slug"]: item for item in RESOURCES}

SERVICE_SEO_TITLES = {
    "seo-services": "SEO Services India | Organic Growth Consulting",
    "seo-consulting": "SEO Consulting India | Independent SEO Consultant",
    "local-seo": "Local SEO Expert India | Profiles & Location Pages",
    "google-ads-management": "Google Ads Management India | Paid Search Consulting",
    "website-design": "SEO Website Design India | Fast Static Sites",
    "technical-seo": "Technical SEO Consultant India | Audits & Implementation",
    "content-strategy": "SEO Content Strategy India | Topic Clusters",
    "analytics-reporting": "SEO Analytics & Reporting India | Measurement",
}


def child_links(root: str, label: str, items: list[dict], overview: str) -> list[dict]:
    links = [{"label": f"All {label.lower()}", "href": root, "description": overview}]
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
    {"label": "Home", "href": "/"},
    {"label": "About", "href": "/about/"},
    {
        "label": "Services",
        "href": "/services/",
        "children": child_links(
            "/services/", "Services", SERVICES[:6], "See the complete service architecture"
        ),
    },
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
            "/locations/", "Locations", LOCATIONS, "Explore the location architecture"
        ),
    },
    {
        "label": "Resources",
        "href": "/resources/",
        "children": child_links(
            "/resources/", "Resources", RESOURCES[:6], "Browse practical guides and checklists"
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
                children.append(
                    f'<a class="nav-panel__link" href="{e(child["href"])}"{current_attr}>'
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
      <a class="nav-panel__link nav-panel__link--overview" href="{e(item["href"])}">
        <strong>Overview</strong><span>Open the {e(item["label"].lower())} hub</span>
      </a>
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
    <a class="btn btn--small btn--primary header-cta" href="/contact/">Book a consultation <span aria-hidden="true">→</span></a>
    <button class="nav-toggle" type="button" data-nav-toggle aria-controls="primary-nav" aria-expanded="false" aria-label="Open navigation">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>'''


def render_footer() -> str:
    service_links = "".join(
        f'<li><a href="/services/{e(item["slug"])}/">{e(item["name"])}</a></li>'
        for item in SERVICES[:6]
    )
    explore_links = "".join(
        f'<li><a href="{e(href)}">{e(label)}</a></li>'
        for label, href in [
            ("About", "/about/"),
            ("Industries", "/industries/"),
            ("Locations", "/locations/"),
            ("Resources", "/resources/"),
            ("Contact", "/contact/"),
        ]
    )
    return f'''<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-intro">
      <a class="brand" href="/" aria-label="{e(SITE_NAME)} home">
        <span class="brand__mark" aria-hidden="true"><span></span></span>
        <span class="brand__text">SREEJITH <span>DIGITAL</span></span>
      </a>
      <p>Independent SEO consulting for teams that value clear priorities, careful execution, and honest reporting.</p>
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
        <li><a href="/sitemap.xml">Sitemap</a></li>
        <li><a href="/robots.txt">Robots.txt</a></li>
      </ul>
    </div>
  </div>
  <div class="container footer-bottom">
    <p>© <span data-year>2026</span> {e(SITE_NAME)}. All rights reserved.</p>
    <p>Independent consultancy · Remote-first delivery</p>
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
        if href:
            item["item"] = BASE_URL + href
        elements.append(item)
    return {"@type": "BreadcrumbList", "itemListElement": elements}


def render_breadcrumbs(path: str) -> str:
    crumbs = breadcrumb_items(path)
    parts = []
    for label, href in crumbs:
        if href:
            parts.append(f'<li><a href="{e(href)}">{e(label)}</a></li>')
        else:
            parts.append(f'<li aria-current="page">{e(label)}</li>')
    return f'<nav class="breadcrumbs" aria-label="Breadcrumb"><ol>{"".join(parts)}</ol></nav>'


def base_schema(path: str, title: str, description: str) -> list[dict]:
    org = {
        "@type": ["Organization", "ProfessionalService"],
        "@id": BASE_URL + "/#organization",
        "name": SITE_NAME,
        "url": BASE_URL + "/",
        "description": DEFAULT_DESCRIPTION,
        "email": CONTACT_EMAIL,
        "areaServed": ["India", "Remote"],
    }
    web_page = {
        "@type": "WebPage",
        "@id": BASE_URL + path + "#webpage",
        "url": BASE_URL + path,
        "name": title,
        "description": description,
        "isPartOf": {"@id": BASE_URL + "/#website"},
        "about": {"@id": BASE_URL + "/#organization"},
    }
    web_site = {
        "@type": "WebSite",
        "@id": BASE_URL + "/#website",
        "url": BASE_URL + "/",
        "name": SITE_NAME,
        "publisher": {"@id": BASE_URL + "/#organization"},
        "inLanguage": "en",
    }
    graph = [org, web_site, web_page]
    if path != "/":
        graph.append(breadcrumb_schema(path))
    return graph


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
) -> str:
    page_title = title if SITE_NAME in title else f"{title} | {SITE_NAME}"
    article_meta = ""
    if og_type == "article":
        article_meta = (
            f'  <meta property="article:published_time" content="{LAST_UPDATED}">\n'
            f'  <meta property="article:modified_time" content="{LAST_UPDATED}">\n'
        )
    canonical = BASE_URL + path
    graph = base_schema(path, page_title, description)
    if schema_extra:
        graph.extend(schema_extra)
    structured_data = json.dumps(
        {"@context": "https://schema.org", "@graph": graph},
        ensure_ascii=False,
        indent=2,
    ).replace("</", "<\\/")
    body_class_attr = f' class="{e(body_class)}"' if body_class else ""
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#050706">
  <title>{e(page_title)}</title>
  <meta name="description" content="{e(description)}">
  <meta name="author" content="{e(SITE_NAME)}">
  <meta name="robots" content="{e(robots)}">
  <link rel="canonical" href="{e(canonical)}">
  <meta property="og:type" content="{e(og_type)}">
  <meta property="og:site_name" content="{e(SITE_NAME)}">
  <meta property="og:title" content="{e(page_title)}">
  <meta property="og:description" content="{e(description)}">
  <meta property="og:url" content="{e(canonical)}">
  <meta property="og:image" content="{BASE_URL}/assets/img/og-image.svg">
{article_meta}  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{e(page_title)}">
  <meta name="twitter:description" content="{e(description)}">
  <meta name="twitter:image" content="{BASE_URL}/assets/img/og-image.svg">
  <link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/assets/css/styles.css">
  <script type="application/ld+json">
{structured_data}
  </script>
  <script src="/assets/js/main.js" defer></script>
</head>
<body{body_class_attr}>
{render_header(path)}
<main id="main">
{main}
</main>
{render_footer()}
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


def write_page(**kwargs: object) -> None:
    path = str(kwargs["path"])
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
        tag = f'<span class="card__tag">{e(card["tag"])}</span>' if card.get("tag") else ""
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


def cta_section(
    title: str = "Ready for a clearer search roadmap?",
    text: str = "Tell me what you are trying to grow, what has already been tried, and where the current site gets in the way.",
) -> str:
    return f'''<section class="section cta-section">
  <div class="container cta-panel">
    <div>
      <p class="eyebrow">Start a conversation</p>
      <h2>{e(title)}</h2>
      <p>{e(text)}</p>
    </div>
    <div class="cta-actions">
      <a class="btn btn--primary" href="/contact/">Book a consultation <span aria-hidden="true">→</span></a>
      <a class="btn btn--secondary" href="mailto:{e(CONTACT_EMAIL)}">Email directly</a>
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


def home_page() -> None:
    service_cards_data = [
        {
            "tag": "SEO Consulting",
            "title": "SEO Consulting",
            "text": "Get expert SEO direction, actionable recommendations and a clear roadmap to improve organic search performance.",
            "href": "/services/seo-consulting/",
            "link_label": "View SEO consulting",
        },
        {
            "tag": "Technical SEO",
            "title": "Technical SEO",
            "text": "Identify and resolve crawling, indexing, website architecture, performance and technical issues that affect visibility.",
            "href": "/services/technical-seo/",
            "link_label": "View technical SEO",
        },
        {
            "tag": "Local SEO",
            "title": "Local SEO",
            "text": "Improve local search visibility through location-focused optimisation, Business Profile guidance and local strategy.",
            "href": "/services/local-seo/",
            "link_label": "View local SEO",
        },
        {
            "tag": "Content",
            "title": "SEO Strategy & Content Optimisation",
            "text": "Develop keyword strategies, improve existing content and create relevant pages aligned with user search intent.",
            "href": "/services/content-strategy/",
            "link_label": "View content strategy",
        },
        {
            "tag": "Paid Search",
            "title": "Google Ads Management",
            "text": "Support organic growth with paid search campaigns designed around relevant enquiries and measurable outcomes.",
            "href": "/services/google-ads-management/",
            "link_label": "View Google Ads",
        },
        {
            "tag": "Website Design",
            "title": "Website Design & SEO",
            "text": "Improve websites with clear information architecture, user experience, search-friendly structures and conversion-focused layouts.",
            "href": "/services/website-design/",
            "link_label": "View website design",
        },
    ]
    industry_cards_data = [
        {
            "tag": "Industry",
            "title": item["name"],
            "text": item["short"],
            "href": f'/industries/{item["slug"]}/',
            "link_label": "View approach",
        }
        for item in INDUSTRIES
    ]
    location_links_html = '<div class="city-links">' + "".join(
        f'<a href="/locations/{e(item["slug"])}/">{e(item["name"])}</a>'
        for item in LOCATIONS
    ) + "</div>"
    resource_cards_data = [
        {
            "tag": item["category"],
            "title": item["name"],
            "text": item["short"],
            "href": f'/resources/{item["slug"]}/',
            "link_label": "Read guide",
        }
        for item in RESOURCES[4:7]
    ]
    approach_steps = [
        ("Discover", "Understand the business, target audience, existing website performance and organic search opportunities."),
        ("Diagnose", "Review technical SEO, keyword targeting, content quality, competitors and website conversion paths."),
        ("Prioritise", "Create a practical SEO roadmap with clearly defined priorities and implementation recommendations."),
        ("Improve and measure", "Implement improvements, monitor search performance and refine the strategy using meaningful data."),
    ]
    why_items = [
        "Independent SEO consulting",
        "Direct communication and focused attention",
        "Practical, implementation-ready recommendations",
        "Technical and strategic SEO expertise",
        "Transparent performance measurement",
        "No unrealistic ranking guarantees",
        "A business-focused approach to organic growth",
    ]
    homepage_faqs = [
        (
            "What does an independent SEO consultant do?",
            "An independent SEO consultant evaluates a website’s search performance, identifies optimisation opportunities and develops a strategy to improve organic visibility, qualified traffic and business enquiries.",
        ),
        (
            "Do you provide SEO consulting across India?",
            "Yes. Sreejith Digital follows a remote-first consulting model and works with businesses across India, including Chennai, Bengaluru, Mumbai, Delhi NCR, Hyderabad, Pune and Kochi.",
        ),
        (
            "What SEO services are available?",
            "Services include SEO consulting, technical SEO, local SEO, keyword research, content optimisation, website SEO strategy and organic search performance improvement.",
        ),
        (
            "How long does SEO take to show results?",
            "SEO timelines vary depending on website condition, competition, industry and implementation. Meaningful improvements generally require consistent work over several months. No specific ranking position or timeline can be guaranteed.",
        ),
        (
            "Can you audit my existing website?",
            "Yes. A website SEO audit can identify technical problems, content gaps, keyword opportunities and improvements to website architecture and organic search performance.",
        ),
    ]
    faq_schema = {
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": question,
                "acceptedAnswer": {"@type": "Answer", "text": answer},
            }
            for question, answer in homepage_faqs
        ],
    }
    main = f'''<section class="hero">
  <div class="hero__glow" aria-hidden="true"></div>
  <div class="container hero-grid">
    <div class="hero-copy">
      <p class="eyebrow eyebrow--pill">Independent SEO consultant · India</p>
      <h1>Independent SEO Consultant in India <span>Helping Businesses Grow Organically</span></h1>
      <p class="hero-lede">Build sustainable organic visibility with a clear SEO strategy, technical expertise and practical execution.</p>
      <div class="hero-actions">
        <a class="btn btn--primary" href="/contact/">Book an SEO consultation <span aria-hidden="true">→</span></a>
        <a class="btn btn--secondary" href="/services/">Explore SEO services</a>
      </div>
      <ul class="hero-proof">
        <li><strong>Independent</strong><span>Direct senior-level attention</span></li>
        <li><strong>Practical</strong><span>Implementation-ready work</span></li>
        <li><strong>Transparent</strong><span>No ranking promises</span></li>
      </ul>
    </div>
    <div class="hero-visual" aria-label="Illustration of a prioritised SEO roadmap">
      <div class="visual-card">
        <div class="visual-card__top">
          <span class="status-dot" aria-hidden="true"></span>
          <div><strong>Growth system</strong><span>Quarterly roadmap</span></div>
          <span class="visual-badge">Live</span>
        </div>
        <div class="visual-score">
          <div><span>Focus</span><strong>4 priorities</strong></div>
          <div class="score-ring" aria-hidden="true"><span>04</span></div>
        </div>
        <div class="visual-rows">
          <div><span>Fix indexation</span><b>Technical</b><i class="bar bar--high" aria-hidden="true"></i></div>
          <div><span>Map service intent</span><b>Strategy</b><i class="bar bar--mid" aria-hidden="true"></i></div>
          <div><span>Improve location pages</span><b>Local</b><i class="bar bar--low" aria-hidden="true"></i></div>
        </div>
        <div class="visual-footer"><span>Evidence → Priority → Delivery → Measurement</span><span aria-hidden="true">↗</span></div>
      </div>
      <div class="floating-note"><span aria-hidden="true">✦</span><p><strong>One roadmap.</strong><br>Every recommendation has an owner.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container prose-layout">
    <div class="prose">
      <p class="lead">Sreejith Digital provides independent SEO consulting for businesses looking to improve search visibility, attract qualified visitors and turn organic traffic into meaningful business enquiries.</p>
      <h2>SEO Consulting That Connects Search Visibility With Business Growth</h2>
      <p>Getting more website traffic is not the only objective of SEO. Your website needs to reach the right audience, answer their search requirements and encourage meaningful action.</p>
      <p>From technical SEO and website optimisation to local search and content strategy, every recommendation is focused on business objectives, search intent and measurable improvement. Whether you are building a new website, improving existing visibility or expanding into competitive markets, the focus stays on identifying what matters and prioritising the right improvements.</p>
    </div>
    <aside class="aside-panel">
      <p class="eyebrow">Consultation focus</p>
      <h3>Qualified enquiries, not just traffic</h3>
      {check_list([
        "Clear commercial outcomes",
        "Search intent mapped to pages",
        "Technical foundations verified",
        "Implementation-ready recommendations",
        "Honest, decision-focused reporting",
      ])}
      <a class="btn btn--secondary btn--full" href="/contact/">Discuss your SEO roadmap <span aria-hidden="true">→</span></a>
    </aside>
  </div>
</section>

<section class="section section--surface">
  <div class="container">
    {section_header("Independent SEO Services for Growing Businesses", "Choose the right entry point", "Use one focused service or connect strategy, technical work, local search, paid media and measurement into a single programme.", ("All services", "/services/"))}
    {card_grid(service_cards_data, 3)}
  </div>
</section>

<section class="section">
  <div class="container">
    {section_header("SEO Consulting for Different Business Models", "Strategy shaped by how customers search", "SEO strategies should reflect how customers research, compare and decide—not just the industry label.", ("All industries", "/industries/"))}
    {card_grid(industry_cards_data, 2)}
  </div>
</section>

<section class="section section--surface">
  <div class="container">
    {section_header("SEO Consultant Serving Businesses Across India", "Remote-first, market-aware", "Sreejith Digital provides remote-first independent SEO consulting to businesses across India. Each market strategy is developed around the business, its customers and the search competition—without claiming physical offices.", ("All locations", "/locations/"))}
    {location_links_html}
  </div>
</section>

<section class="section">
  <div class="container split-section">
    <div>
      {section_header("A Practical Approach to SEO Growth", "Short roadmap. Careful delivery. Plain-language reporting.")}
      {numbered_steps(approach_steps)}
    </div>
    <aside class="aside-panel">
      <p class="eyebrow">Why Sreejith Digital</p>
      <h3>Built around clarity and useful work</h3>
      {check_list(why_items)}
      <a class="btn btn--secondary btn--full" href="/about/">More about the approach <span aria-hidden="true">→</span></a>
    </aside>
  </div>
</section>

<section class="section section--surface">
  <div class="container">
    {section_header("Frequently Asked Questions", "Useful answers before you get in touch")}
    {faq_html(homepage_faqs)}
  </div>
</section>

<section class="section">
  <div class="container">
    {section_header("Practical SEO Resources", "Guides for in-house teams", "Straightforward explanations for Indian businesses evaluating SEO, local search, pricing and measurement.", ("All resources", "/resources/"))}
    {card_grid(resource_cards_data, 3)}
  </div>
</section>

{cta_section("Let’s Build a Better Organic Search Strategy", "Your website should attract relevant visitors, communicate your expertise and support business growth. If you need an independent SEO consultant to identify opportunities and develop a practical roadmap, let’s discuss your requirements.")}
'''
    write_page(
        path="/",
        title="SEO Consultant India | Technical & Local SEO – Sreejith Digital",
        description=DEFAULT_DESCRIPTION,
        main=main,
        body_class="page-home",
        schema_extra=[faq_schema],
    )

def about_page() -> None:
    principles = [
        {"title": "Clarity before activity", "text": "Every action should connect to a business goal, an owner, and a way to verify the change."},
        {"title": "Evidence over folklore", "text": "Use data and observed site behaviour, and be explicit when the evidence is incomplete."},
        {"title": "Architecture first", "text": "A clean structure makes content, internal links, local pages, and reporting easier to scale."},
        {"title": "Honest measurement", "text": "Report outcomes and uncertainty together. No vanity metrics dressed up as growth."},
    ]
    models = [
        {"tag": "01", "title": "Audit & roadmap", "text": "A focused review that ends with a prioritised, implementation-ready plan."},
        {"tag": "02", "title": "Consulting retainer", "text": "Recurring strategic support, implementation review, and decision documentation."},
        {"tag": "03", "title": "Build project", "text": "A defined site, local architecture, or measurement build with clear acceptance criteria."},
    ]
    main = f'''{page_hero(
        path="/about/",
        eyebrow="About",
        title="Independent, senior-level SEO support",
        lede="Sreejith Digital is an independent consultancy built around direct attention, practical decisions, and work your team can understand and maintain.",
        meta=["Independent consultancy", "Remote-first", "Strategy + delivery"],
    )}

<section class="section">
  <div class="container prose-layout">
    <div class="prose">
      <p class="lead">Good consulting should leave your team with more than a slide deck. It should leave behind a clearer structure, better decisions, and documentation that still makes sense months later.</p>
      <h2>Work directly with the consultant</h2>
      <p>Engagements are intentionally focused. That keeps context close to the work, reduces hand-off noise, and makes it easier to connect technical findings, content decisions, and commercial goals.</p>
      <h2>Built for teams that value the details</h2>
      <p>Some teams need a full organic growth programme. Others already have strong writers, developers, or media buyers and need a sharper strategy or an independent technical review. The scope starts with the capacity and constraints you actually have.</p>
    </div>
    <aside class="aside-panel">
      <p class="eyebrow">At a glance</p>
      <h3>What stays consistent</h3>
      {check_list([
        "A single, documented roadmap",
        "Plain-language recommendations",
        "No guaranteed ranking claims",
        "No analytics or tracking by default on this site",
        "Clear handover of every deliverable",
      ])}
    </aside>
  </div>
</section>

<section class="section section--surface">
  <div class="container">
    {section_header("Principles", "How the work is approached", "A few simple rules keep the engagement useful and the reporting credible.")}
    {card_grid(principles, 4)}
  </div>
</section>

<section class="section">
  <div class="container">
    {section_header("Engagement models", "A scope that fits your team", "The shape of the work follows your goals and execution capacity—not a fixed package.")}
    {card_grid(models, 3)}
  </div>
</section>

{cta_section("Have a project in mind?", "Share the current site, the goal, and the constraint. I will come back with the most useful next step.")}
'''
    write_page(
        path="/about/",
        title="About Sreejith Digital | Independent SEO Consultant India",
        description="Learn how Sreejith Digital approaches independent SEO consulting, implementation, and reporting.",
        main=main,
    )


def services_hub() -> None:
    main = f'''{page_hero(
        path="/services/",
        eyebrow="Services",
        title="A connected service architecture",
        lede="Use one focused service or combine strategy, technical work, content, local search, paid media, and measurement into a single programme.",
        meta=["8 focused services", "Strategy + implementation", "No fixed packages"],
    )}

<section class="section">
  <div class="container">
    {section_header("Explore services", "Choose the work you need now", "Each page includes what is covered, who it suits, deliverables, process, and common questions.")}
    {service_cards(SERVICES, 3)}
  </div>
</section>

<section class="section section--surface">
  <div class="container split-section">
    <div>
      {section_header("How services connect", "Avoid isolated fixes", "A technical issue, a content gap, and a weak conversion path often share the same root cause. The services are designed to be combined without creating competing priorities.")}
      {numbered_steps([
        ("Establish the foundation", "Technical SEO and analytics define what can be trusted and measured."),
        ("Clarify demand", "Content strategy and keyword-to-URL mapping give pages distinct jobs."),
        ("Capture intent", "Local SEO, website design, and Google Ads connect the offer to the moment of action."),
        ("Keep it accountable", "Consulting and reporting turn activity into a maintained roadmap."),
      ])}
    </div>
    <aside class="aside-panel">
      <p class="eyebrow">Not sure where to start?</p>
      <h3>Begin with a conversation</h3>
      <p>A short discovery call is usually enough to identify whether you need an audit, a strategy, hands-on delivery, or a website build.</p>
      <a class="btn btn--primary" href="/contact/">Book a consultation <span aria-hidden="true">→</span></a>
    </aside>
  </div>
</section>

{cta_section()}
'''
    write_page(
        path="/services/",
        title="SEO Services India | Consulting, Technical & Local SEO",
        description="Explore SEO services, consulting, local SEO, Google Ads management, website design, technical SEO, content strategy, and reporting.",
        main=main,
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
        "name": service["name"],
        "serviceType": service["name"],
        "description": service["description"],
        "provider": {"@id": BASE_URL + "/#organization"},
        "areaServed": ["India", "Remote"],
        "url": BASE_URL + path,
    }
    aside = f'''<p class="eyebrow">Best for</p>
<p>{e(service["audience"])}</p>
<a class="btn btn--primary btn--full" href="/contact/">Discuss this service <span aria-hidden="true">→</span></a>'''
    main = f'''{page_hero(
        path=path,
        eyebrow="Service",
        title=service["name"],
        lede=service["intro"],
        meta=["Focused scope", "Practical deliverables", "Clear handover"],
        aside=aside,
    )}

<section class="section">
  <div class="container">
    {section_header("What is covered", "Practical work, clearly scoped", service["description"])}
    {card_grid(included_cards, 3)}
  </div>
</section>

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

{cta_section("Want to scope this properly?", "Share your site, the goal, and the team available. The first conversation should make the next step obvious.")}
'''
    write_page(
        path=path,
        title=SERVICE_SEO_TITLES.get(service["slug"], service["name"]),
        description=service["description"],
        main=main,
        schema_extra=[service_schema],
    )


def industries_hub() -> None:
    cards = [
        {
            "tag": "Industry",
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
        title="Search strategy shaped by context",
        lede="Different business models create different search problems. These pages explain the common constraints and how the work is structured to address them.",
        meta=["B2B & SaaS", "Professional services", "Ecommerce", "Multi-location"],
    )}

<section class="section">
  <div class="container">
    {section_header("Explore industries", "A starting point, not a template", "The principles are consistent; the architecture and priorities should reflect how your customers actually decide.")}
    {card_grid(cards, 2)}
  </div>
</section>

<section class="section section--surface">
  <div class="container">
    {section_header("Shared foundation", "What every industry engagement starts with")}
    {check_list([
      "A clear commercial outcome and a realistic time horizon",
      "One primary URL for each priority search intent",
      "Technical foundations that support—not undermine—the content",
      "Measurement definitions the whole team can trust",
      "A page structure that can expand without creating overlap",
    ])}
  </div>
</section>

{cta_section("Need an industry-specific view?", "Tell me the business model and the current bottleneck. I will suggest the most relevant starting point.")}
'''
    write_page(
        path="/industries/",
        title="SEO for B2B, SaaS, Ecommerce & Professional Services",
        description="SEO approaches for B2B and SaaS, professional services, ecommerce, and multi-location organisations.",
        main=main,
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
    main = f'''{page_hero(
        path=path,
        eyebrow="Industry",
        title=industry["name"],
        lede=industry["intro"],
        meta=["Context-led strategy", "No generic template"],
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

<section class="section section--surface">
  <div class="container">
    {section_header("Approach", "How the work is structured", "A practical sequence that keeps pages, content, and measurement aligned.")}
    {card_grid(approach_cards, 3)}
  </div>
</section>

<section class="section">
  <div class="container">
    {section_header("Useful starting points", "Services that often fit", "These are common combinations, not fixed bundles.", ("All services", "/services/"))}
    {card_grid(service_links, 3)}
  </div>
</section>

{cta_section()}
'''
    write_page(
        path=path,
        title=f'{industry["name"]} SEO Services India | Sreejith Digital',
        description=industry["description"],
        main=main,
    )


def locations_hub() -> None:
    cards = [
        {
            "tag": LOCATION_TIERS.get(item["slug"], "Location"),
            "title": item["name"],
            "text": item["short"],
            "href": f'/locations/{item["slug"]}/',
            "link_label": "View location",
        }
        for item in LOCATIONS
    ]
    planned_html = '<div class="page-hero__meta">' + "".join(
        f'<span>{e(name)}</span>' for name in PLANNED_LOCATIONS
    ) + "</div>"
    main = f'''{page_hero(
        path="/locations/",
        eyebrow="Locations",
        title="Local relevance with a clean architecture",
        lede="Location pages should help people verify, choose, and act. They should also connect cleanly to the services and industries they support.",
        meta=["Remote-first delivery", "City-level research", "No thin duplicates"],
    )}

<section class="section">
  <div class="container">
    {section_header("Explore locations", "Priority location guides", "Each guide has a distinct market context and links to the services that support it. New cities are added only when there is useful local information to publish.", ("Local SEO service", "/services/local-seo/"))}
    {card_grid(cards, 2)}
  </div>
</section>

<section class="section section--surface">
  <div class="container prose-layout">
    <div class="prose">
      <p class="lead">These pages describe remote-first consulting tailored to a market. They are not claims of physical offices.</p>
      <h2>A hierarchy that can grow</h2>
      <p>Start with a location hub, create useful pages only for genuine service areas, and link each one to the relevant service and industry pages. That structure is easier to maintain than a large set of near-identical landing pages.</p>
      <h2>Substance over substitution</h2>
      <p>Each location page should add real context: the services available, the audience, local trust signals, and a clear next step. Swapping a city name into the same paragraph does not create relevance.</p>
    </div>
    <aside class="aside-panel">
      <p class="eyebrow">Architecture rule</p>
      <h3>One page, one job</h3>
      {check_list([
        "A hub for navigation",
        "A distinct page for each genuine service area",
        "Service pages for the offer",
        "Industry pages for context",
        "Resources for useful supporting detail",
      ])}
    </aside>
  </div>
</section>

<section class="section">
  <div class="container">
    {section_header("Expansion plan", "Markets to add after real local insight", "These locations are deliberately not published as thin pages yet. Each one should get a distinct page only after its search intent, audience and service context are documented.")}
    {planned_html}
  </div>
</section>

{cta_section("Planning a multi-location site?", "A short architecture review can prevent months of duplicated pages and overlapping keywords.")}
'''
    write_page(
        path="/locations/",
        title="SEO Consultant India: City Guides | Sreejith Digital",
        description="Explore remote-first SEO consulting across Chennai, Bengaluru, Mumbai, Delhi NCR, Hyderabad, Kochi and Pune, with a scalable India location architecture.",
        main=main,
    )


def location_page(location: dict) -> None:
    path = f'/locations/{location["slug"]}/'
    service_schema = {
        "@type": "Service",
        "name": f'SEO consulting for {location["name"]}',
        "serviceType": "Local SEO Consulting",
        "description": location["description"],
        "provider": {"@id": BASE_URL + "/#organization"},
        "areaServed": location["name"],
        "url": BASE_URL + path,
    }
    main = f'''{page_hero(
        path=path,
        eyebrow="Location",
        title=f'SEO Consultant in {location["name"]}',
        lede=location["intro"],
        meta=["Remote-first", "Locally relevant research", "No physical office implied"],
    )}

<section class="section">
  <div class="container split-section">
    <div class="prose">
      <p class="lead">{e(location["intro"])}</p>
      <h2>Understanding the local search context</h2>
      <p>{e(location["market"])} The work starts by mapping those queries to pages with clearly different jobs, rather than producing a set of interchangeable city pages.</p>
      <h2>Delivered remotely, grounded in the market</h2>
      <p>Consulting, technical reviews, content planning, and reporting are delivered remotely. Location research shapes the architecture and page content; it does not imply a physical office in {e(location["name"])}.</p>
    </div>
    <aside class="aside-panel">
      <p class="eyebrow">Priority foundations</p>
      <h3>What the work focuses on</h3>
      {check_list(location["focus"])}
      <a class="btn btn--secondary btn--full" href="/services/local-seo/">See Local SEO <span aria-hidden="true">→</span></a>
    </aside>
  </div>
</section>

<section class="section section--surface">
  <div class="container">
    {section_header("Location page checklist", "Build for usefulness, not volume")}
    {check_list([
      "State the service area and the next action clearly",
      "Connect the page to relevant service and industry pages",
      "Include genuinely local context and trust signals",
      "Keep core business information consistent with profiles and listings",
      "Avoid duplicate copy with only the city name changed",
      "Measure local enquiries, calls, and profile actions separately",
    ])}
  </div>
</section>

<section class="section">
  <div class="container">
    {section_header("Relevant services", "Connect the location to the offer", "Location pages work best when they support a clearly defined service—not when they stand alone.", ("All services", "/services/"))}
    {card_grid([
        {"tag": "Service", "title": SERVICE_BY_SLUG[slug]["name"], "text": SERVICE_BY_SLUG[slug]["short"], "href": f"/services/{slug}/", "link_label": "View service"}
        for slug in ("local-seo", "technical-seo", "analytics-reporting")
    ], 3)}
  </div>
</section>

<section class="section section--surface">
  <div class="container">
    {section_header("Other locations", "Explore the wider architecture", "The same principles apply across each service area.", ("All locations", "/locations/"))}
    {card_grid([
        {"tag": "Location", "title": item["name"], "text": item["short"], "href": f'/locations/{item["slug"]}/', "link_label": "View location"}
        for item in LOCATIONS if item["slug"] != location["slug"]
    ][:3], 3)}
  </div>
</section>

{cta_section(f'Targeting {location["name"]}?', "Share the locations you genuinely serve and the current page structure. I will suggest a clean, scalable hierarchy.")}
'''
    write_page(
        path=path,
        title=f'SEO Consultant in {location["name"]} | Sreejith Digital',
        description=location["description"],
        main=main,
        schema_extra=[service_schema],
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
        title="Practical guides, not recycled advice",
        lede="Short, useful explanations of the decisions behind technical SEO, keyword strategy, local search, and measurement.",
        meta=["Guides", "Checklists", "Frameworks"],
    )}

<section class="section">
  <div class="container">
    {section_header("India-focused guides", "Start with a useful question", "Practical guides for Indian businesses evaluating SEO, local search, measurement and paid-versus-organic decisions.")}
    {card_grid(cards, 2)}
  </div>
</section>

{cta_section("Prefer a working session?", "Bring a current audit, dashboard, or page structure. A focused review is often faster than another article.")}
'''
    write_page(
        path="/resources/",
        title="SEO Resources India | Guides & Checklists",
        description="Practical SEO guides for Indian businesses on technical audits, consultant selection, pricing, local search, measurement and SEO versus Google Ads.",
        main=main,
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
        "headline": resource["name"],
        "description": resource["description"],
        "about": resource["category"],
        "datePublished": LAST_UPDATED,
        "dateModified": LAST_UPDATED,
        "author": {"@id": BASE_URL + "/#organization"},
        "publisher": {"@id": BASE_URL + "/#organization"},
        "mainEntityOfPage": BASE_URL + path,
        "inLanguage": "en",
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
      <p class="lead">{e(resource["intro"])}</p>
      {''.join(sections)}
      <div class="article-end"><span aria-hidden="true">✦</span><p>Written by <strong>{e(SITE_NAME)}</strong> · Practical SEO guidance for in-house teams.</p></div>
    </article>
    <aside class="article-aside">
      <div class="aside-panel aside-panel--sticky">
        <p class="eyebrow">On this page</p>
        <h3>Contents</h3>
        <ol class="toc">{''.join(toc)}</ol>
        <a class="btn btn--secondary btn--full" href="/contact/">Discuss this with me <span aria-hidden="true">→</span></a>
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

{cta_section("Want this applied to your site?", "A short review can turn the checklist into a prioritised, team-ready roadmap.")}
'''
    write_page(
        path=path,
        title=resource["name"],
        description=resource["description"],
        main=main,
        schema_extra=[article_schema],
        og_type="article",
    )


def contact_page() -> None:
    service_options = "".join(
        f'<option value="{e(item["name"])}">{e(item["name"])}</option>' for item in SERVICES
    )
    main = f'''{page_hero(
        path="/contact/",
        eyebrow="Contact",
        title="Tell me what you are trying to grow",
        lede="Share a little context and I will come back with the most useful next step. No sales script, no obligations, and no ranking promises.",
        meta=["Direct response", "Practical first step", "No tracking on this form"],
    )}

<section class="section">
  <div class="container contact-layout">
    <div class="contact-form-wrap">
      <div class="contact-form-head">
        <p class="eyebrow">Consultation enquiry</p>
        <h2>Start with the essentials</h2>
        <p>This static form opens your email app with the details filled in, so nothing is stored by this website before you choose to send.</p>
      </div>
      <form class="contact-form" data-contact-form data-contact-email="{e(CONTACT_EMAIL)}" action="mailto:{e(CONTACT_EMAIL)}" method="post" enctype="text/plain">
        <div class="form-grid">
          <div class="field">
            <label for="name">Name <span aria-hidden="true">*</span></label>
            <input id="name" name="name" type="text" autocomplete="name" required>
          </div>
          <div class="field">
            <label for="email">Work email <span aria-hidden="true">*</span></label>
            <input id="email" name="email" type="email" autocomplete="email" required>
          </div>
          <div class="field">
            <label for="company">Company</label>
            <input id="company" name="company" type="text" autocomplete="organization">
          </div>
          <div class="field">
            <label for="website">Website</label>
            <input id="website" name="website" type="url" placeholder="https://" autocomplete="url">
          </div>
          <div class="field">
            <label for="service">Area of interest</label>
            <select id="service" name="service">
              <option value="Not sure yet">Not sure yet</option>
              {service_options}
              <option value="Something else">Something else</option>
            </select>
          </div>
          <div class="field">
            <label for="timeline">Ideal timeline</label>
            <select id="timeline" name="timeline">
              <option value="As soon as practical">As soon as practical</option>
              <option value="This quarter">This quarter</option>
              <option value="Next quarter">Next quarter</option>
              <option value="Exploring only">Exploring only</option>
            </select>
          </div>
          <div class="field field--full">
            <label for="message">What would you like to improve? <span aria-hidden="true">*</span></label>
            <textarea id="message" name="message" rows="6" required placeholder="Current goal, what has been tried, and any known constraints."></textarea>
          </div>
        </div>
        <label class="checkbox-field">
          <input type="checkbox" name="consent" required>
          <span>I understand that submitting opens my email application and that my message will be sent to {e(CONTACT_EMAIL)}.</span>
        </label>
        <div class="form-actions">
          <button class="btn btn--primary" type="submit">Prepare enquiry <span aria-hidden="true">→</span></button>
          <p class="form-note">No analytics, advertising cookies, or third-party form service is used on this site.</p>
        </div>
        <p class="form-status" data-form-status role="status" aria-live="polite"></p>
      </form>
      <noscript><p class="form-note">JavaScript is disabled. Please use the direct email link on this page, or submit the form to open your email application.</p></noscript>
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
          <li><span>01</span><p><strong>Context</strong><br>Review the goal, current site, and constraints.</p></li>
          <li><span>02</span><p><strong>Reply</strong><br>Confirm fit and suggest the most useful next step.</p></li>
          <li><span>03</span><p><strong>Scope</strong><br>Agree on a focused scope only if there is a clear reason to proceed.</p></li>
        </ol>
      </div>
    </aside>
  </div>
</section>
'''
    write_page(
        path="/contact/",
        title="Contact an SEO Consultant in India | Sreejith Digital",
        description="Start a conversation with Sreejith Digital about SEO consulting, technical audits, local search, or a website project.",
        main=main,
    )


def privacy_page() -> None:
    main = f'''{page_hero(
        path="/privacy/",
        eyebrow="Legal",
        title="Privacy Policy",
        lede="A plain-language summary of how this static website handles information.",
        meta=[f"Last updated {LAST_UPDATED}"],
    )}

<section class="section">
  <div class="container prose-layout">
    <div class="prose">
      <p class="lead">This website is intentionally lightweight. It does not use analytics, advertising trackers, marketing cookies, or a third-party form service.</p>
      <h2>Information you choose to send</h2>
      <p>The contact page prepares an email in your own email application. The details you enter are not collected or stored by the website itself. Once you press send, your email provider and the recipient’s email provider process the message under their own policies.</p>
      <h2>Technical information</h2>
      <p>The hosting provider may process routine technical data such as IP addresses, request times, user agents, and requested URLs in order to deliver the site, maintain security, and diagnose abuse. This site does not ask for or use that data for advertising profiles.</p>
      <h2>Cookies and localStorage</h2>
      <p>The site does not set analytics or advertising cookies. The small amount of JavaScript used for navigation and the contact form does not store personal data in browser localStorage.</p>
      <h2>External links</h2>
      <p>Links to external services are not required to use this site. If third-party services are added in future, this policy should be updated before they are enabled.</p>
      <h2>Contact</h2>
      <p>Questions about this policy can be sent to <a href="mailto:{e(CONTACT_EMAIL)}">{e(CONTACT_EMAIL)}</a>.</p>
    </div>
    <aside class="aside-panel">
      <p class="eyebrow">In short</p>
      <h3>No tracking by default</h3>
      {check_list([
        "No analytics scripts",
        "No advertising pixels",
        "No marketing cookies",
        "No third-party form endpoint",
        "Contact starts in your email app",
      ])}
    </aside>
  </div>
</section>
'''
    write_page(
        path="/privacy/",
        title="Privacy Policy",
        description="How the Sreejith Digital static website handles contact details, technical logs, cookies, and external services.",
        main=main,
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
      <p class="lead">These terms cover this website only. The scope, deliverables, fees, timelines, and responsibilities for any consulting engagement are set out in a separate written agreement.</p>
      <h2>Informational content</h2>
      <p>Guides and service pages are provided for general information. They are not a guarantee of search rankings, traffic, revenue, or a specific commercial outcome. Search systems, competitors, and business conditions change.</p>
      <h2>No professional relationship by browsing</h2>
      <p>Reading this website or sending an initial enquiry does not create a consulting relationship. Work begins only when both parties agree to a defined scope in writing.</p>
      <h2>Intellectual property</h2>
      <p>Site copy, design, and original diagrams are provided for reading and sharing with attribution. You may link to these pages, but you may not republish them as your own or remove attribution.</p>
      <h2>Third-party services</h2>
      <p>Names of third-party products may appear for clarity. They remain the property of their respective owners and do not imply endorsement or partnership.</p>
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
        title="Terms of Use",
        description="Basic terms for using the Sreejith Digital website and informational resources.",
        main=main,
    )


def not_found_page() -> None:
    main = f'''<section class="section error-page">
  <div class="container">
    <p class="eyebrow eyebrow--pill">404 · Page not found</p>
    <h1>That URL has moved, or never had a page.</h1>
    <p class="page-hero__lede">Use the architecture below to find the right starting point.</p>
    <div class="error-actions">
      <a class="btn btn--primary" href="/">Return home <span aria-hidden="true">→</span></a>
      <a class="btn btn--secondary" href="/sitemap.xml">View sitemap</a>
    </div>
    {card_grid([
        {"tag": "Services", "title": "What I do", "text": "Explore the full service architecture.", "href": "/services/", "link_label": "Open services"},
        {"tag": "Locations", "title": "Where I work", "text": "Browse location-specific search guides.", "href": "/locations/", "link_label": "Open locations"},
        {"tag": "Resources", "title": "How I think", "text": "Read practical guides and checklists.", "href": "/resources/", "link_label": "Open resources"},
    ], 3)}
  </div>
</section>'''
    write_text(
        SITE_ROOT / "404.html",
        render_page(
            path="/404.html",
            title="Page Not Found",
            description="The requested page could not be found. Explore services, locations, and resources instead.",
            main=main,
            robots="noindex, follow",
        ),
    )


def sitemap_paths() -> list[str]:
    paths = [
        "/",
        "/about/",
        "/services/",
        "/industries/",
        "/locations/",
        "/resources/",
        "/contact/",
        "/privacy/",
        "/terms/",
    ]
    paths.extend(f'/services/{item["slug"]}/' for item in SERVICES)
    paths.extend(f'/industries/{item["slug"]}/' for item in INDUSTRIES)
    paths.extend(f'/locations/{item["slug"]}/' for item in LOCATIONS)
    paths.extend(f'/resources/{item["slug"]}/' for item in RESOURCES)
    return sorted(set(paths), key=lambda value: (value.count("/"), value))


def write_sitemap() -> None:
    entries = "".join(
        f'''  <url>
    <loc>{BASE_URL}{e(path)}</loc>
    <lastmod>{LAST_UPDATED}</lastmod>
    <changefreq>{"weekly" if path == "/" else "monthly"}</changefreq>
    <priority>{"1.0" if path == "/" else "0.7"}</priority>
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
        "homepage-title: SEO Consultant India | Technical & Local SEO – Sreejith Digital",
        "homepage-h1: Independent SEO Consultant in India Helping Businesses Grow Organically",
        "",
    ])
    write_text(SITE_ROOT / "version.txt", content)


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
    resources_hub()
    for resource in RESOURCES:
        resource_page(resource)
    contact_page()
    privacy_page()
    terms_page()
    not_found_page()
    write_sitemap()
    write_version_marker()
    print(f"Generated {len(sitemap_paths())} indexable pages plus 404.html, sitemap.xml and version.txt")


if __name__ == "__main__":
    main()
