"""Build the meeting board (one HTML page) and the Excel task file.

Usage:
  python build_board.py --data data.json --transcript transcript.txt --out board.html --xlsx "tasks.xlsx"
Options:
  --config DIR   folder with team.json, glossary.json and photos/ (default: ../config next to this script)

Reads data.json (see references/data-schema.md), cleans the transcript with config/glossary.json,
maps speakers with config/team.json aliases, merges lines that have no timestamps ("untimed", from a
backup recorder), embeds photos from config/photos/<id>.webp|png|jpg, checks the v2 fields a reader
who missed the call needs, and writes a self-contained board.html plus the .xlsx (also embedded in the
page for download).
Needs: Python 3.9+, openpyxl. Pillow is optional (only for .png/.jpg photos).
"""
import argparse
import base64
import io
import json
import re
import sys
import urllib.parse
from pathlib import Path

try:
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
except ImportError:
    sys.exit("openpyxl is missing. Run: python -m pip install openpyxl")

HERE = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument("--data", required=True)
ap.add_argument("--transcript")
ap.add_argument("--out", required=True)
ap.add_argument("--xlsx", required=True)
ap.add_argument("--config", default=str(HERE.parent / "config"))
args = ap.parse_args()

cfg = Path(args.config)
D = json.loads(Path(args.data).read_text(encoding="utf8"))
team = json.loads((cfg / "team.json").read_text(encoding="utf8")) if (cfg / "team.json").exists() else {"people": []}
gloss = json.loads((cfg / "glossary.json").read_text(encoding="utf8")) if (cfg / "glossary.json").exists() else {}
P = {p["id"]: p for p in D["people"]}
PJ = {p["id"]: p["name"] for p in D["projects"]}
for key in ("tasks", "decisions", "open", "watch", "notes", "spelling", "chapters", "terms", "untimed"):
    D.setdefault(key, [])
D.setdefault("quiz", {"pass": 0, "minutes": 0, "questions": []})


def secs(ts):
    n = [int(x) for x in ts.split(":")]
    return n[0] * 3600 + n[1] * 60 + n[2] if len(n) == 3 else n[0] * 60 + n[1]


def fmt(s):
    s = int(round(s)); h, m, x = s // 3600, s % 3600 // 60, s % 60
    return f"{h}:{m:02d}:{x:02d}" if h else f"{m}:{x:02d}"


def at(sec):
    rec = D["meta"].get("recording") or ""
    if not rec:
        return ""
    nav = {"referralInfo": {"referralApp": "StreamWebApp", "referralView": "ShareDialog", "referralAppPlatform": "Web", "referralMode": "view"},
           "playbackOptions": {"startTimeInSeconds": sec}}
    b = base64.b64encode(json.dumps(nav, separators=(",", ":")).encode()).decode()
    return rec + "?nav=" + urllib.parse.quote(b, safe="")


# ---------- speakers ----------
alias = {}
for p in team.get("people", []):
    for a in [p["name"]] + p.get("aliases", []):
        alias[a.lower()] = p["id"]
for p in D["people"]:
    alias.setdefault(p["name"].lower(), p["id"])
    for a in p.get("aliases", []):
        alias.setdefault(a.lower(), p["id"])

# ---------- clean transcript ----------
FILLER = set("""mm mhm mmh hmm yeah yes okay ok fin the e i no hello hands play pardon what who so and but open sub ohh oh ah huh uh
look up ms am of you thank stand then wow oi got it correct exactly right understood fine good well hey a to be now alright all me""".split())
FILLER |= {w.lower() for w in gloss.get("filler", [])}
FIXES = [(r"\b" + re.escape(f["heard"]) + r"\b", f["fix"]) for f in gloss.get("fixes", [])]
utt, removed, fixes, before, unknown = [], 0, 0, 0, set()
if args.transcript and Path(args.transcript).exists():
    for line in Path(args.transcript).read_text(encoding="utf8").splitlines():
        m = re.match(r"^(.+?)\s{2,}(\d+(?::\d+){1,2})(.*)$", line)
        if not m:
            continue
        before += 1
        name = m.group(1).strip()
        sp = alias.get(name.lower())
        if not sp:
            unknown.add(name); continue
        text = re.sub(r"([.?!])(?=[A-Za-z])", r"\1 ", m.group(3).strip())
        keep = []
        for sent in re.split(r"(?<=[.?!])\s+", text):
            words = re.findall(r"[a-z']+", sent.lower())
            if not sent.strip() or set(sent.strip()) <= set("*."):
                continue
            if words and len(words) <= 3 and all(w in FILLER for w in words):
                continue
            keep.append(sent.strip())
        if not keep:
            removed += 1; continue
        text = " ".join(keep)
        for pat, rep in FIXES:
            text, n = re.subn(pat, rep, text, flags=re.I); fixes += n
        s = secs(m.group(2))
        if utt and utt[-1]["sp"] == sp and s - utt[-1]["s"] < 90:
            utt[-1]["text"] += " " + text
        else:
            utt.append({"s": s, "sp": sp, "text": text})
