# Publishing the board

## As a claude.ai Artifact (best)
Publish `board.html` with the Artifact tool and these capabilities:

```json
{"downloads": true,
 "user": {"scopes": ["profile"]},
 "db": {"rules": [{"path": "quiz", "read": "admin", "write": "owner"},
                  {"path": "quiz/{self}", "read": "interact", "write": "interact"},
                  {"path": "fixes", "read": "admin", "write": "owner"},
                  {"path": "fixes/{self}", "read": "interact", "write": "interact"},
                  {"path": "reviewed", "read": "view", "write": "admin"},
                  {"path": "review", "read": "view", "write": "admin"}]}}
```

- `downloads` → the Excel button and "Download transcript" save files (the viewer confirms the save).
- `quiz` → each person's check result is saved at `quiz/<their id>`; only the owner and editors see everyone's results (Check tab, "Who has checked").
- `fixes` → a reader presses **Fix** next to anything on the board (a word, a transcript line, a decision, a task, the picture) and writes what is right. Their fixes are saved at `fixes/<their id>`; only the owner and editors see everyone's.
- `reviewed` → the owner or an editor approves or rejects each fix in the Review tab (one by one, or Approve all / Reject all). Everyone can read this collection, so approved fixes show on the board at the spot they correct, marked "Corrected".
- `review` → the owner's spelling decisions (`review/spelling`: Accept all / Reject all / Edit), kept for the next meeting.
- Sharing: in the artifact's Share menu give the team **Contributor** access. Viewers and commenters can read the board, but their check results and fixes are not saved.
- After publishing, list `quiz`, `fixes` and `reviewed` once with ArtifactData to confirm the store answers.
- Applying fixes: see SKILL.md step 8. Read `reviewed` and `review/spelling`, fold them into data.json and glossary.json, rebuild, and publish to the same URL. Stored data survives a republish.
- Later meetings: publish a NEW artifact per meeting (one board per meeting), same capabilities.

## As a file (no claude.ai)
`board.html` works on its own in any browser. Without claude.ai the Excel button explains it is unavailable (the .xlsx sits next to the board), and quiz results, fixes and spelling decisions are not saved.

## Video
Teams and Stream recordings cannot be embedded in an iframe. Every timestamp links to the recording with `?nav=` and `startTimeInSeconds`, so it opens at that second (people need access to the recording; Microsoft decides whether it autoplays). Parts that only exist in a backup recording show "no time" and open the transcript instead.

## Teams message template
Keep it to 5-6 lines. Fill the brackets.

```
📋 [Meeting name], [date]: board is ready
[One-line governing thought from the summary]

👉 Board: [artifact link]
• Missed the call? Read the Overview top to bottom (~[N] min, not [total])
• See something wrong? Hover it and press Fix
• Take the Check at the end (2 min) so we know we're aligned
• Your tasks: [@name] [task] by [date] · [@name] [task] by [date]
```
