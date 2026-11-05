---
name: meeting-board
description: Turns a Microsoft Teams meeting transcript (.docx or .vtt) into a visual, tabbed meeting board anyone can read in about 10 minutes - summary, outcomes, action items with owners, chapters with recording timestamps, a clean transcript with hover previews, project diagrams, decisions with reasons, open questions, a per-person watch list, an understanding check (quiz) with saved results, and an Excel task file. Use when the user types /meeting-board, shares a meeting transcript or recording link and asks for action items, minutes, a summary, a board, "what did we decide", "who owns what", or a catch-up for people who missed the call.
---

# Meeting Board

You turn one meeting transcript into one board. The reader is a busy colleague, often someone who missed the call. Everything you produce must be accurate, short, visual and in plain English.

`<skill>` = the folder that holds this file.

## The rules that matter most

1. **Read the whole transcript.** Every line, start to end, before you write anything. Never summarise from the first and last pages. Long meetings hide the most important topics in the middle.
2. **Ask before you build, all at once.** One round of questions (step 2), never questions scattered later or placed on the board.
3. **Never invent.** No owners, dates, numbers or decisions the meeting did not state. Unknown owner → "Needs owner" (optionally `suggested`). Unknown date → `TBC`. Something proposed but not agreed → `Proposed`.
4. **Pictures, not paragraphs.** Each project gets diagrams (journey, workflow, conflict, plan, tiles), built with thinking frameworks (`references/analysis-guide.md`). Text is labels and short sentences.
5. **Everything links back.** Every claim carries the timestamp (seconds) where it was said, so the board can preview the transcript and open the recording at that second.
6. **Plain words.** Short sentences. No jargon the team wouldn't say out loud. Keep chat replies short, too.

## Workflow

### 1. Get the inputs
- The transcript: a Teams `.docx` (Download transcript in the meeting recap) or a `.vtt`. If the user gave none, ask for it.
- Make a work folder next to the transcript: `<transcript folder>/<meeting-slug>-board/`.
- Extract it: `python "<skill>/scripts/extract_transcript.py" "<transcript>" "<work>/transcript.txt"`.
- Read `transcript.txt` completely (use several Read calls for long files; do not skip ranges).
- Read `<skill>/config/team.json`, `config/projects.json`, `config/glossary.json`.

### 2. Ask the up-front questions (one AskUserQuestion call, up to 4 questions)
1. **Active projects** (multi-select): the known projects from `projects.json` plus any new ones you spotted in the transcript. Tasks are tagged only to active projects.
2. **Recording**: "Paste the Teams or SharePoint recording link, so every timestamp opens the video at that second" (options: "I'll paste it" / "No recording link"). Iframes are impossible (Microsoft and the artifact viewer both block them), so never promise an embedded player.
3. **Where tasks go**: Excel is always made. Options: "Excel only" / "Excel + Loop table" / "Excel + another tool (paste link)". If they give a link and a matching connector is available (Asana, monday.com, Notion, Linear, Atlassian, Microsoft 365), add the tasks there after the board is built; otherwise say plainly it stays in Excel.
4. **People check**, only if speakers or names in the transcript are not in `team.json`: who are they and what is their role?
Save the answers (update `projects.json` statuses, add new people to `team.json`).

### 3. Spelling check (step 1 of the review)
Captions mangle names, products and acronyms. Build the `spelling` list (see schema): every suspicious word with its likely fix, meaning, the sentence it appeared in, and its timestamp. Use `glossary.json` first: known `fixes` are applied automatically; `keep` words are not errors. Mark guesses `sure: false` and ask the user to confirm them in chat (short list). Add confirmed fixes to `glossary.json` so the next meeting is cleaner. Hindi or other languages mixed in are not errors.

