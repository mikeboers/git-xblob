import os
import subprocess
from optparse import OptionParser

from ..utils import git, call, CallError


def run_init(args):

    opt_parser = OptionParser()
    opt_parser.add_option('-g', '--get')
    opt_parser.add_option('-p', '--put')
    opt_parser.add_option('-f', '--force')
    opts, args = opt_parser.parse_args(args)

    # Determine if the HEAD exists.
    try:
        git('rev-parse --verify HEAD', stderr=subprocess.PIPE)
        head_exists = True
    except:
        head_exists = False

    # Make sure that the working dir is clean.
    if head_exists and not opts.force:
        git_status = git('status -uno --porcelain')
        if git_status.strip():
            print 'Working directory is not clean.'
            print 'Please commit or stash your changes before initializing git-xblob.'
            return 2

    top_level = os.path.abspath(git('rev-parse --show-toplevel').strip())
    config_path = os.path.join(top_level, '.gitxblobconfig')

    # New config options.
    if opts.get:
        call('git config -f %s xblob.get %s', config_path, opts.get)
    if opts.put:
        call('git config -f %s xblob.put %s', config_path, opts.put)

    # Install user config.
    if os.path.exists(config_path):
        rel_path = os.path.relpath(config_path, os.path.join(top_level, '.git'))
        call('git config --add include.path %s', rel_path)
    else:
        print 'Could not find .gitxblobconfig.'
        print 'Be sure to manually configure git-xblob, e.g.:'
        print '    git config xblob.get http://example.com/path/to/project'
        print '    git config xblob.put scp:example.com:/var/www/path/to/project'

    # Install our filters.
    git('config --replace-all filter.xblob.clean "git-xblob clean %f"')
    git('config --replace-all filter.xblob.smudge "git-xblob smudge %f"')
    git('config --replace-all filter.xblob.required true')


    # Force a re-clean.
    if head_exists:
        try:
            get_url = call('git config xblob.get')
        except CallError:
            pass
        else:
            git('checkout -f HEAD -- %s', top_level)
