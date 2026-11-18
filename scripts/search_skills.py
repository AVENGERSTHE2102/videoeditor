#!/usr/bin/env python3
"""Search the generated video skill index without third-party dependencies."""
import argparse
import json
from pathlib import Path


def search(index, terms, category=None, limit=10):
    words = terms.lower().split()
    results = []
    for skill in index["skills"]:
        if category and skill.get("kind") != category:
            continue
        haystack = " ".join(str(skill.get(k, "")) for k in ("repo", "path", "description", "kind")).lower()
        score = sum(haystack.count(word) for word in words)
        if score:
            results.append((score, skill))
    results.sort(key=lambda x: (-x[0], x[1]["repo"], x[1]["path"]))
    return [skill for _, skill in results[:limit]]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("terms", nargs="+", help="words to match in skill metadata")
    parser.add_argument("--category", help="catalog category id")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--index", type=Path, default=Path(__file__).resolve().parents[1] / "skill-index.json")
    args = parser.parse_args()
    index = json.loads(args.index.read_text(encoding="utf-8"))
    for skill in search(index, " ".join(args.terms), args.category, max(0, args.limit)):
        print(f"[{skill.get('kind') or 'uncategorized'} | {skill.get('security_grade') or 'ungraded'}] {skill['repo']} :: {skill['path']}\n  local: {skill.get('local_path', '')}\n  {skill.get('description') or ''}\n  {skill['url']}")


if __name__ == "__main__":
    main()
