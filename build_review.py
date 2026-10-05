"""Private client-review pages for the DF and BLC case studies (one page each).
Run: python3 build_review.py  ->  work/review-df-4e8b1d.html, work/review-blc-7c2f93.html
Unlinked, noindex, not in the sitemap. Delete each once the client has replied.
Story copy lives here. Facts come from the project work log (The Bridge) and live-site checks.
People are described by role only until the founders approve naming."""
import html
import re
import build_work as bw

e = html.escape
_i, _s = next((i, s) for i, s in enumerate(bw.STUDIES) if s["slug"] == "df")
BASE = bw.render(_i, _s)  # reuse the shared page chrome (head, nav, footer, scripts)


def fig(src, w, h, cap, alt):
    return (f'<figure class="study-shot"><img src="/assets/work/{src}.webp" width="{w}" height="{h}" alt="{e(alt)}" '
            f'loading="lazy" decoding="async"><figcaption>{e(cap)}</figcaption></figure>')


def pair(a, b):
    return f'<div class="rv-pair">{a}{b}</div>'


STORIES = {
"df": dict(
    token="4e8b1d", name="DF",
    dek="A done-for-you email company whose homepage left two prospects asking what it actually did.",
    quote=("Most visitors were not a fit yet, and the site had nothing to tell them.", "From our project log, September 2026"),
    meta=[("Who", "Done-for-you email marketing for product brands"), ("Where", "United States"),
          ("When", "August 2026 to now"), ("What we did", "Website, buyer qualification, AI search, speed, accessibility, operations")],
    chapters=[
        ("Two emails from people who did not understand the headline.", [
            "In early September, two prospects wrote to DF to ask what it actually did. The homepage promised “a complete revenue-generating system” and never said the word email.",
            "The fix was small and specific: one word, EMAIL, in orange, and a short list under it of what DF does. Getting the list right took three tries. The first version wrapped badly in the middle of a label. The second, a plain paragraph, was easier to read and harder to skim. The third was a fixed grid of chips that reads in two seconds.",
            "The lesson was the one we keep relearning. A visitor will not work out what you sell. They will leave and tell nobody why.",
        ], fig("df/home", 1280, 720, "DF’s homepage today. The first thing a visitor now learns is that this is about email.", "DF homepage with the headline “You own the inbox. We make it pay.”")),
        ("Selling to the right buyer is a filter, not a funnel.", [
            "DF’s best-fit brand is specific, and most of the people landing on the site were not that brand yet. The old way to find out was a sales call. We built a page called Fit Check, headed “Who we’re for. And who we’re not.”",
            "It began as a 14-point list of who is and is not a fit. We rebuilt it as a short branching quiz, three to five questions depending on the path, that works out a next step on the spot. For brands that are not ready, the next step is a smaller product, not a closed door.",
            "One decision mattered more than the design. The quiz drew its six outcomes with JavaScript, which hid them from search engines and AI crawlers. We flagged the tradeoff to the co-founder instead of settling it quietly, then put the six outcomes back as readable text.",
            "We also changed the main button from “See if you qualify” to “Apply to work with DF.” Qualify reads like a hurdle. Apply reads like a choice.",
        ], fig("df/fit-check", 1280, 720, "The Fit Check, step one of the quiz.", "DF Fit Check page: Who we’re for. And who we’re not.")),
        ("“Yes, you have AI. So does everyone else’s inbox.”", [
            "Every sophisticated buyer asks why they cannot just use AI themselves. The co-founder had the best possible answer: the same email, written once by generic AI and once by AI directed with a brand’s own research.",
            "We turned that into a section with a draggable dial that slides between the two versions. It is the one place on the site where the visitor does the comparing instead of reading a claim.",
        ], None),
        ("Making the site readable by machines.", [
            "To an AI crawler, almost every page on the site was empty. A plain request, with no JavaScript, returned a blank shell with none of DF’s services, pricing or copy in it. Search engines and AI assistants read the web that way.",
            "We added a step to the build that records each page as a real browser renders it and writes that content into the page itself. We then checked it the way a crawler would, and every page came back with real, correctly titled content.",
            "Structured data came next: the company, the website, breadcrumbs, 28 FAQ answers and the podcast series, all validating with zero errors. The company’s legal facts came from the co-founder, who confirmed them one by one.",
            "Earlier, on September 2, we found every page’s share and search information pointing to an old preview address instead of dragon.fish. That kind of bug quietly costs search visibility for months. It was fixed the day we found it.",
        ], None),
        ("Measured, not assumed.", [
            "Before touching anything we measured all 15 live pages. Performance scores ran from 45 to 72. The biggest cost was not DF’s code. A bot-detection script added by the hosting layer used 1.5 to 4.5 seconds of processor time per page. DF’s own code used under 100 milliseconds.",
            "We tried splitting the code by page. It made the homepage slower, so we undid it instead of keeping complexity that did not pay. What worked was boring: two oversized images. The homepage dropped from 860 KB to 616 KB.",
            "Accessibility got the same treatment. Automated checks against WCAG 2.1 AA on every page and the calculator, every link checked (60, all working), and 36 low-contrast uses of gray text fixed once, in the theme, so the hierarchy survived.",
            "On October 4 the desktop scores were 99 for performance, 100 for accessibility and 100 for SEO. Best practices sits at 81, and the whole gap is that bot-detection script. DF’s team can switch it off in their hosting settings.",
        ], None),
        ("The operating system behind the site.", [
            "A site is only as good as the habits around it. We wrote DF’s file-naming protocol (a DF prefix, 16 department codes, a three-digit sequence), a policy for onboarding and offboarding contractors, a daily work log and a weekly status email.",
            "A naming skill now standardizes a document’s name when it is uploaded, so nobody has to remember the rule.",
        ], None),
        ("Things we tried and changed our minds on.", [
            "We built a chatbot on the site’s own hosting, first matching questions to the FAQ, then answering with Claude. On the day it went live, our own testing found four questions it answered badly, including “how do you work.” We wrote a regression suite so the same bug could not come back. It stood at 56 tests on October 1.",
            "On October 2, at the co-founder’s call, we switched the chatbot off behind a one-line setting. The code stays, so it can return when it is ready.",
            "Marketplace capture, a product DF is rebuilding, is greyed out wherever it appears, with an “under construction” note. It is neither deleted nor oversold.",
        ], None),
    ],
    results=[("99 / 100 / 100", "Lighthouse performance, accessibility and SEO on desktop, measured October 4, 2026."),
             ("−28%", "Homepage weight, 860 KB to 616 KB, in one speed pass."),
             ("0 errors", "Structured data validation across 28 FAQ answers and every page."),
             ("60 of 60", "Links checked and working.")],
    note="These are delivery measures. DF’s own results, such as revenue or reply rates, are not ours to publish.",
    still_open=["Marketplace capture is being rebuilt and is greyed out until then.",
                "The blog is still in progress, so it is kept out of the search sitemap on purpose.",
                "The chatbot is switched off. The code is ready to return.",
                "Best practices stays at 81 until the hosting bot-detection setting is turned off."],
    check=["DF is described as a done-for-you email marketing company for product brands.",
           "The story of the homepage headline (two prospects confused) is accurate and fine to tell.",
           "The Fit Check and the “Apply to work with DF” button are described correctly.",
           "The speed and accessibility numbers: 99, 100, 100 (desktop, October 4, 2026) and 860 KB to 616 KB.",
           "We may mention the chatbot and that it was switched off.",
           "DF’s name, link and the screenshots on this page can appear on our public Work page."],
),
"blc": dict(
    token="7c2f93", name="BLC",
    dek="A free cigar community built around a blindfold, and a country where the law decides what a cigar site may say.",
    quote=("Compliance was a design constraint from day one, not a review at the end.", "How we approached the build"),
    meta=[("Who", "Cigar reviews, education and community platform"), ("Where", "Canada"),
          ("When", "September 2026 to now"), ("What we did", "Rebuild, compliance, founder voice, content migration, handover")],
    chapters=[
        ("A club named after a blindfold.", [
            "BLC runs on one idea: judge the cigar, not the label. Its founder has smoked cigars for forty years and, by his own telling, was not a fan of the first five. Today BLC is a free community with honest reviews, a podcast, a glossary of 791 terms and informal meetups in city lounges. It sells nothing. No cigars, no memberships.",
            "The old site had grown one page at a time, and it showed. It did a great deal, with a search bar, a chat bubble, poster-weight type and a crowded menu, and the calm, curious tone of the brand was hard to find in it. The job was to make the site sound like the person.",
        ], pair(fig("blc/old-home", 1280, 679, "The old site.", "BLC’s previous website home page"),
                fig("blc/new-home", 1280, 720, "The new site, past the age gate.", "BLC’s new website home page: Some cigars age well. Most of us don’t."))),
        ("We started with the law, and got it wrong first.", [
            "In Canada, tobacco law limits what any cigar brand can show and say. On day four we researched the rules and wrote a first set of content guardrails. We assumed the strictest reading: that even review and community content could count as promotion. So we banned purchase recommendations and lifestyle framing outright.",
            "Three days later the founder shared the compliance review he had already commissioned. It read the rule differently: unpaid commentary is not promotion, as long as no money or favors flow from a cigar maker or retailer. We threw out version one and rebuilt the guardrails around the review’s own four fences: no payment from makers or retailers, no links to cigar sellers, no cigar giveaways, and the same standard across every channel.",
            "Two of our bans became style defaults, because the review confirmed they were lawful. Five questions were still open, so we wrote them down for the founder’s counsel instead of guessing.",
            "The same care shows up in small places. The exact 21+ notice sits in the footer. An audit of all 86 article images found 34 with a person as the focal subject, and each now carries an AI-generated image label. One photo flagged as unlicensed came off the site.",
        ], None),
        ("Sounding like him, without faking it.", [
            "BLC’s voice is one man’s voice. He says “so,” “now,” “you know” and “anyways.” He never says “delve” or “leverage.” To write in that voice without inventing a character, we read six transcripts, about 46,000 words, and pulled out the founder’s own lines: roughly 17,000 words.",
            "We counted about 110 candidate habits, kept the ones he actually uses, and wrote down the words that never appear in his speech. The result is a voice guide with real quotes and a never-say list. Nothing in it is invented biography.",
            "On the second pass we corrected ourselves. Two words we had banned turned out to be in his speech, so they moved from “never” to “avoid as filler.”",
        ], None),
        ("Moving a library without losing a book.", [
            "The old site held 18 blog posts, 7 beginner guides, 28 new-release pages, 111 FAQs and a glossary. We moved it by script wherever the markup allowed. All 791 glossary terms, with pronunciations and category tiers, came across in one pass instead of being retyped.",
            "When we checked the new-release pages against the old ones, only 7 of 28 were on the new site. We added the other 21, with their photos. The 117 event and lounge photos shrank from 99.4 MB to 20.5 MB, down 79 percent, so the gallery loads on a phone.",
            "The founder caught one error himself. A review said Macanudo 1968. The cigar is a 1868, and its hero image showed a different band. We replaced it with the real photos already on file. Seven reviews were missing the founder’s own “From the Porch” story, so we asked, and he wrote all seven the next day.",
        ], fig("blc/new-reviews", 1280, 720, "The new reviews page, with the BLC rating scale up front.", "BLC reviews page showing the rating scale and review cards")),
        ("A 26-page PDF became a shared list.", [
            "The founder’s revisions arrived as a 26-page PDF. We turned every note into its own tracked item: 90 items across 21 sections at first, 176 by September 22. Each item carries a status, a note on what we built, and a comment box, so the founder and his team could settle a question in the open instead of in a thread.",
            "Where we disagreed with a note, we ran the options past a simulated panel of marketers instead of picking one. The homepage line “Built by people who actually smoke cigars” came out of that.",
        ], None),
        ("The hardest part was the last mile.", [
            "On September 22 we found something awkward. About twenty commits of work were on GitHub and none of it was live. The domain still served the old site. We said so plainly instead of calling it launched.",
            "Three days later the domain moved. We checked the live site ourselves rather than taking it on faith: a normal response, no trace of the old software, the right page title.",
        ], None),
        ("Handing over the keys.", [
            "BLC should not need us for every edit. On September 29 we set the founder up to change his own site safely: an editor with Claude Code installed, a separate preview copy of the site, and one rule written into the project. Nothing goes to the live site until he has seen it on preview. A test photo went up on the preview that same day.",
            "We switched some things off on purpose. The “Ash” chat helper kept answering “I don’t have a script for that,” so it is off behind one setting, and visitors go to the contact page until it is rebuilt. Instagram refuses to show cigar posts to logged-out visitors, so we hosted the founder’s two reels on the site instead of embedding them.",
        ], None),
    ],
    results=[("About 2 weeks", "From the first push to GitHub (September 11) to the new site on its own domain (September 25)."),
             ("791", "Glossary terms moved across by script."),
             ("−79%", "Gallery image weight, 99.4 MB down to 20.5 MB."),
             ("90 to 176", "Tracked launch items, each with a status and a note.")],
    note="These are delivery facts. BLC’s own results, such as members and podcast listens, are not ours to publish.",
    still_open=["Pushes to the live site are still manual. The hosting account has no automatic deploy connected yet.",
                "The Ash helper is off until it is rebuilt.",
                "Five compliance questions are with the founder’s counsel."],
    check=["BLC is described as a free community that sells nothing.",
           "The compliance story is told fairly: we first assumed the strict reading, then rebuilt around his compliance review. Please also check the wording about the law.",
           "The founder’s “forty years, not a fan of the first five” story can be told.",
           "The old and new site screenshots on this page can be public.",
           "The numbers: 791 glossary terms, 117 photos, 99.4 MB to 20.5 MB, and September 11 to September 25.",
           "The founder’s name, BLC’s name and link can appear on our public Work page."],
),
}

