import os
import subprocess
from optparse import OptionParser

from ..utils import call, config, CallError


def run_init(args):

    opt_parser = OptionParser()
    opt_parser.add_option('-g', '--get')
    opt_parser.add_option('-s', '--sync')
    opt_parser.add_option('-f', '--force')
    opts, args = opt_parser.parse_args(args)

    # Determine if the HEAD exists.
    try:
        call('git rev-parse --verify HEAD', stderr=subprocess.PIPE)
        head_exists = True
    except:
        head_exists = False

    # Make sure that the working dir is clean.
    if head_exists and not opts.force:
        git_status = call('git status -uno --porcelain')
        if git_status.strip():
            print 'Working directory is not clean.'
            print 'Please commit or stash your changes before initializing git-xblob.'
            return 2

    top_level = os.path.abspath(call('git rev-parse --show-toplevel').strip())
    config_path = os.path.join(top_level, '.gitxblobconfig')

    # New config options.
    if opts.get:
        call('git config -f %s xblob.get %s', config_path, opts.get)
    if opts.sync:
        call('git config -f %s xblob.sync %s', config_path, opts.sync)

    # Install user config.
    if os.path.exists(config_path):
        rel_path = os.path.relpath(config_path, os.path.join(top_level, '.git'))
        try:
            call('git config --unset-all include.path %s', rel_path)
        except CallError:
            pass
        call('git config --add include.path %s', rel_path)
    else:
        print 'Could not find .gitxblobconfig.'
        print 'Be sure to manually configure git-xblob, e.g.:'
        print '    git config xblob.get http://example.com/path/to/project'
        print '    git config xblob.sync rsync:example.com:/var/www/path/to/project'

    # Install our filters.
    config('filter.xblob.clean', 'git-xblob clean %f')
    config('filter.xblob.smudge', 'git-xblob smudge %f')
    config('filter.xblob.required', 'true')

    # Force a re-clean.
    if head_exists and config('xblob.get'):
        call('git checkout -f HEAD -- %s', top_level)
