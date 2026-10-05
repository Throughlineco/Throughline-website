"""Private client-review page for the DF and BLC case studies.
Run: python3 build_review.py  ->  work/review-df-blc-5f3a9c.html
Unlinked, noindex, not in the sitemap. Delete it once both clients have replied.
Copy comes straight from STUDIES in build_work.py, so edit there and rerun both."""
import html
import re
import build_work as bw

e = html.escape
S = {s["slug"]: (i, s) for i, s in enumerate(bw.STUDIES)}
OUT = "work/review-df-blc-5f3a9c.html"

CHECK = {
    "df": ["The page describes DF as a done-for-you email marketing company for product brands.",
           "A 16-page site, designed, written and built by us from August 19, 2026.",
           "The Fit Check quiz, which tells visitors whether they are a fit before they book.",
           "Lighthouse scores of 99 (performance), 100 (accessibility) and 100 (SEO), measured October 4, 2026.",
           "Homepage weight cut 28 percent (860 KB to 616 KB)."],
    "blc": ["The page describes BLC as a free cigar reviews, education, podcast and community platform.",
            "About two weeks from first commit (September 11, 2026) to the new site live, replacing WordPress.",
            "149 pages in the new sitemap, and 791 glossary terms moved across by script.",
            "The compliance work: content guardrails written against Canada's tobacco advertising rules, and an audit of 86 images.",
            "Gallery image weight cut 79 percent (99.4 MB to 20.5 MB)."],
}


def parts(slug):
    i, s = S[slug]
    page = bw.render(i, s)
    head = re.search(r'<header class="study-head">.*?</header>', page, re.S).group(0)
    head = re.sub(r'<a class="study-back.*?</a>', "", head, flags=re.S)
    body = re.search(r'<div class="study-body">.*?</div>\s*\n\s*<aside', page, re.S).group(0)[:-len("<aside")].rstrip()
    return page, head, body


page, df_head, df_body = parts("df")
_, blc_head, blc_body = parts("blc")


def block(label, slug, head, body):
    items = "".join(f"<li><label><input type=\"checkbox\"> {e(t)}</label></li>" for t in CHECK[slug])
    return f"""<section class="rv-block">
      <p class="rv-tag">{label}</p>
      {head}
      {body}
      <div class="rv-check"><h2>Please check these before anything is published</h2>
        <ul>{items}</ul>
        <p class="rv-q">Edits, cuts or anything we got wrong? Reply to Riya and we will change it. Nothing goes on the public site until you say yes.</p></div>
    </section>"""


css = """<style>
.rv-top{max-width:1200px;margin:0 auto;padding:140px 80px 8px}.rv-top p{max-width:720px}.rv-block .study-head{padding-top:20px}.rv-block .study-body{padding-top:48px}
.rv-top h1{font-family:var(--font-display);font-weight:400;font-size:clamp(30px,4vw,46px);letter-spacing:-.03em;line-height:1.1;color:var(--deep-forest)}
.rv-top p{margin-top:16px;font-size:17px;line-height:1.7;color:var(--ink-2)}
.rv-flag{display:inline-block;margin-bottom:16px;padding:6px 12px;border-radius:9999px;background:var(--cream-d,#EDE8DC);font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#9D5537}
.rv-block{padding:56px 0 24px;border-top:1px solid var(--rule)}
.rv-block:first-of-type{margin-top:40px}
.rv-tag{max-width:1200px;margin:0 auto;padding:0 80px;font-size:12px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#9D5537}
.rv-check{max-width:1040px;margin:24px auto 0;padding:28px 24px;border:1px solid var(--rule);border-radius:14px;background:#FBF8F2}
.rv-check h2{font-family:var(--font-display);font-weight:400;font-size:22px;color:var(--deep-forest)}
.rv-check ul{list-style:none;margin-top:14px}.rv-check li{padding:8px 0;font-size:16px;line-height:1.6;color:var(--ink-2)}
.rv-check input{margin-right:8px;accent-color:#3D6B4F}
.rv-q{margin-top:16px;font-size:15px;color:var(--ink-2)}
@media(max-width:1100px){.rv-top,.rv-tag{padding-left:40px;padding-right:40px}.rv-check{margin-left:40px;margin-right:40px}}
@media(max-width:720px){.rv-top,.rv-tag{padding-left:24px;padding-right:24px}.rv-check{margin-left:24px;margin-right:24px}}
</style>"""
intro = """<div class="rv-top"><span class="rv-flag">Draft for review. Not published.</span>
<h1>Two case studies, for your approval.</h1>
<p>This page is private. It is not linked from our website and search engines are told to skip it. Below are the two case studies exactly as we would publish them. Your company name, link and screenshots are left out until you say they can go in. Tick what is accurate, tell us what to change, and we will update this page before anything goes live.</p></div>"""

main = f'<main>{intro}{block("Case study 1", "df", df_head, df_body)}{block("Case study 2", "blc", blc_head, blc_body)}</main>'
page = re.sub(r"<main>.*?</main>", lambda m: main, page, flags=re.S)
page = re.sub(r'<script type="application/ld\+json">.*?</script>', "", page, flags=re.S)
page = re.sub(r'  <link rel="canonical"[^\n]*\n', '  <meta name="robots" content="noindex, nofollow">\n', page)
page = re.sub(r"<meta (property|name)=\"(og|twitter):[^\n]*\n", "", page)
page = re.sub(r"<title>.*?</title>", "<title>Case studies for review | Throughline Co.</title>", page)
page = page.replace("</head>", css + "\n</head>", 1)
open(OUT, "w", encoding="utf-8").write(page)
print("wrote", OUT)