CSS = """<style>
.rv-top{max-width:1200px;margin:0 auto;padding:140px 80px 8px}
.rv-top h1{font-family:var(--font-display);font-weight:400;font-size:clamp(26px,3.4vw,40px);letter-spacing:-.03em;line-height:1.1;color:var(--deep-forest)}
.rv-top p{margin-top:16px;font-size:17px;line-height:1.7;color:var(--ink-2);max-width:720px}
.rv-flag{display:inline-block;margin-bottom:16px;padding:6px 12px;border-radius:9999px;background:var(--cream-d,#EDE8DC);font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#9D5537}
.rv-study .study-head{padding-top:32px}
.rv-pair{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px;margin-top:28px}
.rv-study .study-copy>.study-shot{margin-top:28px}
.rv-open,.rv-check{max-width:1040px;margin:0 auto 24px;padding:28px 28px;border:1px solid var(--rule);border-radius:14px;background:#FBF8F2}
.rv-open h2,.rv-check h2{font-family:var(--font-display);font-weight:400;font-size:22px;color:var(--deep-forest)}
.rv-open ul,.rv-check ul{list-style:none;margin-top:14px}.rv-open li,.rv-check li{padding:7px 0;font-size:16px;line-height:1.6;color:var(--ink-2)}
.rv-check input{margin-right:8px;accent-color:#3D6B4F}
.rv-q{margin-top:16px;font-size:15px;color:var(--ink-2)}
.rv-end{padding:24px 80px 96px}
@media(max-width:1100px){.rv-top{padding-left:40px;padding-right:40px}.rv-end{padding-left:40px;padding-right:40px}}
@media(max-width:720px){.rv-top{padding-left:24px;padding-right:24px}.rv-end{padding-left:24px;padding-right:24px}.rv-pair{grid-template-columns:1fr}}
</style>"""


