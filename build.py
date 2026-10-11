#!/usr/bin/env python3
"""Build the Lifepointe Chiropractic & Wellness Center website.

    python3 build.py              build into _site/ (emptied first)
    python3 build.py --out DIR    build into DIR instead

Content is in data/*.json, page templates in generator/pages/, shared styling in
css/site.css. Python 3.9+ standard library only. See README.md.
"""
import sys
from pathlib import Path

if sys.version_info < (3, 9):
    sys.exit('build.py needs Python 3.9 or newer')

sys.path.insert(0, str(Path(__file__).resolve().parent))

from generator.main import main  # noqa: E402

if __name__ == '__main__':
    sys.exit(main())
