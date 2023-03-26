import subprocess
from pathlib import Path


for config in Path.cwd().glob('*.pre-commit-config.yaml'):
    subprocess.check_call(
        ['pre-commit', 'autoupdate', '--config', config]
    )