def build(key):
    s = STORIES[key]
    secs = ""
    for heading, paras, extra in s["chapters"]:
        secs += (f'<section class="study-section"><h2>{e(heading)}</h2><div class="study-copy">'
                 + "".join(f"<p>{e(p)}</p>" for p in paras) + (extra or "") + "</div></section>")
    res = '<ul class="study-results">' + "".join(f"<li><b>{e(a)}</b><span>{e(b)}</span></li>" for a, b in s["results"]) + "</ul>"
    secs += (f'<section class="study-section"><h2>What changed</h2><div class="study-copy">{res}'
             f'<p class="study-note">{e(s["note"])}</p></div></section>')
    meta = "".join(f"<div><dt>{e(a)}</dt><dd>{e(b)}</dd></div>" for a, b in s["meta"])
    opens = "".join(f"<li>{e(t)}</li>" for t in s["still_open"])
    checks = "".join(f'<li><label><input type="checkbox"> {e(t)}</label></li>' for t in s["check"])
    main = f"""<main class="rv-study">
    <div class="rv-top"><span class="rv-flag">Draft for review. Not published.</span>
      <h1>{e(s['name'])} case study, for your approval.</h1>
      <p>This page is private. It is not linked from our website and search engines are told to skip it, but anyone with the address can open it, so please do not forward it. It shows the case study as we would publish it. Nothing goes on our public site until you say yes. Tick what is accurate, tell us what to change, and we will update this page first.</p></div>
    <header class="study-head">
      <h2 class="study-title">{e(s['name'])}</h2>
      <p class="study-dek">{e(s['dek'])}</p>
      <div class="study-lede"><blockquote class="study-quote"><p>{e(s['quote'][0])}</p><cite>{e(s['quote'][1])}</cite></blockquote></div>
      <dl class="study-meta">{meta}</dl>
    </header>
    <div class="study-body">{secs}</div>
    <div class="rv-end">
      <div class="rv-open"><h2>What is still open</h2><ul>{opens}</ul></div>
      <div class="rv-check"><h2>Please check before anything is published</h2><ul>{checks}</ul>
        <p class="rv-q">Edits, cuts, or anything we got wrong? Reply to Riya and we will change it.</p></div>
    </div>
  </main>"""
    page = re.sub(r"<main>.*?</main>", lambda m: main, BASE, flags=re.S)
    page = re.sub(r'<script type="application/ld\+json">.*?</script>', "", page, flags=re.S)
    page = re.sub(r'  <link rel="canonical"[^\n]*\n', '  <meta name="robots" content="noindex, nofollow">\n', page)
    page = re.sub(r"<meta (property|name)=\"(og|twitter):[^\n]*\n", "", page)
    page = re.sub(r"<title>.*?</title>", f"<title>{e(s['name'])} case study for review | Throughline Co.</title>", page)
    page = page.replace("</head>", CSS + "\n</head>", 1)
    out = f"work/review-{key}-{s['token']}.html"
    open(out, "w", encoding="utf-8").write(page)
    print("wrote", out)


if __name__ == "__main__":
    for k in STORIES:
        build(k)