if unknown:
    print("WARNING: speakers not in data.json people or team.json aliases (their lines were skipped):", ", ".join(sorted(unknown)))

# lines with no timestamp (a backup recorder): placed at "at" seconds, marked nt so the board shows "no time"
for x in D["untimed"]:
    sp = x.get("sp") or "unmarked"
    if sp not in P:
        D["people"].append({"id": sp, "name": "Unmarked speaker", "title": "Backup recorder, no names", "attended": False, "notime": True})
        P[sp] = D["people"][-1]
    text = x["text"]
    for pat, rep_ in FIXES:
        text, n = re.subn(pat, rep_, text, flags=re.I); fixes += n
    utt.append({"s": int(x["at"]), "sp": sp, "text": text, "nt": True})
utt.sort(key=lambda u: (u["s"], 1 if u.get("nt") else 0))
del D["untimed"]
D["transcript"] = utt

# ---------- checks for readers who missed the call ----------
def warn(msg):
    print("CHECK:", msg)
if not D.get("context"):
    warn("no 'context' (before / call / question / decided): the overview cannot explain why the meeting happened")
for c in D["chapters"]:
    if not c.get("summary"):
        warn(f"chapter {c['n']} has no 'summary'")
for t in D["tasks"]:
    if not t.get("why") or not t.get("done"):
        warn(f"task {t['id']} has no 'why' or 'done': it will not make sense on its own")
if not D["terms"]:
    warn("no 'terms': list the acronyms, team words and names a newcomer would not know")
pic = D.get("picture")
if pic and int(pic.get("confidence", 100)) < 90 and not pic.get("ask"):
    warn("picture confidence is under 90% but 'ask' has no timestamps for screenshots")
pids = {p["id"] for p in D["projects"]}
stages = [s["name"] if isinstance(s, dict) else s for s in D.get("stages") or ["Idea", "Shaping", "Planned", "Building", "Live"]]
for p in D["projects"]:
    if p.get("stage") and p["stage"] not in stages:
        warn(f"project {p['id']} stage '{p['stage']}' is not one of {stages}")
for k in ("tasks", "decisions", "open", "chapters"):
    for x in D[k]:
        if x.get("project") and x["project"] not in pids:
            warn(f"{k}: project '{x['project']}' is not in projects")
D["clean"] = {"lines_before": before, "lines_after": len(utt), "fixes": fixes}

