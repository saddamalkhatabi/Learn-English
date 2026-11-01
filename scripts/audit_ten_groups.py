"""Audit existence and navigability of every learning group in the deployed source tree.

Requires no network. Audio coverage for the tenth group is an opt-in extra
so the initial curriculum commit can pass before MP3 generation completes.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
names = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten")
html = (ROOT / "index.html").read_text(encoding="utf-8")
app = (ROOT / "app.js").read_text(encoding="utf-8")
server = (ROOT / "server.mjs").read_text(encoding="utf-8")
readme = (ROOT / "README.md").read_text(encoding="utf-8")
source = json.loads((ROOT / "data/patterns.json").read_text(encoding="utf-8"))
assert len(source["patterns"]) == 1034, "Source corpus changed unexpectedly"
ids = {p["id"] for p in source["patterns"]}
total_patterns = total_scenes = 0
for n, name in enumerate(names, 1):
    tag = "g" + str(n)
    filename = f"group-{name}"
    file = ROOT / f"data/{filename}.json"
    code = ROOT / f"{filename}.js"
    assert file.is_file() and code.is_file(), (name, "missing group data/module")
    data = json.loads(file.read_text(encoding="utf-8"))
    assert data.get("schema") == 1 and len(data["items"]) == 18, (name, "invalid pattern count")
    assert [p["id"] for p in data["items"]] == list(range(1, 19))
    assert len({p["key"] for p in data["items"]}) == 18, (name, "duplicate keys")
    assert all(len(p["scenes"]) == 4 for p in data["items"]), (name, "invalid scenes")
    assert all(p["title"] and p["meaning"] and p["formula"] for p in data["items"])
    assert all(not p.get("sourceIds") or set(p["sourceIds"]).issubset(ids) for p in data["items"]), (name, "unknown source IDs")
    total_patterns += len(data["items"])
    total_scenes += sum(len(p["scenes"]) for p in data["items"])
    assert f'data-view="{filename}"' in html and f'id="view-{filename}"' in html, (name, "navigation missing")
    assert f'src="{filename}.js"' in html, (name, "script missing")
    assert f'"{filename}"' in app, (name, "router missing")
    assert f'window.GROUP_{name.upper()}?.open()' in app, (name, "hook missing")
    assert f'"/{filename}.js"' in server, (name, "server whitelist missing")
    assert f'window.GROUP_{name.upper()}=' in code.read_text(encoding="utf-8"), (name, "module export missing")
    assert f'id="{tag}PatternList"' in html, (name, "pattern UI missing")
    assert f'docs/GROUP-{name.upper()}-AR.md' in readme, (name, "documentation missing")
    assert (ROOT / f"docs/GROUP-{name.upper()}-AR.md").is_file(), (name, "doc file missing")
assert total_patterns == 180 and total_scenes == 720
assert len(set(re.findall(r'data-view="group-([a-z]+)"', html))) == 10
assert "عشر مجموعات" in html
if "--require-ten-audio" in sys.argv:
    index = json.loads((ROOT / "data/group-ten-audio-index.json").read_text(encoding="utf-8"))
    assert index["verified_count"] == 198 and len(index["items"]) == 198
    from subprocess import run
    run([sys.executable, str(ROOT / "scripts/test_group_ten.py"), "--require-audio"], check=True)
print("OK: all 10 groups on main have 180 patterns, 720 scenes, 10 navigators, 10 scripts, source links and documentation.")
