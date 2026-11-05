# data.json schema (v2)

One JSON object. `t` and `e` are seconds from the meeting start (`e` = end of a range). Person ids and project ids are short lowercase slugs. A full example is in `examples/weekly-product-sync.data.json` (fictional company Fernway); copy its shape. Fields marked *v2* are new; a v1 file still builds, but `build_board.py` prints a `CHECK` line for each v2 field a reader who missed the call needs.

```jsonc
{
  "meta": {
    "title": "Weekly Product Sync",      // full title
    "short": "Product Sync",               // header + page title
    "date": "Tue 10 Nov 2026", "start": "09:30",
    "platform": "Teams",
    "medium": "Microsoft Teams (Meet now), recorded and transcribed",
    "place": "Remote",
    "duration": 4320,                      // seconds (last timestamp of the transcript)
    "agenda": "One line",
    "recording": "https://<tenant>.sharepoint.com/:v:/g/personal/...",  // "" if none
    "transcript": "file name of the .docx",
    "reader": "olivia",                    // v2: whose parts "For you" shows first (a person id with a watch entry)
    "coverage": [                          // v2: what the board could hear. Omit only if everything was captured
      {"start": 0,   "end": 54,  "quality": "good"},
      {"start": 54,  "end": 613, "quality": "weak", "note": "The middle 9 minutes come from a backup recorder with no names or times."},
      {"start": 613, "end": 921, "quality": "good"}
    ]
  },
  "people": [ {"id": "emma", "name": "Emma Clarke", "title": "CEO", "attended": true, "note": "Left at 49:50", "external": false, "aliases": ["Emma"],
               "why": "Ran the meeting and made the calls."} ],          // v2 why: why they matter in THIS meeting
  "summary": {"lead": "Governing thought, under 10 words.", "accent": "One supporting sentence."},
  "context": {                             // v2: why the meeting happened, for someone who wasn't there
    "before": "The backstory a newcomer needs.",
    "call": "What happened in this call, and who drove it.",
    "question": "What the meeting had to settle.",
    "decided": "The answer, in one or two sentences."
  },
  "picture": {                             // v2, optional: the meeting's one idea as a hub diagram
    "title": "The idea in one picture", "sub": "One line under the title",
    "confidence": 70,                      // under 90 shows "about 70% sure" and asks readers for help
    "reason": "Emma drew this on her screen, which wasn't recorded.",
    "ask": [30, 616],                      // timestamps to screenshot (step 2b)
    "top": {"label": "plug in as separate parts", "items": ["ICP research", "Product research"]},
    "hub": {"title": "One shared system", "sub": "Every team gets its data from one place"},
    "users": [ {"title": "Sales", "t": 759, "who": ["daniel"], "note": "SDRs", "items": ["Prep before a call", "Calls logged for them"]} ],  // 2-4 boxes
    "later": {"text": "Decided last: where the data comes from", "t": 664}
  },
  "chapters": [ {"n": 1, "start": 0, "end": 529, "project": "insights", "title": "Short title",
                 "t": 100,                                   // v2: the key moment (defaults to start)
                 "summary": "2-3 plain sentences of what happened.",   // v2
                 "pills": [{"text": "Agreed", "kind": "ok"}],  // v2: ok | mute | warn
                 "quotes": [{"sp": "emma", "t": 100, "text": "Exact words from the transcript."},
                            {"sp": "emma", "t": 54, "text": "...", "guess": true}],   // v2: guess = speaker not certain
                 "onscreen": "What was shown, if anything",  // v2
                 "weak": false,                              // v2: true if this part only exists in a backup recording
                 "note": "optional", "see": ["3 short lines"]} ],
  "terms": [ {"term": "ICP", "meaning": "Ideal customer profile: the kind of company we want to sell to.",   // v2
              "heard": ["I C P"], "note": "optional", "flag": false} ],   // flag: used in a special sense in this meeting
  "untimed": [ {"at": 54, "sp": "emma", "text": "A line from a backup recorder."} ],   // v2: build merges these into the transcript as "no time"; omit sp if unsure
  "stages": [ {"name": "Idea", "means": "Talked about, nothing agreed"}, {"name": "Shaping", "means": "..."},
              {"name": "Planned", "means": "..."}, {"name": "Building", "means": "..."}, {"name": "Live", "means": "..."} ],  // v2, optional; this is the default
  "projects": [ {
    "id": "insights", "name": "Insights", "aka": "Heard as In Sites in the captions",
    "what": "Two sentences: what it is, for whom.",
    "status": "Where it stands after this meeting.",
    "stage": "Building",                   // v2: one of stages[].name
    "next": "What moves it to the next stage.",  // v2
    "lead": "Who leads it",
    "map": {"badge": "Product", "blurb": "One line", "points": ["3-4 short items"], "open": "One open item (amber)", "cta": "See the journey"},
    "blocks": [ /* 2-4 visual blocks, see below */ ]
  } ],
  "links": [ {"from": "insights", "to": "pricing", "label": "needs a price from"} ],
  "mapRoot": {"title": "Fernway", "sub": "The one idea that ties the projects together"},
  "mapIntro": "One sentence under the concept map heading.",
  "decisions": [ {"text": "What was decided.", "why": "The reason given.", "t": 305, "kind": "Agreed|Proposed", "project": "insights", "by": "optional: who decided"} ],
  "open": [ {"q": "Question?", "why": "Why nobody can answer yet.", "close": "What would settle it.", "who": ["emma"], "next": "Next step.", "kind": "Research|Small test|Decision|Expert", "project": "insights", "t": 305} ],
  "tasks": [ {"id": "T1", "task": "Verb-first task", "owners": ["emma"], "suggested": "laura", "project": "insights",
              "priority": "now|next|proposed", "due": "18 Nov|TBC|Week 1", "status": "Agreed|Proposed|Idea|Open|Not started|Needs owner",
              "t": 332, "external": false, "top": true,
              "why": "Why it matters, in words a newcomer understands.",   // v2
              "done": "What finished looks like.",                         // v2
              "extra": {"label": "Blocks|Waits for|When|Note", "text": "..."} } ],   // v2, optional
  "watch": [ {"person": "olivia", "ranges": [[2900, 2990, "Why this part matters to them"]]} ],
  "notes": [ {"text": "Also worth knowing.", "t": 40} ],
  "spelling": [ {"heard": "Zen desk", "fix": "Zendesk", "sure": true, "meaning": "Short meaning", "example": "Sentence from the meeting", "t": 4600} ],
  "taskNote": "Optional sentence on the Tasks tab.",
  "quiz": {"pass": 5, "minutes": 2, "questions": [
    {"id": "q1", "q": "Question?", "options": ["A", "B", "C", "D"], "answer": 1, "why": "One-line explanation.",
     "review": {"tab": "decisions|tasks|projects|transcript|watch", "proj": "insights", "label": "Decisions", "t": 305, "e": 330}}
  ]}
}
```

