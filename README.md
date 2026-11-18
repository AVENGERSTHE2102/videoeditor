# Video Agent Skill Library

A searchable collection of video-making agent skills cataloged by [awesome-claude-video-skills](https://github.com/zhuyansen/awesome-claude-video-skills), plus an always-on director skill for routing an editing agent to the right guidance.

## Install for personal use

Install the director and its local skill library into the default agent skills directory:

```sh
python3 scripts/install.py
```

Or install into a particular project's `.agents/skills` directory:

```sh
python3 scripts/install.py --target /path/to/project/.agents/skills
```

The installer adds one discoverable skill, `video-production-director`. Specialist skills stay in its local library and are loaded only when routing selects them. Existing installs are left untouched; move an old install aside before replacing it.

For a one-off search, run:

```sh
python3 scripts/search_skills.py motion graphics
python3 scripts/search_skills.py editing --category editing --limit 20
python3 scripts/audit_skills.py
```

## Layout

- `.agents/skills/video-production-director/SKILL.md`: automatically discoverable parent skill for video tasks.
- `library/<owner>/<repo>/<skill-path>/`: downloaded skill entrypoints and concise support files, preserving source paths.
- `skill-index.json`: all catalog projects and discovered skill entrypoints, with source URLs, descriptions, categories, and security grades.
- `scripts/search_skills.py`: dependency-free search over the index.
- `scripts/audit_skills.py`: static suspicious-instruction triage; review `audit-report.json` findings manually.
- `scripts/install.py`: installs the director and local routing library for personal use.

The initial static audit covered 1,982 skill entrypoints. It found no direct instruction-override matches; it flagged 18 remote-installer pipe-to-shell instructions and 179 destructive/privileged-command mentions for review. These are flags, not confirmed vulnerabilities. The director does not execute imported scripts automatically.

The source catalog includes apps and frameworks as well as skills. Projects without a `SKILL.md` remain in the index and are marked with `skill_count: 0`; they are not represented as installable agent skills. Imported instructions and concise support files retain their upstream contents. Large image assets, demo/template folders, and media bundles are omitted to keep the library practical to clone; upstream links remain in the index. Check each upstream license and security grade before redistribution or execution. The root has no blanket license because the imported sources have different terms.

## Refreshing

This is a snapshot of the parent catalog recorded in `skill-index.json`. To refresh it, rerun the collection workflow against the upstream catalog and review changed skills and licenses before publishing.
