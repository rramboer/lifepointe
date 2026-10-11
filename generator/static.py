"""Copy the hand-written files the pages use into the output folder."""
import shutil

from .errors import BuildError

# Folders copied as-is into the site. Add a name here to publish another folder.
STATIC_DIRS = ['css', 'js', 'assets', 'email']


def copy_static(root, out):
    for name in STATIC_DIRS:
        source = root / name
        if not source.is_dir():
            raise BuildError(f'static folder {name}/ is missing')
        shutil.copytree(source, out / name, ignore=shutil.ignore_patterns('.DS_Store', 'Thumbs.db'))
    return STATIC_DIRS
