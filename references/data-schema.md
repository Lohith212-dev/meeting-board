# data.json schema

One JSON object. `t` and `e` are seconds from the meeting start (`e` = end of a range). Person ids and project ids are short lowercase slugs. A full real example is in `examples/weekly-product-sync.data.json` (fictional company Fernway); copy its shape.

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
    "transcript": "file name of the .docx"
  },
  "people": [ {"id": "emma", "name": "Emma Clarke", "title": "CEO", "attended": true, "note": "Left at 49:50", "external": false, "aliases": ["Emma"]} ],
  "projects": [ {
    "id": "insights", "name": "Insights", "aka": "Heard as In Sites in the captions",
    "what": "Two sentences: what it is, for whom.",
    "status": "Where it stands after this meeting.",
    "lead": "Who leads it",
    "map": {"badge": "Product", "blurb": "One line", "points": ["3-4 short items"], "open": "One open item (amber)", "cta": "See the journey"},
    "blocks": [ /* 2-4 visual blocks, see below */ ]
  } ],
  "links": [ {"from": "insights", "to": "pricing", "label": "needs a price from"} ],   // arrows between adjacent projects on the concept map
  "mapRoot": {"title": "Fernway", "sub": "The one idea that ties the projects together"},
  "mapIntro": "One sentence under the concept map heading.",
  "summary": {
    "lead": "Governing thought, under 10 words.",
    "accent": "One supporting sentence.",
    "points": [ {"project": "insights", "t": 305, "title": "3-5 words", "text": "One or two sentences."} ]   // exactly 4
  },
  "chapters": [ {"n": 1, "start": 0, "end": 529, "project": "insights", "title": "Short title", "note": "optional", "see": ["3 short lines"]} ],
  "decisions": [ {"text": "What was decided.", "why": "The reason given.", "t": 305, "kind": "Agreed|Proposed", "project": "insights"} ],
  "open": [ {"q": "Question?", "why": "Why nobody can answer yet.", "close": "What would settle it.", "who": ["emma"], "next": "Next step.", "kind": "Research|Small test|Decision|Expert", "project": "insights", "t": 305} ],
  "tasks": [ {"id": "T1", "task": "Verb-first task", "owners": ["emma"], "suggested": "laura", "project": "insights",
              "priority": "now|next|proposed", "due": "18 Nov|TBC|Week 1", "status": "Agreed|Proposed|Idea|Open|Not started|Needs owner",
              "t": 332, "external": false, "top": true} ],
  "watch": [ {"person": "olivia", "ranges": [[2900, 2990, "Why this part matters to them"]]} ],   // people who missed the call
  "notes": [ {"text": "Also worth knowing.", "t": 40} ],
  "spelling": [ {"heard": "Zen desk", "fix": "Zendesk", "sure": true, "meaning": "Short meaning", "example": "Sentence from the meeting", "t": 4600} ],
  "taskNote": "Optional sentence under the task table.",
  "quiz": {"pass": 5, "minutes": 2, "questions": [
    {"id": "q1", "q": "Question?", "options": ["A", "B", "C", "D"], "answer": 1, "why": "One-line explanation.",
     "review": {"tab": "decisions|tasks|projects|transcript|watch", "proj": "insights", "label": "Decisions", "t": 305, "e": 330}}
  ]}
}
```

`build_board.py` adds `transcript`, `clean`, `photos` and the embedded Excel; do not write them yourself.

## Visual blocks (`projects[].blocks`)

Pick the block that matches how the discussion was shaped. Every item can carry `t` (and `e`).

| type | Use for | Fields |
|---|---|---|
| `steps` | A journey or sequence with several facets per step (customer journey, onboarding) | `label, title, note, items:[{title, sub, t, cols:[{label,text}]}]` (first col is highlighted; 2-3 cols) |
| `flow` | A workflow of 3-8 steps, who does what (process, pipeline) | `label, title, note, items:[{title, t, rows:[{label,text}], tags:[], highlight}], meter:{label,value(0-100),t}, chips:{label, items:[], later, t}, quote` |
| `cards` | 2-4 parallel things (inputs, options, components) | `label, title, t, e, intro, items:[{title, text, t, icon: video|doc|map|chat|check|user}], quote:{quote:true,text,t}` |
| `pair` | Two side-by-side cards of two items each (idea vs idea, us vs competitor) | `items:[{label, title, t, e, items:[{title,text,t}]}]` (exactly 2) |
| `conflict` | A disagreement (Conflict Resolution Diagram) | `label, title, status, goal, sides:[{person, position, tp, because, tb}], way, tw` (exactly 2 sides) |
| `columns` | A plan in phases or weeks with owners | `label, title, note, items:[{label, title, text, people:[[id, role]], gate, t}], quote:{lead,text,t}` (`"all"` = everyone) |
| `tiles` | 2-4 small fact cards (who / when / what / measure) | `items:[{label, title, text, list:[], t}]` |

## Tabs and where things show
- **Overview**: meeting details (collapsed), summary + 4 outcomes, the check call-out, top tasks (`top: true`), watch list, chapters, notes.
- **Transcript**: clean transcript by chapter, search. **Projects**: concept map + blocks. **Decisions**: decided + open. **Tasks**: table + Excel. **Watch list**. **Check**: quiz + owner results. **Review**: spelling check.