`build_board.py` adds `transcript`, `clean`, `photos` and the embedded Excel, and turns `untimed` into transcript lines; do not write those yourself.

**Times inside a weak part.** Any timestamp that falls inside a `coverage` range whose quality is not `good` shows as "no time" on the board (it still opens that part of the transcript). Point items from the backup recorder at the gap's start.

## Visual blocks (`projects[].blocks`)

Pick the block that matches how the discussion was shaped. Every item can carry `t` (and `e`).

| type | Use for | Fields |
|---|---|---|
| `steps` | A journey or sequence with several facets per step | `label, title, note, items:[{title, sub, t, cols:[{label,text}]}]` |
| `flow` | A workflow of 3-8 steps, who does what | `label, title, note, items:[{title, t, rows:[{label,text}], tags:[], highlight}], meter:{label,value(0-100),t}, chips:{label, items:[], later, t}, quote` |
| `cards` | 2-4 parallel things | `label, title, t, e, intro, items:[{title, text, t, icon: video|doc|map|chat|check|user}], quote:{quote:true,text,t}` |
| `pair` | Two side-by-side cards of two items each | `items:[{label, title, t, e, items:[{title,text,t}]}]` (exactly 2) |
| `conflict` | A disagreement (Conflict Resolution Diagram) | `label, title, status, goal, sides:[{person, position, tp, because, tb}], way, tw` (exactly 2 sides) |
| `columns` | A plan in phases or weeks with owners | `label, title, note, items:[{label, title, text, people:[[id, role]], gate, t}], quote:{lead,text,t}` |
| `tiles` | 2-4 small fact cards | `items:[{label, title, text, list:[], t}]` |

## Tabs and where things show
- **Overview** (a numbered reading path): how much was heard → why the meeting happened (`context`) → who's who → the idea in one picture → what happened, in order (`chapters` with quotes) → where it landed (decided / floated / open) → what happens next (`top` tasks) → your parts and chapters → words (`terms`) → also worth knowing → the check.
- **Projects**: concept map, each project's stage ladder, and counts that jump to its filtered decisions and tasks, with a Back button.
- **Decisions**: decisions and open questions together, grouped by project, filtered by project and status.
- **Tasks**: cards with why and done, filtered by project, owner and priority.
- **Transcript**: chapter summaries, gap notes, "on screen" notes, key-moment tags, "Key moments only", search, copy or download as Markdown.
- **Watch list**, **Review** (spelling with Accept all / Reject all / Edit; readers' fixes and the owner's approvals), **Check** (quiz and results).

## Fix keys
Every claim a reader can correct has a key. Approved fixes are stored under these keys (`reviewed` collection) and shown at that spot:
`hero`, `ctx-before|call|question|decided`, `picture`, `person-<id>`, `ch-<n>`, `dec-<index>`, `open-<index>`, `task-<id>`, `term-<index>`, `note-<index>`, `proj-<id>`, `line-<transcript index>`.
