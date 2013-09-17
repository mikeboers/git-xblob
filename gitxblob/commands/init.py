import os
import subprocess

from ..utils import git


def run_init(args):

    # Determine if the HEAD exists.
    try:
        git('rev-parse --verify HEAD', stderr=subprocess.PIPE)
        head_exists = True
    except:
        head_exists = False

    # Make sure that the working dir is clean.
    if head_exists and '-f' not in args:
        git_status = git('status -uno --porcelain')
        if git_status.strip():
            print 'Working directory is not clean.'
            print 'Please commit or stash your changes before initializing git-xblob.'
            return 2

    # Install user config.
    top_level = git('rev-parse --show-toplevel').strip()
    config_path = os.path.join(top_level, '.gitxblobconfig')
    if os.path.exists(config_path):
        for line in open(config_path):
            line = line.strip()
            if not line:
                continue
            git('config ' + line)
    else:
        print 'Could not find .gitxblobconfig; skipping.'

    # Install our filters.
    git('config --replace-all filter.xblob.clean "git-xblob clean %f"')
    git('config --replace-all filter.xblob.smudge "git-xblob smudge %f"')
    git('config --replace-all filter.xblob.required true')

    # Force a re-clean.
    if head_exists:
        git('checkout -f HEAD -- %s', top_level)
