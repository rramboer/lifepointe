"""Copy the hand-written files the pages use into the output folder."""
import shutil

from .errors import BuildError

# Folders copied as-is into the site, each to the same path. Add a name here to publish another
# folder. From email/ only images/ is published, because emails load their pictures from
# https://lifepointechiro.com/email/images/. The template itself is pasted into an email
# platform and previewed by opening the file, so it is not a page on the site.
STATIC_DIRS = ['css', 'js', 'assets', 'email/images', 'forms']


def copy_static(root, out):
    for name in STATIC_DIRS:
        source = root / name
        if not source.is_dir():
            raise BuildError(f'static folder {name}/ is missing')
        shutil.copytree(source, out / name, ignore=shutil.ignore_patterns('.DS_Store', 'Thumbs.db'))
    return STATIC_DIRS
