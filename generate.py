from pathlib import Path
from shutil import copyfile


def removesuffix(s: str, suffix: str) -> str:
    assert s.endswith(suffix)
    point = len(suffix)
    return s[:-point]


META = Path(__file__).parent

copyfile(META / 'template.run.py', 'run.py')

hooks_template = (META / 'template.pre-commit-hooks.yaml').read_text()
hooks = '\n'.join(
    hooks_template.format(
        name=removesuffix(file.name, '.pre-commit-config.yaml'),
        file=file.name
    )
    for file
    in Path.cwd().glob('*.pre-commit-config.yaml')
)
Path('.pre-commit-hooks.yaml').write_text(hooks)
