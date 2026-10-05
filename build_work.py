"""Build the /work/<slug> case-study pages from STUDIES below.

Run: python3 build_work.py
Shared chrome (nav, footer, cookie banner, analytics, scripts) is copied from
b2b-marketing.html at build time, so it always matches the rest of the site.
Rerun after editing STUDIES or that page's chrome. Output: work/<slug>.html

Rules for STUDIES copy: no em dashes, US spelling, only claims we can source.
Use "What changed" only when there is a measured outcome.
DF and BLC stay anonymous (no names, links or screenshots) until the client
gives written permission.
"""
import html
import json
import os

SITE = "https://throughline.community"
SRC = open("b2b-marketing.html", encoding="utf-8").read()


def between(a, b):
    i = SRC.index(a)
    return SRC[i:SRC.index(b, i)]


BASE_CSS = between("    :root {", "    /* ── HERO (single column, centered) ── */")
FOOT_CSS = between("    /* FOOTER */", "    /* RESPONSIVE */")
NAV_RESP = """    @media (max-width: 1100px) { .nav-links { display: none; } }
    @media (max-width: 900px) { .nav { padding: 20px 36px; } }
    @media (max-width: 720px) {
      .nav { padding: 16px 24px; }
      .nav-logo-svg { height: 52px; }
      .site-footer { padding: 20px 24px; flex-direction: column; align-items: flex-start; }
    }
"""
MOBILE_CSS = between("    /* ── MOBILE NAV ── */", "  </style>")
GTAG = between("  <!-- Google tag (gtag.js) — Consent Mode v2 -->", "</head>")
NAV = (between('  <svg id="tlNav"', "  <!-- HERO -->").replace(' class="active" aria-current="page"', "")
       .replace('nav-trigger active', 'nav-trigger').replace('<a href="/work">', '<a href="/work" class="active">'))
FOOTER = between("  <!-- FOOTER -->", "  <script>")
SCRIPTS = between("    // Scroll reveal", "  </script>\n\n  <div class=\"cookie-banner\"")
COOKIE = SRC[SRC.index('  <div class="cookie-banner"'):SRC.index("</body>")]
FONTS = between('  <link rel="preconnect" href="https://fonts.googleapis.com">', '  <script type="application/ld+json">')

e = html.escape

B2B = ("Founder-led B2B with the same problem?", "See how we work with B2B brands", "/b2b-marketing")
EMERGING = ("Building something real that people are not finding yet?", "See how we work with emerging brands", "/for-emerging-brands")
ESTABLISHED = ("Has your business outgrown how the market sees it?", "See how we handle rebrands", "/for-established-brands")
SERVICES = ("Want this kind of thinking on your brand?", "See everything we do", "/services")


def img(slug, name, w, h, cap, alt):
    return (f"assets/work/{slug}/{name}.webp", w, h, cap, alt)


