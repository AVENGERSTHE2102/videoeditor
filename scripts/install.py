#!/usr/bin/env python3
"""Install the video director skill and its local skill library."""
import argparse
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents/skills/video-production-director"


def install(target: Path) -> Path:
    dest = target.expanduser() / "video-production-director"
    if dest.exists():
        raise FileExistsError(f"{dest} already exists; move it aside before installing")
    resources = dest / "resources"
    (dest / "references").mkdir(parents=True)
    (resources / "scripts").mkdir(parents=True)
    shutil.copy2(SKILL / "SKILL.md", dest / "SKILL.md")
    shutil.copy2(SKILL / "references/platform-principles.md", dest / "references/platform-principles.md")
    shutil.copytree(ROOT / "library", resources / "library")
    shutil.copy2(ROOT / "scripts/search_skills.py", resources / "scripts/search_skills.py")
    index = json.loads((ROOT / "skill-index.json").read_text(encoding="utf-8"))
    for skill in index["skills"]:
        skill["local_path"] = "resources/" + skill["local_path"]
    (resources / "skill-index.json").write_text(json.dumps(index, ensure_ascii=False), encoding="utf-8")
    (dest / ".video-skill-library-install").write_text("1\n", encoding="utf-8")
    return dest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, default=Path.home() / ".agents/skills", help="agent skills directory (default: ~/.agents/skills)")
    args = parser.parse_args()
    print(install(args.target))


if __name__ == "__main__":
    main()
