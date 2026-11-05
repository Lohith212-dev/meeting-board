---
name: meeting-board
description: Turns a meeting transcript (Teams .docx or .vtt, plus an optional backup recording's text) into a visual, tabbed meeting board that someone who missed the call can understand in under 10 minutes and trust enough not to watch the recording - why the meeting happened, who's who, the idea in one picture, the story in time order with quotes, what was decided, floated and left open, tasks with why and "done when", per-person watch lists, words explained on hover, a clean transcript with key moments, project stages, reader corrections the owner approves, an understanding check and an Excel task file. Use when the user types /meeting-board, shares a meeting transcript or recording link and asks for action items, minutes, a summary, a board, "what did we decide", "who owns what", or a catch-up for people who missed the call.
---

# Meeting Board (v2)

You turn one meeting transcript into one board. **The reader missed the call.** They don't know the people, the projects, the words the team uses or what was on screen. If the board only makes sense to someone who was there, it has failed: they will go back to the recording. Everything you produce must be accurate, short, visual, in plain English, and honest about what you could not hear.

`<skill>` = the folder that holds this file.

## The rules that matter most

1. **Read the whole transcript.** Every line, start to end, before you write anything. Long meetings hide the most important topics in the middle.
2. **Write for the person who missed it.** Say why the meeting happened before what it decided. Explain every person, project and team word the first time it appears (`terms`). A task must make sense to someone who read nothing else.
3. **Say what you couldn't hear.** Gaps in the captions, a second recorder with no names or times, a shared screen nobody recorded: put them in `meta.coverage`, mark those parts, and lower your confidence. Never smooth over a gap.
4. **Ask before you build, in one round.** Step 2. Ask about the reader, not about things only an attendee would know. The one exception is step 2b (an unsure picture).
5. **Never invent.** No owners, dates, numbers or decisions the meeting did not state. Unknown owner → "Needs owner" (optionally `suggested`). Unknown date → `TBC`. Floated but not agreed → `Proposed`. A guessed speaker → `guess`.
6. **Pictures, not paragraphs. Time order, not importance order.** The story runs in the order it happened, with the strongest quote of each part and the speaker's photo.
7. **Everything links back.** Every claim carries the timestamp (seconds) where it was said.
8. **Plain words.** Short sentences. Keep chat replies short, too.

## Workflow

### 1. Get the inputs
- The transcript: a Teams `.docx` (Download transcript in the meeting recap) or a `.vtt`. If the user gave none, ask for it. A second recording's text (no timestamps, no names) is welcome: use it to fill gaps (step 4, `untimed`).
- Make a work folder next to the transcript: `<transcript folder>/<meeting-slug>-board/`.
- Extract it: `python "<skill>/scripts/extract_transcript.py" "<transcript>" "<work>/transcript.txt"`.
- Read `transcript.txt` completely (several Read calls for long files; do not skip ranges). Read any second recording completely too.
- Read `<skill>/config/team.json`, `config/projects.json`, `config/glossary.json`. If `team.json` still says EXAMPLE in `about`, you don't know the user's team yet.
- Note while reading: gaps in the timestamps (a jump of several minutes with no lines), garbled names, and moments where someone points at a screen ("as you can see", "this block here").

### 2. Ask the up-front questions (one AskUserQuestion call, up to 4 questions)
Ask about the reader and the context, never "which of these projects are active?" to someone who may not know.
1. **Who reads the board?** "People who missed the call (Recommended)" / "People who were there" / "Both". For people who missed it, explain more and write the `context` block carefully.
2. **About you and your team.** Only when `team.json` is the example or the user is not in it: "Who are you, and what do you care about?" and, on first use, "Paste your team: name, role, what they care about (or skip and I'll use the names in the transcript)". Save the answers to `team.json` and set `meta.reader`. When the team is already known, use this slot for **where tasks go**: Excel is always made; options "Excel only" / "Excel + Loop table" / "Excel + another tool (paste link)".
3. **The projects you found.** List what you identified: "I found these projects in the call: A, B, C. Do they look right?" Options: "Yes, looks right" / "Some are one project (tell me which)" / "Rename or remove some" / "I don't know these: go with your list". Merge, rename or drop as told. If the user doesn't know, go ahead with your list and say in `projects[].aka` or `status` that it is the AI's reading.
4. **Recording**: "Paste the Teams or SharePoint recording link, so every timestamp opens the video at that second" (options: "I'll paste it" / "No recording link"). Iframes are impossible, so never promise an embedded player.
Unknown names in the transcript: don't ask a non-attendee to identify them. Put them in `people` with `title: "Role not said"` and let readers correct them on the board.

### 2b. When a picture is a guess (only if needed)
If the meeting was built around something on screen (a diagram, a prototype, a slide) and you are **less than 90% sure** your `picture` matches it, ask once more before building:
"Part of this meeting was on a shared screen I can't see. Do you have the recording?" Options:
- "Yes, I'll send screenshots": give the exact timestamps (`picture.ask`), e.g. "0:30 and 10:16". Read the screenshots and redraw.
- "Yes, it's under 15 minutes: I'll send the file": extract frames yourself at those times, e.g. `ffmpeg -ss 30 -i "<recording>" -frames:v 1 "<work>/frame-0030.png"` (one per timestamp), read them and redraw.
- "No, go with your best guess": build it with `confidence` set honestly and `reason` saying what was not seen. The board shows "about N% sure" and lets readers correct it.

### 3. Spelling and words (step 1 of the review)
Captions mangle names, products and acronyms. Build the `spelling` list (see schema): every suspicious word with its likely fix, meaning, the sentence it appeared in, and its timestamp. Use `glossary.json` first: known `fixes` are applied automatically; `keep` words are not errors. Mark guesses `sure: false` and ask the user to confirm them in chat (short list). Add confirmed fixes to `glossary.json`. Other languages mixed in are not errors.
Then write `terms`: every acronym, product, client, team word or word used in a special sense that a newcomer would trip on, with a plain meaning and what the captions heard. Flag (`flag: true`) any word the team uses differently from its usual meaning. The board explains these on hover everywhere they appear, and a reader can correct one word in one place.

### 4. Analyse and write `data.json`
Follow `references/data-schema.md` exactly and `references/analysis-guide.md` for how to think. In short:
- **meta.coverage**: which seconds were heard clearly (`good`) and which only come from a backup recorder or not at all (`weak`), with a one-line `note`.
- **untimed**: lines from a backup recording that fill a gap, placed at the gap's start (`at`), with `sp` only if you are sure who spoke.
- **summary** (`lead`, `accent`) and **context**: `before` (the backstory), `call` (what happened in this call), `question` (what it had to settle), `decided` (the answer, in one or two sentences).
- **people[].why**: why each person matters in this meeting, not only their title.
- **picture** (optional): the one idea of the meeting as a hub diagram, with `confidence` and `ask` timestamps.
- **chapters**: 4-8 blocks in time order covering the whole meeting, each with `summary` (2-3 plain sentences), `t` (the key moment), `pills` (Agreed / Idea / still open), 1-2 `quotes` with the speaker (`guess` when unsure), `onscreen` when something was shown, `weak: true` when it comes from the backup recording.
- **projects** with `stage` (from `stages`) and `next` (what moves it to the next stage), plus the concept-map card and 2-4 visual `blocks`.
- **decisions** (`Agreed` / `Proposed` with the reason) and **open questions** (why open, what settles it, who, next step, kind of help).
- **tasks**: verb first, owner(s), project, priority, due, status, timestamp, plus `why` and `done` (always) and `extra` (what it blocks or waits for). Mark 3-4 as `top`.
- **watch**: for each person NOT on the call but affected, 1-3 ranges and why, under 10 minutes. `meta.reader` picks whose parts the overview shows first.
- **quiz**: 5-7 questions with a `review` pointer. It sits at the end of the board, after reading.
- **notes**: 3-6 "also worth knowing" lines.
Timestamps are seconds from the start; use the first line of the relevant speaker turn.

### 5. Build
```
python "<skill>/scripts/build_board.py" --data "<work>/data.json" --transcript "<work>/transcript.txt" --out "<work>/board.html" --xlsx "<work>/<Meeting> <YYYY-MM-DD> - tasks.xlsx"
```
Needs `openpyxl` (`python -m pip install openpyxl`). Fix every `WARNING` (unknown speakers → add aliases to `team.json` or `people`) and every `CHECK` line (a missing context, chapter summary, task why/done, terms, or an unsure picture with no screenshot times).

### 6. Check it as someone who missed the call
Serve the folder (`python -m http.server` in `<work>`) and open it with a browser tool if one is available. Read the Overview top to bottom as a stranger: does it say why the meeting happened, who everyone is, and what each word means? Then click every tab, hover one dotted word and one timestamp, open one side panel, press a project's "decisions" count and the "Back" button, filter Decisions and Tasks, turn on "Key moments only" in the Transcript, press Accept all in Review, answer the quiz once. No console errors, no empty tabs, nothing wider than a phone screen. Without a browser tool, at least run the page script through `node -e "new Function(...)"`.

### 7. Publish and hand over
- Publish `board.html` as an Artifact with the capabilities in `references/publishing.md` (Excel download, saved quiz results, reader fixes the owner approves, the spelling review).
- After publishing, list the `quiz`, `fixes` and `reviewed` collections once with ArtifactData to confirm the store answers.
- Tell the user: share at **Contributor** access so check results and fixes are saved; fixes wait in the Review tab for the owner (or an editor) to approve, and approved ones show on the board for everyone.
- If tasks go to another tool (step 2), add them now and say where.
- Reply in chat with: the board link, the Excel path, and a ready-to-paste Teams message (template in `references/publishing.md`). Max 6 short lines plus the message.

### 8. Apply readers' fixes (later, when asked)
When the user says "apply the fixes" or before building the next board from the same team:
- Read the artifact's `reviewed` collection (approved fixes) and the `review/spelling` document with ArtifactData.
- Fold them in: word fixes into `terms` and `glossary.json` (`fixes`), spelling decisions into `glossary.json`, other fixes into the right field of `data.json` (key `task-T3` → that task, `ch-2` → chapter 2, `line-14` → transcript line 14, `person-x` → that person, and so on).
- Rebuild and publish to the same URL. Stored fixes and check results survive a republish.

## Files

| Path | What |
|---|---|
| `scripts/extract_transcript.py` | .docx / .vtt → `transcript.txt` (`Name   m:ss text` lines) |
| `scripts/build_board.py` | data.json + transcript → `board.html` + Excel (cleans the transcript, merges untimed lines, maps speakers, embeds photos, checks the v2 fields) |
| `assets/board-template.html` | The board app. Do not edit per meeting; all content comes from data.json |
| `references/data-schema.md` | Every field of data.json, with types and an example |
| `references/analysis-guide.md` | How to write for someone who missed the call: context, chapters, quotes, pictures, decisions, tasks, words, watch lists, the quiz |
| `references/publishing.md` | Artifact capabilities, sharing levels, fixes and approval, the Teams message template |
| `config/team.json` | People, titles, aliases, what each person cares about; `photos/<id>.webp`. Ships with a fictional example team: replace it |
| `config/projects.json` | Known projects, their status and stage |
| `config/glossary.json` | Caption fixes learned so far |
| `examples/` | A complete fictional example: `Weekly Product Sync.docx` and its `weekly-product-sync.data.json` (company "Fernway"). Build it to see the board |
| `CHANGELOG.md` | What changed in each version |