STUDIES = [
    {
        "slug": "payro-finance",
        "client": "Payro Finance",
        "title": "Payro Finance case study: LinkedIn strategy for a fintech",
        "description": "How Throughline Co. rebuilt a fintech's LinkedIn content around one buyer: followers up 118% and monthly click-to-apply from 12 to 161 in four months.",
        "dek": "We did not go viral. We got specific.",
        "meta": [("Who", "Payroll funding for small businesses"), ("Where", "McLean, Virginia"),
                 ("When", "December 2025 to April 2026"), ("What we did", "LinkedIn strategy, content, brand infrastructure")],
        "link": ("Client site", "https://payrofinance.com/"),
        "reframe": ("Write for someone who has made payroll on a Friday and is already thinking about the next one.",
                    "The brief every post was written to"),
        "sections": [
            ("The posts were written for the wrong reader.",
             ["Payro funds payroll for small businesses when cash-flow timing gets tight. Its LinkedIn sounded like most fintech: finance-speak for finance people, startup-speak for founders. The person who actually needs Payro is a small business owner looking at Friday's payroll.",
              "The easy alternative was to post more often and hope something landed. We did the opposite: picked one reader and rewrote the whole content strategy around what that person worries about."]),
            ("What we built", "built"),
            ("What changed", "results"),
        ],
        "built": [
            ("Content strategy", "Rebuilt around one buyer, a small business owner making payroll, in their words rather than the industry's."),
            ("LinkedIn content system", "Posts, carousels and timely pieces like the Groundhog Day post, all written to that same reader."),
            ("Brand infrastructure", "A consistent voice and visual approach so every post sounds like the same company."),
        ],
        "results": [("1,386 → 3,023", "LinkedIn followers, up 118%."), ("12 → 161", "Monthly click-to-apply.")],
        "results_note": "December 2025 to April 2026. Clicks grew faster than completed applications, so the next job is attracting the right reader, not just more of them.",
        "hero": img("payro-finance", "groundhog-post", 900, 1163, "The Groundhog Day post: a timely hook, written for the owner, not the finance team.", "Payro LinkedIn post of a groundhog in a shirt and tie doing payroll at a desk."),
        "hero_narrow": True,
        "gallery": [img("payro-finance", "instagram", 900, 1200, "The same voice carried across Payro's other channels.", "Payro Finance Instagram profile grid.")],
        "route": B2B,
    },
    {
        "slug": "josh-harris-media",
        "client": "Josh Harris Media",
        "title": "Josh Harris Media case study: B2B video strategy repositioning",
        "description": "How Throughline Co. repositioned a B2B video strategist to sell sales velocity, with a brand book, a new site and two AI sales tools in one month.",
        "dek": "Josh was selling video. His buyers wanted to walk into sales calls already trusted.",
        "meta": [("Who", "Video strategist for founder-led B2B companies"), ("Where", "Charlottesville, Virginia"),
                 ("When", "June 2026"), ("What we did", "Positioning, brand book, website, AI sales tools")],
        "link": ("Live site", "https://www.joshharrismedia.com/"),
        "reframe": ("Everyone is selling content volume. You're the only one positioned to sell sales velocity.", "From the strategy deck, June 1, 2026"),
        "sections": [
            ("The real problem was the pitch, not the video.",
             ["Josh makes excellent video for B2B founders. But his business was described the way most video businesses are: views, reach, content volume. Founders selling five-figure deals do not buy views. They buy shorter sales cycles.",
              "The obvious alternative was the one the whole category takes: make more content and point to the view counts. So before touching design, we rebuilt the argument. Who is the buyer, what do they lose today, and what does a video do for them before the first call even happens?"]),
            ("Everything we made pointed at one idea.", "built"),
            ("Halfway through, the audience changed. So did the copy.",
             ["Midway through the build, Josh widened his ideal client from B2B SaaS to every founder-led B2B company. Rather than patch the old copy, we went back to the research, rewrote the positioning for the wider audience, and rewrote the site to match. Same deadline."]),
            ("How it shipped", "results"),
        ],
        "built": [
            ("Strategy deck and update", "A 9-slide repositioning deck, then a 12-page update covering the ideal client, four messaging pillars and six service formats."),
            ("Brand book", "Positioning, a cultural read on B2B founders, a logo picked from three concepts, color, type and voice rules."),
            ("Website brief and copy", "A build brief with SEO targets and an analytics plan, plus a 23-page copy brief, rewritten after the audience change."),
            ("joshharrismedia.com", "Designed, written and built, live in production."),
            ("Two sales tools", "A Brand Audit that uses AI with live web search to show founders what buyers find about them, and a Revenue Leak Calculator."),
        ],
        "results": [
            ("10 days", "From first line of code (June 15) to the reviewed site with Josh's feedback applied (June 24)."),
            ("2 tools", "The AI Brand Audit and the Revenue Leak Calculator, both live in production."),
            ("1 pivot", "Audience widened mid-project. Research, positioning and copy were redone without moving the deadline."),
        ],
        "results_note": "We do not have traffic or lead data for this site yet, so we are not quoting any. These are delivery facts.",
        "hero": img("josh-harris-media", "site-home", 1440, 810, "joshharrismedia.com, live. The headline came straight out of the repositioning work.", "Josh Harris Media homepage with the headline: The sales call before the sales call."),
        "gallery": [
            img("josh-harris-media", "brand-audit", 1440, 900, "The Brand Audit: a founder enters a company name and gets a report on what buyers see.", "Brand Audit tool page asking what your brand signals before you speak."),
            img("josh-harris-media", "revenue-calculator", 1440, 900, "The Revenue Leak Calculator turns a close rate into the revenue a weak first impression costs.", "Revenue Leak Calculator page."),
        ],
        "voice": ("Working with Riya took a huge weight off my shoulders. She helped me make decisions I'd been putting off for weeks and somehow understood my vision even when I couldn't fully explain it. Halfway through, I completely changed directions, and instead of pushing back, she redid the research and copy to match. It was a pleasure working with her.",
                  "Josh Harris", "Founder, Josh Harris Media"),
        "excerpt": "Halfway through, I completely changed directions, and instead of pushing back, she redid the research and copy to match.",
        "route": B2B,
    },
    {
        "slug": "a-r-morris-jewelers",
        "client": "A.R. Morris Jewelers",
        "title": "A.R. Morris Jewelers case study: repositioning a family jeweler",
        "description": "How Throughline Co. resolved a 65-year jeweler's false choice between a tax-free pitch and a marketplace pitch, then prototyped a guided shopping journey.",
        "dek": "A 65-year jeweler, stuck choosing between two pitches that were never competing.",
        "meta": [("Who", "Family fine jeweler since 1962"), ("Where", "Greenville, Delaware"),
                 ("When", "June 2026 to now"), ("What we did", "Positioning, site audit, guided-shopping prototype")],
        "link": ("Client site", "https://www.armorrisjewelers.com/"),
        "reframe": ("Lead with permanence. Let price be a footnote.", "From the strategy deck, July 2026"),
        "sections": [
            ("Two good ideas, treated as a choice.",
             ["A.R. Morris was weighing two directions: lead with Delaware's tax-free savings, or reposition the store as a new marketplace to shop jewelry. They were being treated as competing options. They answer different questions. Tax-free is a value proposition. Marketplace is a channel decision.",
              "So the answer was not either one. Keep tax-free as quiet proof throughout the site, and make a guided, boutique-style experience the real answer to how people should shop."]),
            ("The site was saying the wrong thing first.",
             ["Our audit of the live site found the heritage claim repeated four times with two different founding years. On mobile, the very first icon a visitor saw was \"0% Sales Tax\". The store's strongest trust signal, that it rejects 9 in 10 diamonds, was buried. The fix was to lead with craft and permanence and let price support it."]),
            ("What we built", "built"),
            ("Where it stands", "results"),
        ],
        "built": [
            ("Opportunity deck", "An 11-page look at the customer, feature and loyalty ideas, a 60-day content calendar and a phased roadmap."),
            ("Strategy deck", "14 pages: cultural analysis, a gap assessment of the live site, a mobile audit, the guided journey and prioritized recommendations."),
            ("Working prototype", "A two-path landing page, a six-question quiz that explains its picks, live filters, ring sizing and inline financing."),
            ("Developer guide", "A five-stage build spec with about 16 analytics events, so the store can see which path converts within a month of launch."),
        ],
        "results": [
            ("2 decks", "25 pages of strategy, from opportunity to recommendations."),
            ("1 prototype", "A clickable guided-shopping journey, ready to build from."),
            ("In progress", "The guided journey is being built now. We will add results once it ships."),
        ],
        "results_note": "The prototype uses sample products and prices. It is not the store's live inventory.",
        "hero": img("a-r-morris-jewelers", "prototype-home", 1440, 1600, "The prototype's front door: two paths, one for people who know what they want and one for people who need help.", "A.R. Morris prototype with two paths: I know what I'm looking for, and Help me find something."),
        "gallery": [
            img("a-r-morris-jewelers", "quiz-results", 1440, 950, "Quiz results explain every pick, so a recommendation reads like advice, not an ad.", "Guided quiz results with reasons for each recommendation."),
            img("a-r-morris-jewelers", "detail-sizing", 1440, 950, "Product detail with a sizing helper and financing shown inline.", "Ring detail page with a sizing calculator."),
        ],
        "voice": ("For our website development and positioning, Riya goes so incredibly above and beyond what she needs to do. Her work is fully comprehensive to an extent I never would have been able to reach myself. She's ingrained in our business as if it were her own, fully invested in getting it right and having the creativity to come up with incredible ideas for our users to make our online experience special. What stands out most is how she masters the balance between catching the finest details through every link, text, and design, while never losing sight of the bigger picture.",
                  "Cole Morris", "Owner, A.R. Morris Jewelers"),
        "excerpt": "She's ingrained in our business as if it were her own.",
        "route": ESTABLISHED,
    },
    {
        "slug": "sanjay-mohan-mittal",
        "client": "Sañjay Mohan Mittal",
        "title": "Sañjay Mohan Mittal case study: author platform and academic outreach",
        "description": "How Throughline Co. fixed a scholarly ebook that broke on Kindle, built the author's platform, and ran outreach that drew a professor's reply in 37 minutes.",
        "dek": "An ancient text, an ebook that broke on Kindle, and readers who did not know the book existed.",
        "meta": [("Who", "Author of a three-volume critical edition of the Manusmṛti"), ("Where", "Bayonne, New Jersey"),
                 ("When", "June to October 2026"), ("What we did", "Ebook fix, author platform, academic outreach")],
        "link": ("Live site", "https://www.sanjaymohanmittal.com/"),
        "reframe": ("Remove unconfirmed claims entirely. Don't soften them or hold them as placeholders.", "Standing rule for the project, August 2026"),
        "sections": [
            ("A serious book needed a serious first impression.",
             ["The trilogy separates the original Manusmṛti from verses added later. Its readers are scholars, students and temple communities, people who check sources. The Sanskrit diacritics and Devanagari were breaking on Kindle, and there was no single place to understand the work or buy it.",
              "The alternative most authors take is to list the book and wait. We fixed the book first, then built a home for it, then went to the readers directly."]),
            ("Credibility was the design brief.",
             ["Every claim on the site was checked against a source. Where something could not be confirmed, it came out rather than being softened. That meant removing an unconfirmed claim in four places, and correcting a price and a verse citation."]),
            ("What we built", "built"),
            ("What changed", "results"),
        ],
        "built": [
            ("Ebook fix", "Diacritic and Devanagari rendering, encoding and file structure, so the text reads correctly on Kindle."),
            ("Author platform", "A five-chapter site where every page leads to the trilogy, with buy links for every format."),
            ("Identity", "A logo system and social preview images in light and dark."),
            ("Academic outreach", "Personal first emails to professors, libraries, temples and press, with follow-ups and a reply playbook."),
        ],
        "results": [
            ("37 minutes", "From the first outreach email to the first reply from a university professor."),
            ("1 library", "A university library is reviewing the full trilogy for its collection, after its selector called it an important work to add."),
            ("1 review copy", "Shipped to a religious studies professor who asked for it."),
        ],
        "results_note": "Outreach began September 21, 2026. The library purchase is still pending. We do not have sales data, so we are not quoting any.",
        "hero": img("sanjay-mohan-mittal", "site-home", 1440, 900, "sanjaymohanmittal.com, live. Five chapters, one destination: the trilogy.", "Sañjay Mohan Mittal author site opening on a havan fire with the heading: What was offered, and what remains."),
        "gallery": [img("sanjay-mohan-mittal", "cover-main", 420, 630, "Ancient Wisdom for the Modern World, the main volume.", "Cover of the main volume of the Manusmṛti trilogy.")],
        "gallery_narrow": True,
        "route": EMERGING,
    },
    {
        "slug": "white-ash-glass",
        "client": "White Ash Glass Studio",
        "title": "White Ash Glass Studio case study: brand and website for a glass artist",
        "description": "How Throughline Co. took a glass studio in the Ontario woods from no web presence to a brand book and a live seven-page site, starting from cultural research.",
        "dek": "A glass artist with a studio in the woods and no digital presence at all.",
        "meta": [("Who", "Community glass studio and bench-torch artist"), ("Where", "Brighton, Ontario"),
                 ("When", "June to August 2026"), ("What we did", "Cultural research, brand book, website")],
        "link": ("Live site", "https://www.whiteashglass.com/"),
        "reframe": ("This community resists being sold to. The moment a website feels like a funnel, they disengage.", "From the brand book, July 2026"),
        "sections": [
            ("We started with the town, not the logo.",
             ["White Ash had real craft and nothing online: no website, and no reviews or hours on Google. Before any design, we studied the place: Brighton, Presqu'ile and the Prince Edward County corridor, how locals talk, what they trust, and what makes them tune out.",
              "That research set the rules. No pop-ups. No funnel. Every call to action reads like an invitation to come see the studio, never a push to buy."]),
            ("What we built", "built"),
            ("How it shipped", "results"),
        ],
        "built": [
            ("Cultural and language research", "Local values and behaviors, words to use and words to avoid, tonal principles and tagline options."),
            ("Brand book", "21 pages: story, positioning, six audiences, the Tree of Life logo, color, type, voice, photography and print."),
            ("whiteashglass.com", "Seven pages: classes, experiences, gallery, the studio and glass, the founder and contact, with a working contact form."),
            ("Print", "A two-tier business card system, brochure and signage direction."),
        ],
        "results": [
            ("0 → 1", "From no web presence to a live site with classes, experiences and a gallery."),
            ("1 month", "From finished brand book (July 16) to the refined live site (August 17)."),
            ("0 pop-ups", "A deliberate choice, straight from the research."),
        ],
        "results_note": "The site does not have analytics set up yet, so we are not quoting traffic.",
        "hero": img("white-ash-glass", "site-home", 1440, 900, "whiteashglass.com, live. The path to the studio, then one line: Made by fire. Built for community.", "White Ash Glass Studio homepage showing a forest path and the line Made by fire, built for community."),
        "gallery": [
            img("white-ash-glass", "classes", 1440, 900, "Classes are written as an invitation: come curious, leave with something real.", "White Ash classes page."),
            img("white-ash-glass", "gallery", 1440, 900, "The gallery lets the glass do the talking.", "White Ash gallery of glass pieces in the flame."),
        ],
        "route": EMERGING,
    },
    {
        "slug": "df",
        "client": "DF",
        "title": "DF case study: B2B website, buyer qualification and AI search",
        "description": "How Throughline Co. built a 16-page B2B site for an email marketing company, with a buyer-qualification quiz, AI-search structure and Lighthouse 99 to 100.",
        "dek": "A B2B email marketing company needed a site that qualifies buyers before the first call.",
        "meta": [("Who", "Done-for-you email marketing for e-commerce brands"), ("Where", "United States"),
                 ("When", "August 2026 to now"), ("What we did", "Website, buyer qualification, AI search, operations")],
        "reframe": ("Most visitors were not a fit yet, and the site had nothing to tell them.", "From our project log, September 2026"),
        "sections": [
            ("A sales team spending calls on the wrong buyers.",
             ["DF sells a done-for-you email system to product brands. Not every brand is ready for it, and the old approach was to find that out on a sales call. The alternative most B2B sites take is a contact form and hope.",
              "We built the site to do the sorting first: tell visitors who it is for, who it is not for, and where to start if they are not ready yet."]),
            ("What we built", "built"),
            ("What changed", "results"),
        ],
        "built": [
            ("A 16-page site", "Designed, written and built from the first commit on August 19, live on its own domain."),
            ("Fit Check", "A short branching quiz that tells a visitor whether they are a fit and what to start with, before they book."),
            ("AI search readiness", "Every page prerendered so AI crawlers can read it, with structured data for the company, services, FAQs and podcast."),
            ("Accessibility", "An accessibility statement, audits on every page, and fixes for every contrast and text-size issue found."),
            ("Operations", "A policies and procedures system, a file-naming protocol, a daily work log and weekly reporting."),
        ],
        "results": [
            ("99 / 100 / 100", "Lighthouse performance, accessibility and SEO on desktop, re-measured October 4, 2026."),
            ("−28%", "Homepage weight, 860 KB to 616 KB, in one speed pass."),
            ("0 errors", "Structured data validation. All 60 site links checked and working."),
        ],
        "results_note": "These are technical measures. The client's results are not ours to publish. The company name, link and screenshots will be added once the client signs off.",
        "route": B2B,
    },
    {
        "slug": "blc",
        "client": "BLC",
        "title": "BLC case study: relaunching a cigar community site under tobacco law",
        "description": "How Throughline Co. rebuilt a cigar community site in about two weeks: 791 glossary terms moved, and Canada's tobacco advertising rules built in.",
        "dek": "A cigar community on an aging WordPress site, in a category where the law limits what you can say.",
        "meta": [("Who", "Cigar content and community platform"), ("Where", "Canada"),
                 ("When", "September 2026"), ("What we did", "Website rebuild, content migration, compliance, social")],
        "reframe": ("Compliance was a design constraint from day one, not a review at the end.", "How we approached the build"),
        "sections": [
            ("A big library, an old site, and strict rules.",
             ["BLC is a free platform for cigar reviews, education, a podcast and a community. It sells nothing. Its content lived on an aging WordPress site, and in Canada, tobacco law limits what any cigar brand can show and say.",
              "The alternative was a fresh coat of paint on the old site. Instead we rebuilt it, moved every piece of content across, and wrote the legal limits into the content rules before a single page was published."]),
            ("What we built", "built"),
            ("What changed", "results"),
        ],
        "built": [
            ("Rebuilt site", "Reviews, education, a cigar database, events, a community hub, search and filters, behind an age gate."),
            ("Content migration", "18 articles, 7 guides, 28 new releases, 117 community photos and 791 glossary terms parsed from the old site by script."),
            ("Compliance", "Content guardrails written against the tobacco act, AI-image disclosure, and an audit of 86 images for identifiable people."),
            ("Voice system", "A founder voice guide built from about 46,000 words of real transcripts, across story, podcast and written registers."),
            ("Social and podcast", "Instagram highlight icons, a podcast intro and outro, and an episode thumbnail kit."),
        ],
        "results": [
            ("About 2 weeks", "From first commit (September 11) to the new site live on its own domain, replacing WordPress."),
            ("149 pages", "Indexed in the new sitemap."),
            ("−79%", "Gallery image weight, 99.4 MB down to 20.5 MB."),
        ],
        "results_note": "The brand name, link and screenshots will be added once the client signs off.",
        "route": EMERGING,
    },
    {
        "slug": "polaris-campus",
        "client": "Polaris Campus",
        "title": "Polaris Campus case study: brand audit and marketing roadmap",
        "description": "A brand audit and marketing roadmap for an Indian tech undergraduate program, aimed at the moment students start doubting a degree abroad.",
        "dek": "Students were weighing a degree abroad. The moment to reach them opens and closes with visa news.",
        "meta": [("Who", "Undergraduate tech and engineering program"), ("Where", "India"),
                 ("When", "September 2026"), ("What we did", "Brand audit and marketing roadmap")],
        "reframe": ("Polaris doesn't need to compete with going abroad. It needs to prove it already delivers what abroad was always the means to, only faster and more honestly.", "From the marketing roadmap, September 2026"),
        "sections": [
            ("The competition is a plane ticket.",
             ["Polaris's real competitor is not another college. It is the plan to study in the US, the UK, Canada or Australia. Our audit found that doubt about that plan clusters around each country's visa news, so the roadmap is built around those moments rather than a generic admissions calendar.",
              "With no graduates yet, the brand cannot oversell anyone. So the audit made that a strength: radical transparency as the position."]),
            ("What we built", "built"),
            ("Where it stands", "results"),
        ],
        "built": [
            ("Brand audit", "Positioning against the real alternatives, a competitive map, and separate messages for students and parents."),
            ("Marketing roadmap", "A seasonal plan tied to visa cycles, offline and online channels, partnerships and a referral idea."),
            ("Two working prototypes", "A visa readiness scorecard and a Plan B calculator, built to show the ideas in action."),
            ("90-day and 12-month plans", "Who runs what, in what order, and how to measure it."),
        ],
        "results": [
            ("Delivered", "The brand audit and roadmap, with both prototypes."),
            ("Pre-launch", "Nothing has gone to market yet, so there are no results to report."),
        ],
        "route": SERVICES,
    },
    {
        "slug": "georgetown-ombuds",
        "short": "Georgetown Ombuds",
        "client": "Georgetown University Student Ombuds",
        "title": "Georgetown Student Ombuds case study: brand refresh and campaigns",
        "description": "How a brand refresh and campus campaigns for Georgetown University's Office of the Student Ombuds grew website traffic 40% and student visits 70%.",
        "dek": "A campus office built to help students, which only works if students know it exists.",
        "meta": [("Who", "Office of the Student Ombuds, Georgetown University"), ("Where", "Washington, DC"),
                 ("When", "September 2023 to July 2025"), ("What we did", "Brand refresh, DEI communications, campaigns")],
        "reframe": ("Visibility is the service. A student who has never heard of the office cannot use it.", "How we framed the work"),
        "sections": [
            ("A good service that students walked past.",
             ["The ombuds office gives students a confidential, neutral place to work through problems. But it was easy to miss, and the alternative for most students was simply not asking for help."]),
            ("What we built", "built"),
            ("What changed", "results"),
        ],
        "built": [
            ("Brand refresh", "A clearer identity and voice for the office, built from scratch."),
            ("DEI communications", "Messaging and materials that speak to every part of the student body."),
            ("Campaigns", "Campus activations with event collateral, including the student action figure campaign and postcards."),
        ],
        "results": [("+40%", "Website traffic."), ("+70%", "Student visits to the ombuds website and office after outreach began."), ("500+", "Students reached per campaign activation.")],
        "results_note": "September 2023 to July 2025.",
        "hero": img("georgetown-ombuds", "postcard", 1200, 800, "Campaign postcard for the office.", "Georgetown University postcard: If you want to go fast, go alone. If you want to go far, go together."),
        "gallery": [
            img("georgetown-ombuds", "action-figure", 900, 1123, "The student action figure campaign.", "Georgetown student action figure campaign graphic."),
            img("georgetown-ombuds", "event", 900, 1200, "Tabling on campus with the refreshed materials.", "Georgetown Student Ombuds event table on campus."),
        ],
        "route": SERVICES,
    },
    {
        "slug": "dyslex-aid",
        "client": "Dyslex-Aid",
        "title": "Dyslex-Aid: founder project, from idea to classroom pilot",
        "description": "Riya Mittal's founder project: an AI reading tool for children with dyslexia, taken from idea to a $6,500 pitch win and pilots in two schools.",
        "dek": "I built this one. An AI reading tool for children with dyslexia, from idea to real classrooms.",
        "meta": [("Who", "AI reading support for children with dyslexia"), ("Where", "Washington, DC"),
                 ("When", "April 2023 to May 2025"), ("What we did", "Product, go-to-market, pitch and pilot")],
        "reframe": ("This is where I learned what it costs when the right people cannot find something that matters.", "Riya Mittal, founder"),
        "sections": [
            ("Why this one is personal.",
             ["I was diagnosed with dyslexia at 21, after being told I was not suited for academia. Dyslex-Aid came out of that: personalized reading support for children who learn the way I do.",
              "Building it taught me the same lesson I now bring to every client. A good product is not enough. The right people have to find it, understand it, and trust it."]),
            ("What changed", "results"),
        ],
        "results": [("$6,500", "Won at a global pitch competition."), ("2 schools", "Piloted in real K-12 classrooms."), ("Featured", "In Georgetown University CCT's Disability Pride Month publication.")],
        "results_note": "April 2023 to May 2025.",
        "hero": img("dyslex-aid", "pitch-cheque", 1000, 666, "The pitch competition win.", "Riya Mittal holding the $6,500 Dyslex-Aid pitch competition cheque."),
        "gallery": [img("dyslex-aid", "cct-article", 1600, 1000, "Featured by Georgetown's Communication, Culture and Technology program.", "Georgetown CCT article about Riya Mittal and Dyslex-Aid.")],
        "route": ("Want to know who is behind the work?", "Read the founder story", "/about"),
    },
    {
        "slug": "wild-foundation",
        "client": "Wild Foundation",
        "title": "Wild Foundation: communications proposal for a conservation nonprofit",
        "description": "A proposal for a 50-year conservation nonprofit: a redesigned donor email, social strategy, a Shenandoah campaign and a data story.",
        "dek": "Fifty years of conservation impact. A digital presence that was not keeping up.",
        "meta": [("Who", "Conservation nonprofit"), ("Where", "Virginia"),
                 ("When", "2026, proposal"), ("What we did", "Communications proposal and campaign design")],
        "reframe": ("They had the story. What they did not have was a way for people to find it, understand it, and act on it.", "How we framed the proposal"),
        "sections": [
            ("The story was there. The setup was not.",
             ["Wild Foundation had fifty years of work to talk about. What they did not have was a communications setup that let people find it, understand it, and act on it. We built a proposal for what that could look like."]),
            ("What we proposed", "built"),
            ("Where it stands", "results"),
        ],
        "built": [
            ("Donor email", "A redesigned donor email."),
            ("Social strategy", "A plan for what to post, where, and why."),
            ("Shenandoah campaign", "A six-slide campaign, designed end to end."),
            ("AI bot and data story", "An AI bot designed to make the website a real resource, and a data story that turns conservation research into content people share."),
        ],
        "results": [("Proposal", "Strategic spec work. Nothing has been deployed yet, and we are in conversation about next steps.")],
        "hero": img("wild-foundation", "shenandoah-01", 1080, 1350, "Shenandoah campaign, slide one.", "Shenandoah campaign slide one."),
        "hero_narrow": True,
        "gallery": [
            img("wild-foundation", "shenandoah-02", 1080, 1350, "Shenandoah campaign, slide two.", "Shenandoah campaign slide two."),
            img("wild-foundation", "donor-email", 1160, 1128, "The redesigned donor email, as proposed.", "Proposed Wild Foundation donor email design."),
        ],
        "route": SERVICES,
    },
]


