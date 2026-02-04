#!/usr/bin/env python3
"""Write a .pth file into the Python user site-packages pointing to the repo.

This avoids relying on shell heredocs and is cross-platform.
"""
import os
import site
from pathlib import Path

def main():
    user_site = site.getusersitepackages()
    p = Path(user_site)
    p.mkdir(parents=True, exist_ok=True)
    pth_file = p / 'gaia_repo_path.pth'
    pth_file.write_text(os.environ.get('GITHUB_WORKSPACE', '') + os.linesep)
    print('wrote .pth to', user_site)

if __name__ == '__main__':
    main()