### 4. Analyse and write `data.json`
Follow `references/data-schema.md` exactly and `references/analysis-guide.md` for how to think. In short:
- **Chapters**: 4-8 topic blocks covering the whole meeting, start/end seconds, a title and 3 "what you'll see" lines, tagged to a project.
- **Summary**: Minto pyramid. One governing sentence (`lead`), one supporting sentence (`accent`), four outcomes (`points`), each with a project and a timestamp.
- **Projects**: what it is, status, lead, a concept-map card (`map`) and 2-4 visual `blocks`. Show how projects connect (`links`).
- **Decisions** with the reason given. **Open questions** with why they're open, what would settle them, who, next step, and what kind of help they need (Research / Small test / Decision / Expert, from Cynefin).
- **Tasks**: owner(s), project, priority (`now` / `next` / `proposed`, Eisenhower), due, status, timestamp. Mark 3-4 as `top` for the overview. External people's tasks get `external: true`.
- **Watch list**: for each person who was NOT on the call but is affected, the time ranges they should watch and why, based on their role in `team.json` (`cares_about`). Aim for under 10 minutes each.
- **Quiz** (the understanding check): 5-7 multiple-choice questions on the decisions, owners, dates and open questions that matter most. One clearly right answer, three plausible wrong ones, a one-line `why`, and a `review` pointer (tab, optional project, timestamp range) to the exact part to re-read. Pass mark: all but one.
- **Notes**: 4-6 "also worth knowing" lines that fit nowhere else.
Timestamps are seconds from the start; use the first line of the relevant speaker turn.

### 5. Build
```
python "<skill>/scripts/build_board.py" --data "<work>/data.json" --transcript "<work>/transcript.txt" --out "<work>/board.html" --xlsx "<work>/<Meeting> <YYYY-MM-DD> - tasks.xlsx"
```
Needs `openpyxl` (`python -m pip install openpyxl`). Fix any WARNING it prints (unknown speakers → add aliases to `team.json` or `people`).

### 6. Check it before showing anyone
Serve the folder (`python -m http.server` in `<work>`) and open it with a browser tool if one is available: click every tab, hover one timestamp, open one side panel, answer the quiz once, switch a project, press "Copy as Markdown" on the Transcript tab. No console errors, no empty tabs. If no browser tool exists, at least run the page script through `node -e "new Function(...)"` to catch syntax errors.

### 7. Publish and hand over
- Publish `board.html` as an Artifact with these capabilities (they power the Excel download and the saved quiz results):
  `{"downloads": true, "user": {"scopes": ["profile"]}, "db": {"rules": [{"path": "quiz", "read": "admin", "write": "owner"}, {"path": "quiz/{self}", "read": "interact", "write": "interact"}]}}`
  Tell the user: share the board with the team at **Contributor** access so each person's check result is saved; the owner sees everyone's results in the Check tab. See `references/publishing.md`.
- If tasks go to another tool (step 2), add them now and say where.
- Reply in chat with: the board link, the Excel path, and a ready-to-paste Teams message (template in `references/publishing.md`). Max 6 short lines plus the message.

## Files

| Path | What |
|---|---|
| `scripts/extract_transcript.py` | .docx / .vtt → `transcript.txt` (`Name   m:ss text` lines) |
| `scripts/build_board.py` | data.json + transcript → `board.html` + Excel (cleans transcript, maps speakers, embeds photos) |
| `assets/board-template.html` | The board app (Vercel Geist look, tabs, hover previews, side panel, quiz, Excel download, transcript copy/download as Markdown). Do not edit per meeting; all content comes from data.json |
| `references/data-schema.md` | Every field of data.json, with types and an example |
| `references/analysis-guide.md` | How to chapter, summarise, pick visuals, write decisions, open questions, watch lists and quiz questions; the thinking frameworks |
| `references/publishing.md` | Artifact capabilities, sharing levels, the Teams message template |
| `config/team.json` | People, titles, aliases, what each person cares about; `photos/<id>.webp`. Ships with a fictional example team: replace it |
| `config/projects.json` | Known projects and their status |
| `config/glossary.json` | Caption fixes learned so far |
| `examples/` | A complete fictional example: `Weekly Product Sync.docx` and its `weekly-product-sync.data.json` (company "Fernway"). Build it to see the board |
