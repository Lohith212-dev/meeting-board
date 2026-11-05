# How to analyse a meeting

The board exists so that someone who **missed** the call knows, in under 10 minutes: why it happened, what was decided, what is still open, what they must do, and which few minutes of the recording (if any) they should watch. The test: after reading the Overview, would they still feel they need the recording? If yes, something is missing.

## 0. Read it as an outsider
- Read the full transcript once without writing. Then read it again as someone new to the team: underline every name, project, acronym and team word they would not know. Those become `people[].why` and `terms`.
- Mark the gaps: a jump of minutes with no lines, a second recorder with no names or times, a moment that only makes sense with a screen ("this block here", "as you can see"). Those become `meta.coverage`, `untimed`, chapter `weak` and `onscreen`, and they lower your confidence in any picture.
- Team words often mean something special. If a word is used differently from its usual meaning (for example "R&D" meaning leadership, product and finance), flag it in `terms`.

## 1. Context first (situation, problem, question, answer)
The reader needs the setup before the answer. Write `context`:
- `before`: what was going on before the call (one or two sentences).
- `call`: what happened in this call and who drove it.
- `question`: what the meeting had to settle.
- `decided`: the answer, short enough to read in one breath.
Then `summary.lead` (the governing thought, under 10 words) and `summary.accent` (the sentence that makes it concrete). Test: could a stranger retell why the meeting happened and how it ended from these lines?

## 2. Chapters, in time order
- Mark where the topic changes: a question, "now", "one more thing", a screen share, a new project name. 4-8 chapters that cover the whole meeting, in the order they happened.
- Each chapter: a title a colleague would use, `summary` (2-3 plain sentences: what was said and where it landed), `t` (the key moment), `pills` (Agreed / Idea, not agreed / still open), and 1-2 `quotes`: the exact words that carry the part, with the speaker. Copy quotes from the transcript; never polish them into something nobody said. If the speaker is not certain (no names in that recording), set `guess`.
- `onscreen` when something was shown. `weak: true` when the chapter only exists in a backup recording. `note` when someone reads an AI or a document aloud, so readers know it is a sample, not agreement.

## 3. The picture (only when the meeting had one idea at its centre)
- If the meeting revolved around one system, plan or diagram, draw it as `picture`: what plugs in on top, the hub, the 2-4 groups or steps it serves, and what comes later.
- Be honest about `confidence`. Built only from what was said about a screen you can't see? Probably 60-80%. Under 90%: ask for screenshots or the recording (SKILL.md step 2b) and fill `reason` and `ask`.
- Leave it out when the meeting was a list of unrelated topics.

## 4. Project pictures (frameworks behind the blocks)
| What the discussion looked like | Block | Framework |
|---|---|---|
| "The user goes from A to B to C, and at each step…" | `steps` | Customer journey |
| "First this happens, then the system does…" | `flow` | Process / issue tree |
| "Two people want different things" | `conflict` | Conflict Resolution Diagram (shared goal, two positions, the need behind each, way forward) |
| "Week one… week two… then we scale" | `columns` | Phased plan with gates |
| "We need three things from the customer" | `cards` | Concept list |
| "Our idea vs theirs" | `pair` | Comparison |
| "Who to target, when, with what, measured how" | `tiles` | Fact sheet |
| How projects relate to each other | concept map (`map`, `links`) | Concept map |

Give each project a `stage` (Idea, Shaping, Planned, Building, Live by default) and `next`: what has to happen to move it on. "Idea stage" alone means nothing to a reader; the ladder shows where it sits and what comes next.

## 5. Decisions vs proposals (Ladder of inference)
- A decision needs someone with authority agreeing out loud. Write the reason they gave (`why`).
- An idea someone floated, or a plan an AI drafted and read out, is `Proposed` ("Floated, not agreed" on the board).
- Facts heard vs assumptions: if the meeting assumed it, say "assumed" in `why`.

## 6. Open questions (Cynefin)
For each unresolved point: why it's open, what would settle it, who, next step, and `kind`:
- `Research`: the answer exists but nobody has it yet.
- `Small test`: complex; only trying it will tell.
- `Expert`: complicated; someone who knows can answer.
- `Decision`: options are clear; someone just has to choose.

## 7. Tasks that make sense on their own (Eisenhower)
- Verb first, one outcome per task, owner(s) as said in the meeting.
- Never point at something the reader can't see: not "go through Emma's idea" but "Read Emma's pricing idea (pictured on the board) and come back with questions".
- Always `why` (why it matters, in plain words) and `done` (what finished looks like). Add `extra` when it blocks or waits for something.
- `now` = urgent and important. `next` = important, not urgent. `proposed` = from a draft nobody committed to.
- `top: true` on the 3-4 that matter most this week. External people get `external: true`.

## 8. Watch list (who should watch what)
- Only people who were not on the call, or who joined late or left early (for the part they missed).
- Use `team.json → cares_about` and their role. 1-3 ranges each, each 1-6 minutes, each with a reason in their language.
- Target: under 10 minutes per person. Set `meta.reader` to the person the board is mainly for.

## 9. The understanding check (quiz)
- 5-7 questions, one per thing people must not get wrong: the main decision, owners and dates, how a plan works, what is still open.
- Wrong options must be plausible. Never trick questions.
- `why`: one line that teaches the answer. `review`: the tab (and project) plus the timestamp range that answers it.
- Pass mark: all but one. The check sits at the end of the board: people take it after reading, not before.

## 10. Spelling and words
- Look for: product and company names, people's names, acronyms, technical words, UK/US spelling from auto-captions.
- `sure: true` only when there is no doubt. Everything else goes to the user to confirm.
- Every word a newcomer would trip on goes into `terms` with a plain meaning. The board explains it on hover wherever it appears.

## 11. Writing style
Plain English, short sentences, numbers as digits on screen, no em dashes, no jargon without a `terms` entry. Name things the way the team names them. Never pad: if a section has nothing, leave it out.