def render(i, s):
    nxt = STUDIES[(i + 1) % len(STUDIES)]
    url = f"{SITE}/work/{s['slug']}"
    page_title = f"{s.get('short', s['client'])} Case Study | Throughline Co."
    image = f"{SITE}/{s['hero'][0]}" if s.get("hero") else f"{SITE}/og-image.png"
    about = {"@type": "Organization", "name": s["client"]}
    if s.get("link"):
        about["url"] = s["link"][1]
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Article", "headline": s["title"], "description": s["description"], "url": url, "image": image,
             "author": {"@id": f"{SITE}/#organization"}, "publisher": {"@id": f"{SITE}/#organization"}, "about": about},
            {"@type": "Organization", "@id": f"{SITE}/#organization", "name": "Throughline Co.", "url": f"{SITE}/",
             "logo": f"{SITE}/favicon.svg"},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": "Work", "item": f"{SITE}/work"},
                {"@type": "ListItem", "position": 3, "name": s["client"], "item": url}]},
        ],
    }

    def shot(src, w, h, cap, alt, cls="", eager=False):
        load = 'fetchpriority="high"' if eager else 'loading="lazy"'
        return (f'<figure class="study-shot {cls} reveal"><img src="/{src}" width="{w}" height="{h}" alt="{e(alt)}" {load} decoding="async">'
                f'<figcaption>{e(cap)}</figcaption></figure>')

    body = []
    for heading, content in s["sections"]:
        if content == "built":
            inner = '<ul class="study-list">' + "".join(f"<li><strong>{e(a)}</strong><span>{e(b)}</span></li>" for a, b in s["built"]) + "</ul>"
        elif content == "results":
            inner = '<ul class="study-results">' + "".join(f"<li><b>{e(a)}</b><span>{e(b)}</span></li>" for a, b in s["results"]) + "</ul>"
            if s.get("results_note"):
                inner += f'<p class="study-note">{e(s["results_note"])}</p>'
        else:
            inner = "".join(f"<p>{e(p)}</p>" for p in content)
        body.append(f'<section class="study-section reveal"><h2>{e(heading)}</h2><div class="study-copy">{inner}</div></section>')

    meta = "".join(f"<div><dt>{e(a)}</dt><dd>{e(b)}</dd></div>" for a, b in s["meta"])
    if s.get("link"):
        label, href = s["link"]
        host = href.split("//")[1].strip("/").removeprefix("www.")
        meta += (f'<div><dt>{e(label)}</dt><dd><a class="study-live" href="{e(href)}" target="_blank" rel="noopener">'
                 f'{e(host)} <span aria-hidden="true">↗</span><span class="visually-hidden"> (opens in a new tab)</span></a></dd></div>')

    lede = f'<blockquote class="study-quote"><p>{e(s["reframe"][0])}</p><cite>{e(s["reframe"][1])}</cite></blockquote>'
    if s.get("excerpt"):
        lede += f'<p class="study-excerpt">“{e(s["excerpt"])}”<span>{e(s["voice"][1])}, {e(s["voice"][2])}</span></p>'

    hero = ""
    if s.get("hero"):
        hero = f'<div class="study-hero{" narrow" if s.get("hero_narrow") else ""}">{shot(*s["hero"], eager=True)}</div>'
    gallery = ""
    if s.get("gallery"):
        gallery = f'<div class="study-gallery{" narrow" if s.get("gallery_narrow") else ""}">' + "".join(shot(*g) for g in s["gallery"]) + "</div>"
    voice = ""
    if s.get("voice"):
        q, name, role = s["voice"]
        voice = f'<section class="study-voice"><blockquote class="reveal"><p>{e(q)}</p><cite><b>{e(name)}</b>, {e(role)}</cite></blockquote></section>'
    ask, link_text, link_href = s["route"]

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{e(page_title)}</title>
  <link rel="canonical" href="{url}">
  <meta name="description" content="{e(s['description'])}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{e(page_title)}">
  <meta property="og:description" content="{e(s['description'])}">
  <meta property="og:image" content="{image}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{e(page_title)}">
  <meta name="twitter:description" content="{e(s['description'])}">
  <meta name="twitter:image" content="{image}">
{FONTS}  <script type="application/ld+json">
{json.dumps(ld, indent=2, ensure_ascii=False)}
  </script>
  <style>
{BASE_CSS}{FOOT_CSS}{NAV_RESP}{MOBILE_CSS}  </style>
  <link rel="stylesheet" href="/assets/site.css">
{GTAG}</head>
<body class="study">

