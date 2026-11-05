# Meeting Board (Claude skill)

Turns a Teams meeting transcript into one visual board that someone who **missed the call** can understand in under 10 minutes, without going back to the recording: why the meeting happened, who's who, the idea in one picture, what happened in time order with the speakers' own words, what was decided, floated and left open, tasks with why and "done when", words explained on hover, a clean transcript with key moments, project stages, corrections from readers, a 2-minute check at the end, and an Excel task file.

**Version 2.** See [CHANGELOG.md](CHANGELOG.md) for what changed.

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
3. Answer the few questions it asks first: who reads the board, who you and your team are (first time only), whether the projects it found look right (merge or rename them, or let it decide), and the recording link. If part of the meeting was on a screen it couldn't see, it asks for screenshots at exact times.
4. Confirm the spelling fixes it lists.
5. You get the board link, the Excel file, and a Teams message to paste.

On the board's Transcript tab, **Copy as Markdown** and **Download transcript** give you the whole clean transcript as Markdown (a `.md` file), with chapters, timestamps and speaker names.

**Claude Desktop or claude.ai (no Claude Code):** zip the `meeting-board` folder, then upload it in Settings → Capabilities → Skills (turn on "Code execution and file creation" first). Attach the transcript in a chat and ask for a meeting board. Changes Claude makes to `config/` there are not kept between chats, so put your team, photos, projects and glossary into `config/` **before** zipping. Without them the board has no photos and asks who your team is every time.

Share the board with your team at **Contributor** access, so everyone's check result is saved and you can see who has understood.

**Readers can correct the AI.** Anyone can hover a word, a transcript line, a decision or a task and press **Fix**. Fixes wait in the Review tab for you to approve (one by one or all at once); approved ones show on the board for everyone. Later, ask Claude to "apply the fixes" and it folds them into the board and your glossary.

## Make it yours
- `config/team.json` ships with a **fictional example team** (company "Fernway"). Replace it with your people: name, title, what they care about. Add square photos as `config/photos/<id>.webp`; people without a photo get an initials circle.
- `config/glossary.json` learns caption fixes (e.g. "Zen desk" → "Zendesk"); `config/projects.json` keeps your projects and whether they're active.
- Try it first on the example: `examples/Weekly Product Sync.docx`.

All people and companies in the examples are fictional; the photos are AI-generated.
