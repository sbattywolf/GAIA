#!/usr/bin/env python3
"""Write a .pth file into a site-packages directory pointing to the repo.

This script is defensive: CI runners may have old Python where
`site.getusersitepackages()` or other helpers are missing. Try several
strategies to find a writable site-packages path.
"""
import os
import sys
import site
import sysconfig


def _makedirs(path):
    try:
        os.makedirs(path, exist_ok=True)
    except TypeError:
        if not os.path.isdir(path):
            os.makedirs(path)


def find_site_packages():
    # 1) Prefer the user site directory when available
    try:
        return site.getusersitepackages()
    except Exception:
        pass

    # 2) Fallback to site.USER_SITE if present
    user_site = getattr(site, 'USER_SITE', None)
    if user_site:
        return user_site

    # 3) Try the system site-packages
    try:
        packs = site.getsitepackages()
        if packs:
            return packs[0]
    except Exception:
        pass

    # 4) Use sysconfig to get a purelib path
    try:
        purelib = sysconfig.get_path('purelib')
        if purelib:
            return purelib
    except Exception:
        pass

    # 5) Platform-specific sensible default
    if os.name == 'nt':
        return os.path.join(sys.base_prefix, 'Lib', 'site-packages')
    else:
        ver = 'python%s' % (sys.version_info[0],)
        return os.path.join(sys.base_prefix, 'lib', ver, 'site-packages')


def main():
    repo = os.environ.get('GITHUB_WORKSPACE') or os.getcwd()
    site_dir = find_site_packages()
    _makedirs(site_dir)
    pth_file = os.path.join(site_dir, 'gaia_repo_path.pth')
    try:
        with open(pth_file, 'w') as fh:
            fh.write(repo + os.linesep)
        print('wrote .pth to', site_dir)
    except Exception as exc:
        print('failed to write .pth to', site_dir, 'error:', exc)
        sys.exit(2)


if __name__ == '__main__':
    main()
