# Publishing the board

## As a claude.ai Artifact (best)
Publish `board.html` with the Artifact tool and these capabilities:

```json
{"downloads": true,
 "user": {"scopes": ["profile"]},
 "db": {"rules": [{"path": "quiz", "read": "admin", "write": "owner"},
                  {"path": "quiz/{self}", "read": "interact", "write": "interact"}]}}
```

- `downloads` → the Excel button saves the task file (the viewer confirms the save).
- `db` + `user` → each person's check result is saved at `quiz/<their id>`; only the owner and editors see everyone's results (Check tab, "Who has checked").
- Sharing: in the artifact's Share menu give the team **Contributor** access. Viewers and commenters can read the board and take the check, but their result is not saved.
- After publishing, read the `quiz` collection once with ArtifactData (`list`) to confirm the store answers.
- Later meetings: publish a NEW artifact per meeting (one board per meeting), same capabilities.

## As a file (no claude.ai)
`board.html` works on its own in any browser. Without claude.ai the Excel button explains it is unavailable (the .xlsx sits next to the board), and quiz results are not saved.

## Video
Teams and Stream recordings cannot be embedded in an iframe. Every timestamp links to the recording with `?nav=` and `startTimeInSeconds`, so it opens at that second (people need access to the recording; Microsoft decides whether it autoplays).

## Teams message template
Keep it to 5-6 lines. Fill the brackets.

```
📋 [Meeting name], [date]: board is ready
[One-line governing thought from the summary]

👉 Board: [artifact link]
• Overview first (2 min), then your tab
• Missed the call? Your parts are in Watch list (~[N] min, not [total])
• Take the Check (2 min) so we know we're aligned
• Your tasks: [@name] [task] by [date] · [@name] [task] by [date]
```