# ---------- photos ----------
D["photos"] = {}
pdir = cfg / team.get("photos_dir", "photos")
for pid in P:
    for ext in ("webp", "png", "jpg", "jpeg"):
        f = pdir / f"{pid}.{ext}"
        if not f.exists():
            continue
        if ext == "webp":
            D["photos"][pid] = "data:image/webp;base64," + base64.b64encode(f.read_bytes()).decode()
        else:
            try:
                from PIL import Image
                im = Image.open(f).convert("RGBA"); w, h = im.size; side = min(w, h)
                im = im.crop(((w - side) // 2, 0, (w + side) // 2, side)).resize((120, 120))
                buf = io.BytesIO(); im.save(buf, "WEBP", quality=84)
                D["photos"][pid] = "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()
            except Exception as e:  # pillow missing or bad file: initials are used instead
                print(f"photo skipped for {pid}: {e}")
        break

# ---------- excel ----------
wb = Workbook()
HEAD = PatternFill("solid", fgColor="0A0A0A"); HF = Font(bold=True, color="FFFFFF"); LINK = Font(color="0068D6", underline="single")


def chapter(t):
    for c in D["chapters"]:
        if c["start"] <= t < c["end"]:
            return f'{c["n"]}. {c["title"]}'
    return ""


def sheet(ws, headers, rows, widths, link_col):
    ws.append(headers)
    for c in ws[1]:
        c.fill, c.font = HEAD, HF
    for r in rows:
        ws.append([v for v, _ in r])
        if r[link_col][1]:
            cell = ws.cell(row=ws.max_row, column=link_col + 1); cell.hyperlink = r[link_col][1]; cell.font = LINK
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "A2"; ws.auto_filter.ref = ws.dimensions


name = lambda i: P[i]["name"] if i in P else i
ws = wb.active; ws.title = "Tasks"
rows = []
for t in D["tasks"]:
    owners = ", ".join(name(o) for o in t["owners"]) or ("Needs owner" + (f' (suggested: {name(t["suggested"])})' if t.get("suggested") else ""))
    pr = {"now": "Do now", "next": "Next", "proposed": "Proposed"}.get(t["priority"], t["priority"])
    extra = t.get("extra") or {}
    rows.append([(t["id"], 0), (t["task"], 0), (t.get("why", ""), 0), (t.get("done", ""), 0), ((extra.get("label", "") + ": " + extra.get("text", "")) if extra.get("text") else "", 0),
                 (owners, 0), ("External" if t.get("external") else "Our team", 0), (PJ.get(t["project"], t["project"]), 0),
                 (pr, 0), (t["due"], 0), (t["status"], 0), ("", 0), (fmt(t["t"]), at(t["t"])), (chapter(t["t"]), 0)])
sheet(ws, ["ID", "Task", "Why", "Done when", "Note", "Owner", "Team", "Project", "Priority", "Due", "Status", "Done?", "Recording", "Chapter"], rows,
      [6, 50, 40, 34, 30, 26, 11, 20, 11, 16, 16, 8, 11, 36], 12)
ws = wb.create_sheet("Decisions")
sheet(ws, ["Decision", "Why", "Type", "Project", "Recording"],
      [[(d["text"], 0), (d.get("why", ""), 0), (d["kind"], 0), (PJ.get(d["project"], ""), 0), (fmt(d["t"]), at(d["t"]))] for d in D["decisions"]], [44, 60, 11, 20, 11], 4)
ws = wb.create_sheet("Open questions")
sheet(ws, ["Question", "Why it's open", "What settles it", "Who", "Next step", "Needs", "Recording"],
      [[(o["q"], 0), (o["why"], 0), (o["close"], 0), (", ".join(name(w) for w in o["who"]) or "Needs owner", 0), (o["next"], 0), (o["kind"], 0), (fmt(o["t"]), at(o["t"]))] for o in D["open"]],
      [40, 44, 36, 22, 26, 11, 11], 6)
ws = wb.create_sheet("Who watches what")
sheet(ws, ["Person", "Role", "What to watch", "Length", "Start"],
      [[(name(w["person"]), 0), (P.get(w["person"], {}).get("title", ""), 0), (lbl, 0), (f"{max(1, round((e - s) / 60))} min", 0), (fmt(s), at(s))] for w in D["watch"] for s, e, lbl in w["ranges"]],
      [18, 38, 44, 9, 11], 4)
ws = wb.create_sheet("Words")
sheet(ws, ["Word", "Meaning", "Captions heard", "Note"],
      [[(x["term"], 0), (x.get("meaning", ""), 0), (", ".join(x.get("heard", [])), 0), (x.get("note", ""), 0)] for x in D["terms"]], [20, 60, 30, 36], 0)
ws = wb.create_sheet("Spelling fixes")
sheet(ws, ["Heard as", "Fix", "Sure?", "Meaning", "Example", "Recording"],
      [[(s["heard"], 0), (s["fix"], 0), ("Yes" if s["sure"] else "Confirm", 0), (s["meaning"], 0), (s["example"], 0), (fmt(s["t"]), at(s["t"]))] for s in D["spelling"]],
      [24, 18, 9, 36, 50, 11], 5)
ws = wb.create_sheet("Clean transcript")
sheet(ws, ["Time", "Speaker", "Chapter", "Text"], [[("no time" if u.get("nt") else fmt(u["s"]), "" if u.get("nt") else at(u["s"])), (name(u["sp"]), 0), (chapter(u["s"]), 0), (u["text"], 0)] for u in utt], [10, 16, 34, 110], 0)
ws = wb.create_sheet("Meeting")
M = D["meta"]
for k, v in [("Title", M["title"]), ("Date", f'{M["date"]}, {M.get("start", "")}'), ("Medium", M.get("medium", "")), ("Place", M.get("place", "")),
             ("Duration", fmt(M["duration"])), ("Agenda", M.get("agenda", "")), ("Summary", D["summary"]["lead"] + " " + D["summary"].get("accent", "")),
             ("Why it happened", " ".join(v for v in [(D.get("context") or {}).get(k, "") for k in ("before", "call", "question")] if v)),
             ("What they decided", (D.get("context") or {}).get("decided", "")),
             ("What we could hear", " ".join(c.get("note", "") for c in M.get("coverage", []) if c.get("quality") != "good") or "Everything, with names and times"),
             ("Recording", M.get("recording", ""))]:
    ws.append([k, v])
ws.column_dimensions["A"].width = 14; ws.column_dimensions["B"].width = 100
for c in ws["A"]:
    c.font = Font(bold=True)
Path(args.xlsx).parent.mkdir(parents=True, exist_ok=True)
wb.save(args.xlsx)
D["meta"]["xlsx"] = Path(args.xlsx).name
D["xlsx_b64"] = base64.b64encode(Path(args.xlsx).read_bytes()).decode()

# ---------- html ----------
tpl = (HERE.parent / "assets" / "board-template.html").read_text(encoding="utf8")
title = (M.get("short") or M["title"]) + " Board"
html = tpl.replace("__TITLE__", title.replace("<", "")).replace("__DATA__", json.dumps(D, ensure_ascii=False).replace("</", "<\\/"))
Path(args.out).write_text(html, encoding="utf8")
print(f"board: {args.out} ({len(html)//1024} KB) | excel: {args.xlsx} | transcript {before} lines -> {len(utt)} turns, {fixes} fixes | photos: {len(D['photos'])}")
