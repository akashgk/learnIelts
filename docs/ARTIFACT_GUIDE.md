# Building a study-tracker artifact from this repo

This repo is designed to power a single-page study app like the "Algo Study Tracker": a sidebar of items per section, a main pane with tabs, progress tracking and "Refresh from GitHub".

## 1. Fetch the data

```js
const OWNER = "akashgk", REPO = "learnIelts", BRANCH = "main";
const RAW = `https://raw.githubusercontent.com/${OWNER}/${REPO}/${BRANCH}`;

const index = await (await fetch(`${RAW}/index.json`)).json();
const file = (id, name) => fetch(`${RAW}/${id}/${name}`).then(r => name.endsWith(".json") ? r.json() : r.text());
```

- Load `index.json` once and fetch item files **lazily** when the user opens an item.
- Show `index.commit` in the header ("snapshot 42aa735") and re-fetch it on **Refresh from GitHub**.
- Use `item.id` as the key for saved progress so progress survives content updates.

## 2. Suggested layout (mirrors the Algo tracker)

```
Header:  IELTS Academic Tracker | Listening 12/80 · Reading 26/105 · Writing 3/24 · Speaking 5/24 | Overview | Refresh
Sidebar: [Listening][Reading][Writing][Speaking][Vocab][Grammar]  ← section tabs (index.sections)
         search box (title, topic, question type) · filter: All / To study / Studied / Revisit
         list of items: "01 Cooling the Concrete Jungle   [TFNG][HEAD]"
Main:    title · difficulty · topics chips · ⏱ timer (meta.minutes)
         tabs per section ↓  ·  Prev / Next / Revisit later / Mark as studied
```

| Section | Tabs | Interactive features |
|---|---|---|
| Reading | Passage · Questions · Solution · **Side by side** (passage left, questions right) | Answer inputs → grade against `questions.json` → band estimate |
| Listening | Play · Questions · Transcript · Solution | **Play** reads `transcript.md` with `speechSynthesis` using `meta.speakers` for voices. Hide the transcript until submitted |
| Writing Task 1 | Prompt (render `data.json` as a real chart) · Your answer (textarea + word counter + 20-min timer) · Model · Notes | Word count vs `min_words` |
| Writing Task 2 | Prompt · Your answer (40-min timer) · Model · Notes | Optionally ask Claude to grade against the 4 criteria |
| Speaking 1 | Flashcards from `meta.questions` · Model answers | Mic recording via `MediaRecorder` |
| Speaking 2&3 | Cue card with 1-min prep + 2-min talk timer · Part 3 questions · Model | Countdown timers |
| Vocabulary | Flashcards from `words.json` · Exercises · Solution | Spaced-repetition "Again / Good / Easy" |
| Grammar | Lesson · Exercises · Solution | Instant feedback |
| Exam guide | Rendered markdown | – |

## 3. Grading snippet

```js
const norm = s => String(s).trim().replace(/\s+/g, " ").replace(/\.$/, "").toLowerCase();

function grade(questionsJson, userAnswers /* { "7": "false", "21-22": ["B","D"] } */) {
  let score = 0, total = 0, results = [];
  for (const g of questionsJson.groups) for (const q of g.questions) {
    const accepted = (Array.isArray(q.answer) ? q.answer : [q.answer]).map(norm);
    if (Array.isArray(q.n)) {                       // mcq_multi: one mark per correct letter
      const given = new Set((userAnswers[q.n.join("-")] || []).map(norm));
      const hits = accepted.filter(a => given.has(a)).length;
      score += hits; total += q.n.length;
      results.push({ n: q.n, correct: hits === q.n.length, q });
    } else {
      const ok = accepted.includes(norm(userAnswers[q.n] ?? ""));
      score += ok; total += 1;
      results.push({ n: q.n, correct: ok, q });
    }
  }
  return { score, total, results };
}
```

Band estimate: `Math.round(score / total * 40)` → look up `band_table.json` (`listening` or `academic_reading`).

## 4. Progress model (per item)

```json
{ "02_reading/01_urban_heat_islands": { "status": "studied", "best": 11, "attempts": 2, "revisit": false, "notes": "…" } }
```

Save it in the artifact's storage or account sync, like the "Saved to your account" indicator in the Algo tracker.

## 5. Prompt to give Claude when building the artifact

> Build a single-page "IELTS Academic Tracker" artifact that loads `https://raw.githubusercontent.com/akashgk/learnIelts/main/index.json` and follows `docs/SCHEMA.md` and `docs/ARTIFACT_GUIDE.md` in that repo. Section tabs in a left sidebar with search and status filters. Main pane with tabs per section as described. Auto-grade `questions.json`, read listening transcripts with speechSynthesis, draw Writing Task 1 charts from `data.json`, add timers, and save progress per `item.id`.
