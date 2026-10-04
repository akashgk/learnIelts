#!/usr/bin/env python3
"""Validate every exercise folder, render QUESTIONS.md / SOLUTION.md from
questions.json, and write the root index.json that an app or artifact loads.

Usage:  python3 scripts/build_index.py          # build
        python3 scripts/build_index.py --check  # validate only, exit 1 on error

No third-party dependencies. See docs/SCHEMA.md for the file formats.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SECTIONS = [
    ("00_exam_guide", "guide", "Exam guide"),
    ("01_listening", "listening", "Listening"),
    ("02_reading", "reading", "Reading"),
    ("03_writing_task1", "writing_task1", "Writing Task 1"),
    ("04_writing_task2", "writing_task2", "Writing Task 2"),
    ("05_speaking_part1", "speaking_part1", "Speaking Part 1"),
    ("06_speaking_part2_3", "speaking_part2_3", "Speaking Parts 2 & 3"),
    ("07_vocabulary", "vocabulary", "Vocabulary"),
    ("08_grammar", "grammar", "Grammar"),
]

QUESTION_TYPES = {
    "tfng": "True / False / Not Given",
    "ynng": "Yes / No / Not Given",
    "mcq": "Multiple choice (one answer)",
    "mcq_multi": "Multiple choice (choose TWO/THREE)",
    "gap": "Completion (sentence / note / table / form / summary)",
    "matching": "Matching (headings, information, features, endings)",
    "short": "Short answer",
}

TFNG = {"TRUE", "FALSE", "NOT GIVEN"}
YNNG = {"YES", "NO", "NOT GIVEN"}
REQUIRED_META = ["title", "summary", "difficulty", "topics"]

errors = []


def err(path, msg):
    errors.append(f"{path.relative_to(ROOT)}: {msg}")


def answers_of(q):
    a = q["answer"]
    return a if isinstance(a, list) else [a]


def qnum(q):
    n = q["n"]
    return "–".join(map(str, n)) if isinstance(n, list) else str(n)


def validate_questions(path, data):
    count = 0
    seen = set()
    for g in data.get("groups", []):
        t = g.get("type")
        if t not in QUESTION_TYPES:
            err(path, f"unknown group type {t!r}")
            continue
        keys = {o["key"] for o in g.get("options", [])}
        for q in g.get("questions", []):
            nums = q["n"] if isinstance(q["n"], list) else [q["n"]]
            for n in nums:
                if n in seen:
                    err(path, f"question {n} duplicated")
                seen.add(n)
            count += len(nums)
            if "answer" not in q or "explanation" not in q:
                err(path, f"question {qnum(q)} needs answer and explanation")
                continue
            ans = [str(a).upper() for a in answers_of(q)]
            if t == "tfng" and not set(ans) <= TFNG:
                err(path, f"q{qnum(q)} tfng answer {ans}")
            if t == "ynng" and not set(ans) <= YNNG:
                err(path, f"q{qnum(q)} ynng answer {ans}")
            if t in ("mcq", "mcq_multi", "matching"):
                opts = keys | {o["key"] for o in q.get("options", [])}
                if not set(ans) <= {k.upper() for k in opts}:
                    err(path, f"q{qnum(q)} answer {ans} not in options {sorted(opts)}")
            if t == "mcq_multi" and len(ans) != len(nums):
                err(path, f"q{qnum(q)} mcq_multi needs one answer per number")
    if data.get("total") not in (None, count):
        err(path, f"total says {data.get('total')} but found {count}")
    return count


def fmt_options(opts):
    return "\n".join(f"- **{o['key']}** {o['text']}" for o in opts)


def render_questions(title, data):
    out = [f"# {title} — Questions", ""]
    if data.get("instructions"):
        out += [data["instructions"], ""]
    for g in data["groups"]:
        out += [f"## Questions {g['range']}", "", f"*{g['instructions']}*", ""]
        if g.get("options"):
            out += [fmt_options(g["options"]), ""]
        for q in g["questions"]:
            out.append(f"**{qnum(q)}.** {q['prompt']}")
            if q.get("options"):
                out += ["", fmt_options(q["options"])]
            out.append("")
    return "\n".join(out).rstrip() + "\n"


def render_solution(title, data):
    out = [f"# {title} — Answers & explanations", ""]
    out += ["| Q | Answer | Also accepted |", "|---|---|---|"]
    for g in data["groups"]:
        for q in g["questions"]:
            a = answers_of(q)
            if g["type"] == "mcq_multi":
                out.append(f"| {qnum(q)} | {', '.join(a)} (any order) | |")
            else:
                out.append(f"| {qnum(q)} | {a[0]} | {', '.join(a[1:])} |")
    out.append("")
    for g in data["groups"]:
        out += [f"## Questions {g['range']} · {QUESTION_TYPES[g['type']]}", ""]
        if g.get("strategy"):
            out += [f"> **Strategy:** {g['strategy']}", ""]
        for q in g["questions"]:
            out.append(f"**{qnum(q)}. {', '.join(map(str, answers_of(q)))}** — {q['explanation']}")
            if q.get("evidence"):
                out.append(f"  \n  *Evidence:* “{q['evidence']}”")
            if q.get("trap"):
                out.append(f"  \n  *Trap:* {q['trap']}")
            out.append("")
    if data.get("band_table"):
        out += ["## Raw score → approximate band", "", data["band_table"], ""]
    return "\n".join(out).rstrip() + "\n"


def word_count(md_path):
    if not md_path.exists():
        return None
    text = md_path.read_text(encoding="utf-8")
    text = re.split(r"^---\s*$", text, maxsplit=1, flags=re.M)[0]  # stop before notes
    text = re.sub(r"^(#|\*\().*$", "", text, flags=re.M)  # headings, "(N words)"
    return len(re.findall(r"[A-Za-z0-9'’-]+", text))


def build_item(section_dir, section_key, item_dir, check):
    meta_path = item_dir / "meta.json"
    if not meta_path.exists():
        err(item_dir, "missing meta.json")
        return None
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    for k in REQUIRED_META:
        if k not in meta:
            err(meta_path, f"missing {k!r}")
    item = {
        "id": f"{section_dir.name}/{item_dir.name}",
        "section": section_key,
        "slug": item_dir.name,
        "order": int(item_dir.name.split("_", 1)[0]) if item_dir.name[:2].isdigit() else 999,
        **meta,
    }
    qpath = item_dir / "questions.json"
    if qpath.exists():
        data = json.loads(qpath.read_text(encoding="utf-8"))
        item["question_count"] = validate_questions(qpath, data)
        item["question_types"] = sorted({g["type"] for g in data["groups"]})
        if not check:
            (item_dir / "QUESTIONS.md").write_text(render_questions(meta["title"], data), encoding="utf-8")
            (item_dir / "SOLUTION.md").write_text(render_solution(meta["title"], data), encoding="utf-8")
    for name in ("passage.md", "model_answer.md"):
        wc = word_count(item_dir / name)
        if wc:
            item[name.split(".")[0] + "_words"] = wc
    item["files"] = sorted(
        p.name for p in item_dir.iterdir() if p.is_file() and p.name != "meta.json"
    )
    return item


FILE_ORDER = ["guide.md", "passage.md", "transcript.md", "map.md", "prompt.md", "cue_card.md", "questions.md",
              "lesson.md", "word_list.md", "QUESTIONS.md", "model_answer.md", "SOLUTION.md"]
MARKER ="<!-- CONTENTS: generated by scripts/build_index.py — do not edit below -->"


def render_contents(dirname, sec_items):
    rows = ["| # | Item | Level | Topics | Files |", "|---|---|---|---|---|"]
    for it in sec_items:
        main_files = sorted((f for f in it["files"] if f.endswith(".md")),
                            key=lambda f: FILE_ORDER.index(f) if f in FILE_ORDER else 99)
        links = " · ".join(f"[{f.rsplit('.', 1)[0]}]({it['slug']}/{f})" for f in main_files)
        extra = f" ({it['question_count']} Qs)" if it.get("question_count") else ""
        rows.append(f"| {it['slug'][:2]} | **{it['title']}**{extra}<br>{it['summary']} | {it['difficulty']} "
                    f"| {', '.join(it['topics'])} | {links} |")
    return "\n".join(rows)


def update_readme(sdir, sec_items, check):
    readme = sdir / "README.md"
    if not readme.exists() or check:
        return
    text = readme.read_text(encoding="utf-8")
    head = text.split(MARKER)[0].rstrip()
    readme.write_text(f"{head}\n\n{MARKER}\n\n## Contents\n\n{render_contents(sdir.name, sec_items)}\n", encoding="utf-8")


def main():
    check = "--check" in sys.argv
    sections, items = [], []
    for dirname, key, label in SECTIONS:
        sdir = ROOT / dirname
        if not sdir.is_dir():
            err(sdir, "section folder missing")
            continue
        sec_items = []
        for d in sorted(p for p in sdir.iterdir() if p.is_dir()):
            it = build_item(sdir, key, d, check)
            if it:
                sec_items.append(it)
        update_readme(sdir, sec_items, check)
        sections.append({
            "key": key, "label": label, "path": dirname,
            "readme": f"{dirname}/README.md" if (sdir / "README.md").exists() else None,
            "count": len(sec_items),
        })
        items += sec_items

    try:
        commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        commit = None

    index = {
        "name": "learnIelts — IELTS Academic practice",
        "schema_version": 1,
        "commit": commit,
        "question_types": QUESTION_TYPES,
        "sections": sections,
        "items": items,
        "totals": {
            "items": len(items),
            "objective_questions": sum(i.get("question_count", 0) for i in items),
        },
    }
    if errors:
        print("\n".join(errors), file=sys.stderr)
        sys.exit(1)
    if not check:
        (ROOT / "index.json").write_text(json.dumps(index, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"OK: {len(items)} items, {index['totals']['objective_questions']} auto-graded questions")


if __name__ == "__main__":
    main()
