# Meeting Board (Claude skill)

Turns a Teams meeting transcript into one visual board anyone can read in about 10 minutes: summary, action items with owners and dates, chapters with recording links, a clean transcript with hover previews, project diagrams, decisions with reasons, open questions, a watch list for people who missed the call, a 2-minute understanding check, and an Excel task file.

## Install (once, 1 minute)

**Option A, with git:**
```
git clone https://github.com/Lohith212-dev/meeting-board.git ~/.claude/skills/meeting-board
```
On Windows the folder is `C:\Users\<you>\.claude\skills\meeting-board`.

**Option B, without git:** on GitHub click **Code → Download ZIP**, unzip, rename the folder to `meeting-board` and move it into your `.claude/skills/` folder.

Then:
1. Make sure Python can write Excel files: `python -m pip install openpyxl`
2. Restart Claude Code.

## Use (every meeting)
1. In Teams, open the meeting recap → Transcript → **Download** (.docx). A `.vtt` caption file works too.
2. In Claude Code, type:
   ```
   /meeting-board "C:\path\to\Your Meeting.docx"
   ```
3. Answer the few questions it asks first: active projects, recording link, where tasks go, any new names.
4. Confirm the spelling fixes it lists.
5. You get the board link, the Excel file, and a Teams message to paste.

Share the board with your team at **Contributor** access, so everyone's check result is saved and you can see who has understood.

## Make it yours
- `config/team.json` ships with a **fictional example team** (company "Fernway"). Replace it with your people: name, title, what they care about. Add square photos as `config/photos/<id>.webp`; people without a photo get an initials circle.
- `config/glossary.json` learns caption fixes (e.g. "Zen desk" → "Zendesk"); `config/projects.json` keeps your projects and whether they're active.
- Try it first on the example: `examples/Weekly Product Sync.docx`.

All people and companies in the examples are fictional; the photos are AI-generated.
