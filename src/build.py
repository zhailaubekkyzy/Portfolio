"""Build the site from src/.  Run from the repo root:  python3 src/build.py

  src/home.src.html  -> index.html               (bilingual RU/EN, projects list)
  src/case.src.html  -> rfm-smartflow.html       + en/rfm-smartflow.html  (via src/en_case.py)
  src/blcrm.src.html -> booklover-crm.html      + en/booklover-crm.html  (texts in blcrm_text.py, data from blsim.js)
  src/pp.src.html  -> projectpro-retention.html + en/projectpro-retention.html  (texts in projectpro_text.py, accounts from ppsim.js)
  src/navspy.html    -> appended to both case pages (active section in the top nav)
  src/crm.src.html   -> rfm-dashboard.html       + en/rfm-dashboard.html  (via src/en_crm.py; sim.js + analytics.js inlined)

Source pages are fragments (no <html>/<head>); this script wraps them into full documents.
It prints any Russian text left untranslated in the English pages.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
sys.path.insert(0, SRC)
import en_case, en_crm, booklover_text, blcrm_text, projectpro_text  # noqa: E402
import json, html

CYR = re.compile("[А-Яа-яЁё]")
HEAD = ('<!doctype html>\n<html lang="{lang}">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<style>:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}'
        'body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>\n')


def read(name):
    with open(os.path.join(SRC, name), encoding="utf-8") as f:
        return f.read()


def write(rel, text):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"  wrote {rel} ({len(text) // 1024} KB)")


# Shared by every page: (1) start at the very top — also inside the Claude app, where the page sits in a frame and
# window.scrollTo alone does not move the screen; (2) hide the phone keyboard when tapping outside a text field,
# on Enter and on Escape.
GLOBAL = """<script>
(function () {
  try { if ("scrollRestoration" in history) history.scrollRestoration = "manual"; } catch (e) {}
  function toTop() {
    try { window.scrollTo(0, 0); } catch (e) {}
    try { if (window.top !== window && document.body) document.body.scrollIntoView({ block: "start" }); } catch (e) {}
  }
  window.pfToTop = toTop;
  function onLoad() {
    var h = decodeURIComponent(location.hash.slice(1));
    if (h && document.getElementById(h)) return; // a link to a section of a long page keeps its place
    toTop();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", onLoad); else onLoad();
  window.addEventListener("pageshow", function (e) { if (e.persisted) onLoad(); });
  var TYPING = /^(INPUT|TEXTAREA|SELECT)$/;
  function typing(el) { return el && (el.isContentEditable || (TYPING.test(el.tagName) && el.type !== "range" && el.type !== "checkbox" && el.type !== "radio" && el.type !== "button")); }
  document.addEventListener("pointerdown", function (e) {
    var a = document.activeElement;
    if (!typing(a)) return;
    var t = e.target;
    if (t && t.closest && t.closest("input, textarea, select, label, [contenteditable]")) return;
    a.blur();
  }, true);
  document.addEventListener("keydown", function (e) {
    var a = document.activeElement;
    if (!typing(a) || a.tagName === "TEXTAREA") return;
    if (e.key === "Enter" || e.key === "Escape") a.blur();
  });
})();
</script>"""


def wrap(fragment, lang):
    i = fragment.index("</style>") + len("</style>")
    return HEAD.format(lang=lang) + fragment[:i] + "\n</head>\n<body>\n" + fragment[i:] + "\n" + GLOBAL + "\n</body>\n</html>\n"


def pairs(text, pairs_list, label):
    for ru, en in pairs_list:
        if ru not in text:
            print(f"  ! {label}: not found: {ru[:70]!r}")
        text = text.replace(ru, en)
    return text


def segments(text, table):
    """Translate every Russian fragment between quotes, tags, backticks and ${ } using the table."""
    parts = re.split(r'([<>"`]|\$\{|\})', text)
    missing = []
    for i, p in enumerate(parts):
        if not CYR.search(p):
            continue
        core = p.strip()
        if core in table:
            lead = p[: len(p) - len(p.lstrip())]
            trail = p[len(p.rstrip()):]
            parts[i] = lead + table[core] + trail
        else:
            missing.append(core)
    return "".join(parts), missing


def leftovers(text, label, skip=()):
    lines = [l.strip()[:110] for l in text.splitlines() if CYR.search(l) and not any(s in l for s in skip)]
    if lines:
        print(f"  ! {label}: {len(lines)} lines still contain Russian, e.g.:")
        for l in lines[:12]:
            print("     ", l)


def main():
    print("Building…")
    # home
    write("index.html", wrap(read("home.src.html"), "ru"))
    write("en/index.html", '<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=../#en">'
                           '<title>Portfolio</title><a href="../#en">Portfolio</a>\n')

    # sticky-nav section highlight + reading progress, shared by the case pages
    spy = "\n" + read("navspy.html")

    # case page
    case = read("case.src.html") + spy
    write("rfm-smartflow.html", wrap(case, "ru"))
    case_en = pairs(case, en_case.PAIRS, "case")
    leftovers(case_en, "en/rfm-smartflow.html")
    write("en/rfm-smartflow.html", wrap(case_en, "en"))

    # CRM dashboard
    crm = read("crm.src.html")
    sim, ana = read("sim.js"), read("analytics.js")
    write("rfm-dashboard.html", wrap(crm.replace("/*__SIM__*/", sim).replace("/*__ANALYTICS__*/", ana), "ru"))
    crm_en = pairs(crm, en_crm.CODE, "crm code")
    crm_en, missing = segments(crm_en, en_crm.T)
    if missing:
        print(f"  ! crm: {len(set(missing))} Russian fragments have no translation in en_crm.T:")
        for m in sorted(set(missing))[:40]:
            print("     ", repr(m[:100]))
    leftovers(crm_en, "en/rfm-dashboard.html")
    write("en/rfm-dashboard.html", wrap(crm_en.replace("/*__SIM__*/", sim).replace("/*__ANALYTICS__*/", ana), "en"))

    # BookLover retention case: {{key}} placeholders filled from booklover_text.py
    bl = read("booklover.src.html") + spy
    for i, lang in enumerate(("ru", "en")):
        page = bl
        extra = {
            "back_href": ("./", "../#en")[i],
            "lang_href": ("en/booklover-retention.html", "../booklover-retention.html")[i],
            "lang_label": ("EN", "RU")[i],
            "root": ("", "../")[i],
            "sql_all": html.escape(open(os.path.join(ROOT, "files", "booklover-retention.sql"), encoding="utf-8").read(), quote=False),
        }
        def sub(m):
            k = m.group(1)
            if k in extra:
                return extra[k]
            if k not in booklover_text.T:
                print(f"  ! booklover: missing key {k}")
                return k
            # keep RU thousands like "8 100" on one line
            return re.sub(r"(\d) (\d{3})(?!\d)", "\\1\u00a0\\2", booklover_text.T[k][i])
        page = re.sub(r"\{\{(\w+)\}\}", sub, page)
        page = page.replace("/*__JS__*/", json.dumps({k: v[i] for k, v in booklover_text.JS.items()}, ensure_ascii=False))
        if lang == "en":
            leftovers(page, "en/booklover-retention.html", skip=("GoPractice",))
        write(("booklover-retention.html", "en/booklover-retention.html")[i], wrap(page, lang))
    # BookLover CRM dashboard: {{key}} placeholders and the page script's T object come from blcrm_text.py
    crm2 = read("blcrm.src.html").replace("/*__SIM__*/", read("blsim.js"))
    for i, lang in enumerate(("ru", "en")):
        extra = {
            "portfolio_href": ("./", "../#en")[i],
            "lang_href": ("en/booklover-crm.html", "../booklover-crm.html")[i],
            "lang_label": ("EN", "RU")[i],
            "root": ("", "../")[i],
        }
        tx = {k: v[i] for k, v in blcrm_text.T.items()}
        tx.update({"c_" + k: v[i] for k, v in booklover_text.T.items()})  # case texts reused as steps of the dashboard
        def sub2(m):
            k = m.group(1)
            if k in extra:
                return extra[k]
            if k not in tx:
                print(f"  ! booklover-crm: missing key {k}")
                return k
            return re.sub(r"(\d) (\d{3})(?!\d)", "\\1\u00a0\\2", tx[k])
        page = re.sub(r"\{\{(\w+)\}\}", sub2, crm2)
        page = page.replace("/*__T__*/", json.dumps(tx, ensure_ascii=False))
        with open(os.path.join(ROOT, "files", "booklover-retention.sql"), encoding="utf-8") as fh:
            page = page.replace("/*__SQL__*/", json.dumps(fh.read()))
        if lang == "en":
            leftovers(page, "en/booklover-crm.html")
        write(("booklover-crm.html", "en/booklover-crm.html")[i], wrap(page, lang))
    # ProjectPro B2B retention case: {{key}} placeholders and the page script's T object come from projectpro_text.py
    pp = read("pp.src.html").replace("/*__SIM__*/", read("ppsim.js"))
    for i, lang in enumerate(("ru", "en")):
        extra = {
            "portfolio_href": ("./", "../#en")[i],
            "lang_href": ("en/projectpro-retention.html", "../projectpro-retention.html")[i],
            "lang_label": ("EN", "RU")[i],
            "root": ("", "../")[i],
        }
        tx = {k: v[i] for k, v in projectpro_text.T.items()}
        def sub3(m):
            k = m.group(1)
            if k in extra:
                return extra[k]
            if k not in tx or not isinstance(tx[k], str):
                print(f"  ! projectpro: missing key {k}")
                return k
            return re.sub(r"(\d) (\d{3})(?!\d)", "\\1\u00a0\\2", tx[k])
        page = re.sub(r"\{\{(\w+)\}\}", sub3, pp)
        page = page.replace("/*__T__*/", json.dumps(tx, ensure_ascii=False))
        if lang == "en":
            leftovers(page, "en/projectpro-retention.html")
        write(("projectpro-retention.html", "en/projectpro-retention.html")[i], wrap(page, lang))
    print("Done.")


if __name__ == "__main__":
    main()
