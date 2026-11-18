"""Find the complete VibeScience checkout through symlinks or explicit configuration."""
import json,os
from pathlib import Path

def locate():
    override=os.environ.get('VIBE_SCIENCE_HOME')
    root=Path(override).expanduser().resolve() if override else Path(__file__).resolve().parents[3]
    if not (root/'video/shared/tools/init_project.py').is_file():
        raise SystemExit('Complete VibeScience checkout missing. Set VIBE_SCIENCE_HOME to the cloned repository.')
    return root
if __name__=='__main__':
    root=locate();print(json.dumps({'root':str(root),'video':str(root/'video'),'shared':str(root/'video/shared')},ensure_ascii=False))