{NAV}
  <main>
    <header class="study-head">
      <a class="study-back reveal" href="/work"><span aria-hidden="true">←</span> All work</a>
      <h1 class="study-title reveal">{e(s['client'])}</h1>
      <p class="study-dek reveal">{e(s['dek'])}</p>
      <div class="study-lede reveal">{lede}</div>
      <dl class="study-meta reveal">{meta}</dl>
    </header>

    {hero}

    <div class="study-body">
      {''.join(body)}
    </div>

    <aside class="study-route reveal" aria-label="Next step">
      <p>{e(ask)} <a href="{link_href}">{e(link_text)} <span aria-hidden="true">→</span></a></p>
      <a href="/contact" class="btn-terra">Book a free 30-min call</a>
    </aside>

    {gallery}

    {voice}

    <nav class="study-next" aria-label="More work">
      <a class="study-next-link" href="/work/{nxt['slug']}"><small>Next case study</small><span>{e(nxt['client'])} <span aria-hidden="true">→</span></span></a>
      <a href="/contact" class="btn-terra">Book a discovery call</a>
    </nav>
  </main>

{FOOTER}
  <script>
{SCRIPTS}  </script>

{COOKIE}  <script src="/assets/site.js" defer></script>
</body>
</html>
"""


if __name__ == "__main__":
    os.makedirs("work", exist_ok=True)
    for i, s in enumerate(STUDIES):
        path = f"work/{s['slug']}.html"
        open(path, "w", encoding="utf-8").write(render(i, s))
        print("wrote", path)
