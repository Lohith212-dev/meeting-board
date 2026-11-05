# Changelog

## 2.0.0 (2026-11-05)

Rebuilt for the person who **missed** the meeting. Tested on a 15-minute call the reader did not attend: the v1 board only made sense to people who were there, so this version adds the context they lack and is honest about what it could not hear.

**Setup questions**
- Asks who reads the board, and who you and your team are (first use only), instead of asking a non-attendee which projects are active.
- Lists the projects it found and asks "do these look right?", with options to merge ("these three are one project"), rename, or go with the AI's list.
- When a picture is a guess (under 90% sure), asks for screenshots at exact timestamps, or the recording itself if it is under 15 minutes.

**Overview: a numbered reading path**
- How much of the call was heard clearly, with gaps marked "no time".
- Why the meeting happened: before, this call, the question, and what they decided (big and up front).
- Who's who, with why each person matters in this meeting.
- The idea in one picture, with a confidence level.
- What happened, in time order, with a short summary and the speaker's own words (photo, name, time) for each part.
- Where it landed: Decided, Floated not agreed, Still open, clearly labelled.
- What happens next: tasks with why and "done when".
- Your parts of the recording and the chapters, side by side. Words you'll hear. The check moved to the end.

**Other tabs**
- Projects: a stage ladder (Idea, Shaping, Planned, Building, Live) and what moves each project on. Counts jump to filtered decisions and tasks, with a Back button that returns to the same spot.
- Decisions: decisions and open questions together, grouped by project, filtered by project and status.
- Tasks: cards with context, filtered by project, owner and priority.
- Transcript: chapter summaries, gap and "on screen" notes, tags where each decision or task was said, "Key moments only", lines from a backup recorder merged in as "no time".
- Review: Accept all / Reject all / Edit for spelling, saved. Readers press **Fix** next to anything to correct the AI; the owner approves or rejects (one by one or all at once); approved fixes show on the board for everyone.
- Dotted words explain themselves on hover, everywhere.

**Build**
- `build_board.py` merges `untimed` lines, adds Why / Done when / Note columns and a Words sheet to the Excel, and prints `CHECK` lines for anything a newcomer would miss.
- New data fields: `meta.coverage`, `meta.reader`, `context`, `picture`, `terms`, `untimed`, `stages`, `people[].why`, chapter `summary` / `quotes` / `pills` / `onscreen` / `weak`, project `stage` / `next`, task `why` / `done` / `extra`. v1 files still build.

## 1.1.0
- Transcript tab: copy or download the whole clean transcript as Markdown.

## 1.0.0
- First release.
