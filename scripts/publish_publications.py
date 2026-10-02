#!/usr/bin/env python3
"""Commit on a disposable GitHub runner; recompute after a concurrent push."""
import os
from pathlib import Path
import subprocess
import sys

ALLOWED = ['_pages/about.md', 'data/publication_overrides.json', 'data/publication_sync_status.json']


def run(*args, **kwargs):
    return subprocess.run(args, check=True, text=True, **kwargs)


def main():
    if os.environ.get('GITHUB_ACTIONS') != 'true':
        raise RuntimeError('This publisher is restricted to disposable GitHub Actions runners')
    snapshot = str(Path(sys.argv[1]).resolve())
    branch = os.environ['PUBLICATION_BRANCH']
    for attempt in range(3):
        run('git', 'fetch', 'origin', branch)
        # Only this disposable runner is reset. Never reset a user checkout.
        run('git', 'reset', '--hard', 'FETCH_HEAD')
        run(sys.executable, 'scripts/update_publications.py', '--apply', snapshot, '--write')
        run(sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v')
        run('bundle', 'exec', 'jekyll', 'build', '--destination', '/tmp/publication-site')
        run('git', 'diff', '--check')
        run('git', 'add', '--', *ALLOWED)
        staged = subprocess.check_output(['git','diff','--cached','--name-only'], text=True).splitlines()
        if not set(staged).issubset(ALLOWED):
            raise RuntimeError('Unexpected files staged for publication')
        if not staged:
            break
        run('git', 'commit', '-m', 'Update publications and latest five news items')
        result = subprocess.run(['git','push','origin',f'HEAD:{branch}'],text=True)
        if result.returncode == 0:
            break
        if attempt == 2:
            raise RuntimeError('Remote changed repeatedly or push was denied; no force push attempted')
    sha = subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
    with open(os.environ['GITHUB_OUTPUT'],'a') as output:
        output.write('published_sha=' + sha + '\n')


if __name__ == '__main__':
    main()
