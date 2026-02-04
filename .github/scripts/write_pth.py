#!/usr/bin/env python3
"""Write a .pth file into the Python user site-packages pointing to the repo.

This avoids relying on shell heredocs and is cross-platform.
"""
import os
import site

def _makedirs(path):
    try:
        os.makedirs(path, exist_ok=True)
    except TypeError:
        # Python < 3.2 doesn't support exist_ok
        if not os.path.isdir(path):
            os.makedirs(path)

def main():
    user_site = site.getusersitepackages()
    _makedirs(user_site)
    pth_file = os.path.join(user_site, 'gaia_repo_path.pth')
    with open(pth_file, 'w') as fh:
        fh.write(os.environ.get('GITHUB_WORKSPACE', '') + os.linesep)
    print('wrote .pth to', user_site)

if __name__ == '__main__':
    main()
