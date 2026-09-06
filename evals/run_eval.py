"""Lightweight offline evaluation harness.

It checks response keyword coverage and emits a simple aggregate score. This is
not a substitute for human evaluation or model-based RAG metrics.
"""
import json
from pathlib import Path
from agent import chat

DATASET = Path(__file__).with_name("dataset.jsonl")


def run():
    rows = [json.loads(line) for line in DATASET.read_text().splitlines() if line.strip()]
    passed = 0
    for row in rows:
        answer = chat([{"role":"system","content":"Answer accurately."},{"role":"user","content":row["question"]}]).lower()
        hits = sum(k.lower() in answer for k in row["expected_keywords"])
        score = hits / len(row["expected_keywords"])
        passed += score >= 0.67
        print(f"{score:.2f} | {row['question']}")
    print(f"Aggregate: {passed}/{len(rows)} cases passed")

if __name__ == "__main__":
    run()
