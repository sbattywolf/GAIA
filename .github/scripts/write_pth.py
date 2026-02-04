#!/usr/bin/env python
"""Write a .pth file into a site-packages directory pointing to the repo.

This script is defensive: CI runners may be very old. Try several
strategies to find a writable site-packages path without failing on
missing stdlib modules.
"""
import os
import sys


def _makedirs(path):
    try:
        os.makedirs(path, exist_ok=True)
    except TypeError:
        if not os.path.isdir(path):
            os.makedirs(path)


def find_site_packages():
    # Try importing site and preferred helpers first, but don't fail
    site = None
    try:
        import site as _site
        site = _site
    except Exception:
        site = None

    if site is not None:
        try:
            val = site.getusersitepackages()
            if val:
                return val
        except Exception:
            pass

        user_site = getattr(site, 'USER_SITE', None)
        if user_site:
            return user_site

        try:
            packs = site.getsitepackages()
            if packs:
                return packs[0]
        except Exception:
            pass

    # Try sysconfig if available
    try:
        import sysconfig as _sysconfig
        try:
            purelib = _sysconfig.get_path('purelib')
            if purelib:
                return purelib
        except Exception:
            pass
    except Exception:
        pass

    # Try distutils.sysconfig
    try:
        from distutils import sysconfig as _distro
        try:
            lib = _distro.get_python_lib()
            if lib:
                return lib
        except Exception:
            pass
    except Exception:
        pass

    # Try to pick an existing site-packages-like entry from sys.path
    for p in sys.path:
        if not p:
            continue
        if os.path.isdir(p) and ('site-packages' in p or 'dist-packages' in p):
            return p

    # Last-resort sensible defaults
    try:
        base = getattr(sys, 'base_prefix', sys.prefix)
    except Exception:
        base = sys.prefix

    if os.name == 'nt':
        return os.path.join(base, 'Lib', 'site-packages')
    else:
        ver = 'python%d' % (getattr(sys, 'version_info')[0],)
        return os.path.join(base, 'lib', ver, 'site-packages')


def main():
    repo = os.environ.get('GITHUB_WORKSPACE') or os.getcwd()
    site_dir = find_site_packages()
    try:
        _makedirs(site_dir)
    except Exception:
        print('unable to create site-packages directory:', site_dir)
        sys.exit(2)

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
