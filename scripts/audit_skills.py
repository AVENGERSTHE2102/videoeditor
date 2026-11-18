#!/usr/bin/env python3
"""Static triage of imported skill instructions; findings require human review."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULES = [
    ("high", "instruction override", re.compile(r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions|reveal\s+(the\s+)?(system|hidden) prompt", re.I)),
    ("review", "explicit instruction override", re.compile(r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions|reveal\s+(the\s+)?(system|hidden) prompt", re.I)),
    ("review", "remote installer piped to shell", re.compile(r"(?:curl|wget)\b[^\n|]{0,200}\|\s*(?:ba)?sh\b", re.I)),
    ("review", "destructive or privileged command", re.compile(r"\brm\s+-rf\b|\bsudo\b|\bchmod\s+777\b", re.I)),
]


def main():
    findings = []
    for path in (ROOT / "library").rglob("*"):
        if path.suffix.lower() not in {".md", ".txt", ".py", ".sh", ".js", ".ts"}:
            continue
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for number, line in enumerate(lines, 1):
            for severity, label, pattern in RULES:
                if pattern.search(line):
                    findings.append({"severity": severity, "rule": label, "file": str(path.relative_to(ROOT)), "line": number, "excerpt": line.strip()[:240]})
    report = {"method": "static regex triage; not a sandbox or proof of safety", "skills_scanned": sum(1 for _ in (ROOT / "library").rglob("SKILL.md")), "findings": findings}
    (ROOT / "audit-report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"skills_scanned": report["skills_scanned"], "findings": len(findings), "flagged_files": len({x['file'] for x in findings}), "report": "audit-report.json"}))


if __name__ == "__main__":
    main()
