import subprocess
import sys
from pathlib import Path
from shutil import copyfile


META = Path(__file__).parent


def run(hooks_path: Path) -> int:
    print('Hooks path:', hooks_path)
    print('Args:', sys.argv)
    config = hooks_path / sys.argv[1]
    files = sys.argv[2:]

    prepare_config(config)

    return subprocess.call(
        # TODO: only `--color always` when color is on for this process? isatty?
        ['pre-commit', 'run', '--color', 'always', '--config', config, '--files'] + files
    )


def prepare_config(config: Path) -> None:
    content = config.read_text(encoding='utf-8')
    new_content = content.replace('$HERE', str(config.parent.absolute()))
    if content != new_content:
        config.write_text(new_content, encoding='utf-8')


def generate() -> int:
    copyfile(META / 'template.setup.cfg', 'setup.cfg')
    copyfile(META / 'template.setup.py', 'setup.py')
    copyfile(META / 'template.pre_commit_meta_hooks_inner.py', 'pre_commit_meta_hooks_inner.py')
    copyfile(META / 'template.run.py', 'run.py')

    pre_commit_hooks_template = (META / 'template.pre-commit-hooks.yaml').read_text()
    pre_commit_hooks = '\n'.join(
        pre_commit_hooks_template.format(
            name=removesuffix(file.name, '.pre-commit-config.yaml'),
            file=file.name
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
