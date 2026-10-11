"""Build the site: check the data, render every page, copy static files, check the output."""
import argparse
import shutil
import sys
from pathlib import Path

from . import checks, data, static
from .errors import BuildError
from .pages import PAGES

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = ROOT / '_site'
# Never write the output into the repo root or over source folders.
SOURCE_DIRS = ['.git', '.github', 'data', 'generator'] + static.STATIC_DIRS
# Every build leaves this empty file in its output. --out only empties a folder that has it.
BUILD_MARKER = '.site-build'


def _output_dir(arg):
    out = Path(arg).resolve() if arg else DEFAULT_OUT
    if out == ROOT or out in ROOT.parents:
        raise BuildError(f'refusing to build into {out}: it holds the source. Use a new folder.')
    if out == Path.home():
        raise BuildError(f'refusing to build into {out}: it is your home folder. Use a new folder.')
    for name in SOURCE_DIRS:
        source = ROOT / name
        if out == source or source in out.parents:
            raise BuildError(f'refusing to build into {out}: it is inside {name}/.')
    if out.exists() and not out.is_dir():
        raise BuildError(f'refusing to build into {out}: it is a file. Use a new folder.')
    if (out / '.git').exists() or (out / 'build.py').exists():
        raise BuildError(f'refusing to empty {out}: it looks like a source checkout. Use a new folder.')
    if out != DEFAULT_OUT and out.exists() and any(out.iterdir()) and not (out / BUILD_MARKER).is_file():
        raise BuildError(f'refusing to empty {out}: it is not a previous build. Use a new folder.')
    return out


def _shown(path):
    """_site rather than a long absolute path when the folder is in the repo."""
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def build(out_arg=None):
    filenames = [page.FILENAME for page in PAGES]
    if len(set(filenames)) != len(filenames):
        raise BuildError('two page modules share a FILENAME')
    site = data.load(ROOT / 'data', set(filenames))
    rendered = [(page.FILENAME, page.render(site)) for page in PAGES]

    out = _output_dir(out_arg)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    (out / BUILD_MARKER).write_text('', encoding='utf-8')
    for filename, html in rendered:
        with open(out / filename, 'w', encoding='utf-8', newline='\n') as f:
            f.write(html)
    copied = static.copy_static(ROOT, out)

    problems, scanned = checks.scan(out)
    if problems:
        raise BuildError(f'the output contains banned text ({len(problems)} found):\n  ' + '\n  '.join(problems))
    print(f'built {len(rendered)} pages into {_shown(out)}/ (copied {", ".join(copied)}; {scanned} text files checked)')


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(errors='backslashreplace')  # never crash printing on a non-UTF-8 console
    parser = argparse.ArgumentParser(prog='build.py', description='Build the Lifepointe website.')
    parser.add_argument('--out', metavar='DIR', help=f'output folder (default: {_shown(DEFAULT_OUT)}/); emptied first')
    args = parser.parse_args(argv)
    try:
        build(args.out)
    except BuildError as e:
        print(f'build failed: {e}', file=sys.stderr)
        return 1
    return 0
