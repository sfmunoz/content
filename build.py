#!/usr/bin/env python3
# vim: set foldmethod=marker:
#
# Author: 46285520+sfmunoz@users.noreply.github.com
# Date:   Wed Aug 27 18:26:17 UTC 2025
# Issue:  https://github.com/sfmunoz/content/issues/3
#

# {{{ imports

import sys

from logging import getLogger, basicConfig, INFO
basicConfig(format='%(asctime)s [%(relativeCreated)7.0f] [%(levelname).1s] %(message)s',level=INFO,stream=sys.stderr)
log = getLogger(__name__)

from argparse import ArgumentParser, RawTextHelpFormatter

import datetime
from pathlib import Path
from re import compile as re_compile

HEADER_MD = """# content

> [!WARNING]
> **DO NOT EDIT**: this **README.md** file was automatically generated on **{0}** by the **build.py** script based on the contents of the repository.

https://sfmunoz.com/ site content

## Architecture

```mermaid
flowchart LR
    user(["user"])
    sfmunoz("`sfmunoz.github.io<br>**frontend**<br>SvelteKit`")
    cms("`cms<br>**backend**<br>Hugo`")
    content("`content<br>**data**<br>Git`")
    style content stroke-width:4px
    user -->|https| sfmunoz --> cms --> content
```
"""

# }}}
# -------- ReadmeBuild(object) -- class --------
# {{{ ReadmeBuild -- class

class ReadmeBuild(object):

# }}}
# {{{ ReadmeBuild.__init__()

    def __init__(self,args):
        self.__args = args
        self.__pat = re_compile('^([a-z])/[a-z][a-z]/(.+)/index.md$')

# }}}
# {{{ ReadmeBuild.run()

    def run(self):
        fname = "README.md"
        fp = sys.stdout if self.__args.stdout else open(fname,"w")
        log.info("dumping markdown to {0}".format("stdout" if self.__args.stdout else fname))
        ts_utc = datetime.datetime.now(datetime.UTC)
        fp.write(HEADER_MD.format(ts_utc.strftime("%Y-%m-%d %H:%M:%S UTC")))
        c_cur = ""
        for p in sorted(Path(".").rglob("**/index.md"),reverse=False):
            if not p.is_file():
                continue
            p_str = p.as_posix()
            m = self.__pat.match(p_str)
            if not m:
                continue
            c = m.group(1)
            slug = m.group(2)
            if c_cur != c:
                fp.write(f"\n## {c}\n\n")
                c_cur = c
            fp.write(f"* [{slug}]({p_str})\n")
        if self.__args.stdout:
            log.info("markdown dumped to stdout")
        else:
            log.info(f"markdown dumped to {fname}")
            fp.close()

# }}}
# -------- main --------
# {{{ main

if __name__ == "__main__":
    epilog = "46285520+sfmunoz@users.noreply.github.com (C) 2025-2026"

    parser = ArgumentParser(
        description = 'build.py (v1.0)',
        epilog = epilog,
        formatter_class = RawTextHelpFormatter,
    )

    parser.add_argument('-d', '--debug', action='store_true',
                        help='enable debug mode')

    parser.add_argument('-o', '--stdout', action='store_true',
                        help='dump output to stdout instead of README.md')

    args = parser.parse_args()

    if args.debug:
        from logging import DEBUG
        log.setLevel(DEBUG)

    ReadmeBuild(args).run()

# }}}
