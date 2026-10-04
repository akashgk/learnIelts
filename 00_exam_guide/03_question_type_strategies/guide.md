# Question-type strategies (Reading and Listening)

Every objective question in this repo is tagged with one of these `type` values in `questions.json`. Learn the strategy, then filter the practice sets by type.

## Reading

### `tfng` — True / False / Not Given
- **TRUE:** the passage says the same thing, usually in different words.
- **FALSE:** the passage says the **opposite**.
- **NOT GIVEN:** the passage doesn't say. The topic might be mentioned, but the specific claim isn't.
- Questions follow **passage order**.
- Watch qualifiers: *all, only, always, some, never, partly, mainly*. These are often what decides the answer.
- 🧪 Practise: `02_reading/01`, `03`, `05`, `08`

### `ynng` — Yes / No / Not Given
- Same as TFNG but about the **writer's opinions or claims**. Look for evaluative words: *clearly, surprisingly, it is doubtful whether…*
- 🧪 Practise: `02_reading/04`, `06`

### `matching` — Headings / Information / Features / Endings
- **Headings:** read the paragraph and summarise it in 3–5 words *before* you look at the list. A heading covers the **whole** paragraph. Distractors match only one detail.
- **Matching information** ("Which paragraph contains…"): questions are **not** in order. Look for the *type* of information: a reason, an example, a comparison, a definition.
- **Features** (people/dates): scan for the names, then read **around every mention**.
- **Sentence endings:** check both grammar and meaning. Two endings are usually grammatically possible.
- 🧪 Practise: `02_reading/01`, `02`, `03`, `04`, `05`, `07`, `08`

### `mcq` / `mcq_multi` — Multiple choice
- Find the location first, then eliminate options. Typical traps: true but irrelevant; the opposite; two details mixed together; a word repeated from the text with a changed meaning.
- For "Choose TWO", each letter scores separately and order doesn't matter.
- 🧪 Practise: `02_reading/02`, `05`, `06`, `07`

### `gap` / `short` — Completion and short answers
- **Read the word limit.** "NO MORE THAN TWO WORDS AND/OR A NUMBER" means 1–2 words, plus optionally a number.
- Predict the **word class** (noun, adjective, plural?) before you scan.
- Copy the word **exactly** from the passage. Don't change its form.
- Hyphenated words count as one word.
- 🧪 Practise: every reading set

## Listening

| Part | Common types | Key skill |
|---|---|---|
| 1 | Form/note completion | Spelling, numbers, dates, **self-corrections** ("no, sorry…") |
| 2 | MCQ, map labelling, matching | Following directions (*opposite, to the left of, in the north-east corner*) |
| 3 | MCQ, matching speakers, choose two | Tracking **who** says what and **final decisions** after a change of mind |
| 4 | Note completion | Signpost language (*Now let's turn to…, Finally…*), paraphrase |

**Universal listening tips**
1. Use the reading time to **underline keywords** and predict answers.
2. The first thing you hear is often a **distractor**. Wait for the confirmed answer.
3. If you miss one, **move on**. Don't lose the next three.
4. Check plurals (*-s*) and spelling at the end.

## Self-check grading rules (used by any app built on this repo)
- Answers are **case-insensitive** and trimmed.
- Any value in an `answer` array is accepted.
- For `mcq_multi`, each correct letter scores one mark, in any order.
