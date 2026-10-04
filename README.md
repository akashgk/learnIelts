# learnIelts: IELTS Academic practice repository

A complete, structured practice bank for **IELTS Academic**: Listening, Reading, Writing, Speaking, Vocabulary and Grammar. Every exercise is a folder with the **problem** and its **solution and explanation**. A machine-readable **`index.json`** lets you build an interactive study app or artifact on top of it.

> All passages, recordings, prompts and model answers are **original** and written to the official IELTS format and band descriptors. Links to free official tests are in [`resources/`](resources/README.md).

## 📦 What's inside

| # | Section | Items | Each item contains |
|---|---|---|---|
| 00 | [Exam guide](00_exam_guide/README.md) | 5 | Test format · band scores & conversion tables · question-type strategies · 8-week plan · test-day checklist |
| 01 | [Listening](01_listening/README.md) | 16 (4 full tests, 160 Qs) | `transcript.md` (TTS-ready) · `questions.json` · `QUESTIONS.md` · `SOLUTION.md` |
| 02 | [Reading](02_reading/README.md) | 20 passages (261 Qs) | `passage.md` · `questions.json` · `QUESTIONS.md` · `SOLUTION.md` (evidence + traps) |
| 03 | [Writing Task 1](03_writing_task1/README.md) | 18 | `prompt.md` · `data.json` (chart spec) · `model_answer.md` (Band 8–9 + notes) |
| 04 | [Writing Task 2](04_writing_task2/README.md) | 26 model essays + 60-prompt bank | `prompt.md` · `model_answer.md` (essay + plan + vocabulary) |
| 05 | [Speaking Part 1](05_speaking_part1/README.md) | 20 modelled topics + 92-question bank | `questions.md` · `model_answer.md` |
| 06 | [Speaking Parts 2 & 3](06_speaking_part2_3/README.md) | 18 modelled cue cards + 24-card bank | `cue_card.md` · `model_answer.md` (2-min talk + Part 3) |
| 07 | [Vocabulary](07_vocabulary/README.md) | 18 sets (216 words, 180 Qs) | `words.json` · `word_list.md` · exercises |
| 08 | [Grammar](08_grammar/README.md) | 16 lessons (144 Qs) | `lesson.md` · exercises |

**Totals:** 160 study items · 745 auto-graded questions · 44 model essays/reports · 60 extra essay prompts · 38 modelled speaking sets + 92 Part 1 questions and 24 cue cards in the banks.

## 🗂 Folder structure

```
learnIelts/
├── index.json                  ← generated catalogue of every item (load this in an app)
├── 00_exam_guide/              ← start here
├── 01_listening/
│   └── 01_s1_sports_centre_membership/
│       ├── meta.json           ← title, level, topics, speakers
│       ├── transcript.md       ← "**SPEAKER:** line" format, [Qn] markers
│       ├── questions.json      ← single source of truth (answers + explanations)
│       ├── QUESTIONS.md        ← generated
│       └── SOLUTION.md         ← generated
├── 02_reading/NN_topic/        ← passage.md + questions.json (+ generated md)
├── 03_writing_task1/NN_type_topic/  ← prompt.md + data.json + model_answer.md
├── 04_writing_task2/NN_type_topic/  ← prompt.md + model_answer.md
├── 05_speaking_part1/NN_topic/
├── 06_speaking_part2_3/NN_topic/
├── 07_vocabulary/NN_topic/     ← words.json + exercises
├── 08_grammar/NN_topic/        ← lesson.md + exercises
├── docs/
│   ├── SCHEMA.md               ← file formats and grading rules
│   └── ARTIFACT_GUIDE.md       ← how to build a study-tracker app on top of this repo
├── resources/README.md         ← free official practice tests and daily input
└── scripts/build_index.py      ← validates content, regenerates index + markdown
```

Folder names are `NN_descriptive_slug`, so they sort in study order and stay stable as IDs.

## 🚀 How to use it

**As a learner (no tools needed)**
1. Read [`00_exam_guide`](00_exam_guide/README.md), then follow the [8-week plan](00_exam_guide/04_eight_week_study_plan/guide.md).
2. Open an item, attempt `QUESTIONS.md` / `prompt.md` under time, then check `SOLUTION.md` / `model_answer.md`.

**As a builder (artifact or app)**
1. Fetch `https://raw.githubusercontent.com/akashgk/learnIelts/<branch>/index.json`.
2. Follow [`docs/ARTIFACT_GUIDE.md`](docs/ARTIFACT_GUIDE.md): section tabs, side-by-side passage and questions, auto-grading, TTS listening, Task 1 charts from `data.json`, timers and progress per `item.id`.

## ✍️ Adding content

1. Create a folder `NN_slug` in the right section, with a `meta.json` (`title`, `summary`, `difficulty`, `topics`).
2. Add the section's content files (see [`docs/SCHEMA.md`](docs/SCHEMA.md)). For objective practice, write `questions.json`.
3. Run:
   ```bash
   python3 scripts/build_index.py          # validate + regenerate index.json, QUESTIONS.md, SOLUTION.md, section READMEs
   python3 scripts/build_index.py --check  # validate only (CI-friendly)
   ```
   The validator checks for duplicate question numbers, answers that don't match the options, invalid TRUE/FALSE/NOT GIVEN values and wrong totals.

## 📊 Quick facts about the test
| | Listening | Reading | Writing | Speaking |
|---|---|---|---|---|
| Time | ~30 min | 60 min | 60 min | 11–14 min |
| Format | 4 parts, 40 Qs | 3 passages, 40 Qs | Task 1 (150 w) + Task 2 (250 w) | 3 parts |
| Band 7 ≈ | 30/40 | 30/40 | all 4 criteria at 7 | all 4 criteria at 7 |

From mid-2026, IELTS is delivered on computer in most markets. Content and scoring are unchanged. See the [test format guide](00_exam_guide/01_test_format/guide.md).
