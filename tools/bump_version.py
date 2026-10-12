#!/usr/bin/env python3
"""Bump Perfboard Planner to the next CalVer version (YYYY.MM.MICRO).

MICRO restarts at 0 each month and counts releases within it.
Updates APP_VERSION / APP_DATE / RELEASE_NOTES in index.html and adds a CHANGELOG.md section.

    python3 tools/bump_version.py "First change" "Second change"
"""
import datetime, json, pathlib, re, sys

root = pathlib.Path(__file__).resolve().parent.parent
html = root / "index.html"
log = root / "CHANGELOG.md"
notes = sys.argv[1:]
if not notes:
    sys.exit("Give at least one release note, e.g. bump_version.py \"Added X\"")

src = html.read_text(encoding="utf-8")
cur = re.search(r"APP_VERSION='(\d{4})\.(\d{1,2})\.(\d+)'", src)
if not cur:
    sys.exit("APP_VERSION not found in index.html")
today = datetime.date.today()
y, m, n = (int(x) for x in cur.groups())
new = f"{today.year}.{today.month}.{n + 1 if (y, m) == (today.year, today.month) else 0}"

src = re.sub(r"APP_VERSION='[^']*'", f"APP_VERSION='{new}'", src, count=1)
src = re.sub(r"APP_DATE='[^']*'", f"APP_DATE='{today.isoformat()}'", src, count=1)
src = re.sub(r"const RELEASE_NOTES=\[.*?\];", "const RELEASE_NOTES=[\n  " + ",\n  ".join(json.dumps(x, ensure_ascii=False) for x in notes) + "];", src, count=1, flags=re.S)
html.write_text(src, encoding="utf-8")

entry = f"## [{new}] - {today.isoformat()}\n\n" + "\n".join(f"- {x}" for x in notes) + "\n\n"
text = log.read_text(encoding="utf-8")
i = text.find("\n## [")
log.write_text(text[: i + 1] + entry + text[i + 1 :] if i >= 0 else text + "\n" + entry, encoding="utf-8")
print(f"{cur.group(0)} -> {new}")
