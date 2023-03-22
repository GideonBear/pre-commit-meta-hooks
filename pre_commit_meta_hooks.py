import subprocess
import sys
from pathlib import Path
from shutil import copyfile


HERE = Path(__file__).parent


def run() -> int:
    config = Path(sys.argv[1])
    files = sys.argv[2:]

    prepare_config(config)

    return subprocess.call(
        ['pre-commit', 'run', '--color', 'always', '--config', config, '--files'] + files
    )


def prepare_config(config: Path) -> None:
    content = config.read_text(encoding='utf-8')
    new_content = content.replace('$HERE', str(HERE))
    if content != new_content:
        config.write_text(new_content, encoding='utf-8')


def generate() -> int:
    copyfile(HERE / 'template.setup.cfg', 'setup.cfg')
    copyfile(HERE / 'template.setup.py', 'setup.py')

    pre_commit_hooks_template = (HERE / 'template.pre-commit-hooks.yaml').read_text()
    pre_commit_hooks = '\n'.join(
        pre_commit_hooks_template.format(
            name=removesuffix(file.name, '.pre-commit-config.yaml'),
            file=file
        )
        for file
        in Path.cwd().glob('*.pre-commit-config.yaml')
    )
    Path('.pre-commit-hooks.yaml').write_text(pre_commit_hooks)

    return 0


def removesuffix(s: str, suffix: str) -> str:
    assert s.endswith(suffix)
    point = len(suffix)
    return s[:-point]
