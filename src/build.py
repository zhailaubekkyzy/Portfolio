"""Build the site from src/.  Run from the repo root:  python3 src/build.py

  src/home.src.html  -> index.html               (bilingual RU/EN, projects list)
  src/case.src.html  -> rfm-smartflow.html       + en/rfm-smartflow.html  (via src/en_case.py)
  src/navspy.html    -> appended to both case pages (active section in the top nav)
  src/crm.src.html   -> rfm-dashboard.html       + en/rfm-dashboard.html  (via src/en_crm.py; sim.js + analytics.js inlined)

Source pages are fragments (no <html>/<head>); this script wraps them into full documents.
It prints any Russian text left untranslated in the English pages.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
sys.path.insert(0, SRC)
import en_case, en_crm, booklover_text  # noqa: E402
import json

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


def wrap(fragment, lang):
    i = fragment.index("</style>") + len("</style>")
    return HEAD.format(lang=lang) + fragment[:i] + "\n</head>\n<body>\n" + fragment[i:] + "\n</body>\n</html>\n"


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
    print("Done.")


if __name__ == "__main__":
    main()
