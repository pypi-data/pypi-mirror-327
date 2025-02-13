#!/usr/bin/env python3

"""mg - MultiGit - utility for managing multiple Git repos in a hierarchical directory tree"""

import os
import sys
import argparse
import fnmatch
import configparser
import shlex
from collections import defaultdict

import thingy.git2 as git
import thingy.colour as colour

################################################################################

# DONE: / Output name of each git repo as it is processed as command sits there seeming to do nothing otherwise.
# DONE: Don't save the configuration on exit if it hasn't changed
# DONE: Don't use a fixed list of default branch names
# DONE: Use the configuration file
# DONE: init function
# TODO: -j option to run in parallel?
# TODO: Pull/fetch - only output after running command and only if something updated
# TODO: Better error-handling - e.g. continue/abort option after failure in one repo
# TODO: Consistent colours in output
# TODO: Dry-run option
# DONE: If the config file isn't in the current directory then search up the directory tree for it but run in the current directory
# TODO: If run in a subdirectory, only process repos in that tree (or have an option to do so)
# TODO: Is it going to be a problem if the same repo is checked out twice or more in the same workspace
# TODO: Switch to tomlkit
# TODO: Verbose option
# TODO: When specifying list of repos, if repo name doesn't contain '/' prefix it with '*'?

################################################################################

DEFAULT_CONFIG_FILE = 'multigit.toml'

# If a branch name is specified as 'DEFAULT' then the default branch for the
# repo is used instead.

DEFAULT_BRANCH = 'DEFAULT'

################################################################################

def error(msg, status=1):
    """Quit with an error"""

    sys.stderr.write(f'{msg}\n')
    sys.exit(status)

################################################################################

def show_progress(width, msg):
    """Show a single line progress message"""

    name = msg[:width-1]

    colour.write(f'{name}', newline=False)

    if len(name) < width-1:
        colour.write(' '*(width-len(name)), newline=False)

    colour.write('\r', newline=False)

################################################################################

def find_git_repos(args):
    """Locate and return a list of '.git' directory parent directories in the
       specified path.

       If wildcard is not None then it is treated as a list of wildcards and
       only repos matching at least one of the wildcards are returned.

       If the same repo matches multiple times it will only be returned once. """

    repos = set()

    for root, dirs, _ in os.walk(args.directory):
        if '.git' in dirs:
            if root.startswith('./'):
                root = root[2:]

            if args.repos:
                for card in args.repos:
                    if fnmatch.fnmatch(root, card):
                        if root not in repos:
                            yield root
                            repos.add(root)
                        break
            else:
                if root not in repos:
                    yield root
                    repos.add(root)

################################################################################

def select_git_repos(args, config):
    """Return git repos from the configuration that match the criteria on the
       multigit command line (the --repos, --modified and --branched options)
       or, return them all if no relevant options specified"""

    for repo in config.sections():
        # If repos are specified, then only match according to wildcards, full
        # path or just basename.

        if args.repos:
            for entry in args.repos:
                if '?' in entry or '*' in entry:
                    if fnmatch.fnmatch(repo, entry):
                        matching = True
                        break
                elif '/' in entry:
                    if repo == entry:
                        matching = True
                        break
                elif os.path.basename(repo) == entry:
                    matching = True
                    break

            else:
                matching = False
        else:
            matching = True

        # If branched specified, only match if the repo is matched _and_ branched

        if matching and args.branched:
            if git.branch(path=repo) == config[repo]['default branch']:
                matching = False

        # If modified specified, only match if the repo is matched _and_ modified

        if matching and args.modified:
            if not git.status(path=repo):
                matching = False

        if matching:
            yield config[repo]

################################################################################

def branch_name(name, default_branch):
    """If name is None or DEFAULT_BRANCH return default_branch, otherwise return name"""

    return default_branch if not name or name == DEFAULT_BRANCH else name

################################################################################

def run_git_status(cmd, path, cont=False, redirect=True):
    """Run a git command and exit if it fails"""

    output, status = git.git_run_status(cmd, path=path, redirect=redirect)

    if output:
        colour.write(f'[BOLD:{path}]')
        colour.write()
        colour.write(output, indent=4)

    if status and not cont:
        sys.exit(status)

################################################################################

def mg_init(args, config, console):
    """Create or update the configuration
       By default, it scans the tree for git directories and adds or updates them
       in the configuration, using the current branch as the default branch. """

    # TODO: Update should remove or warn about repos that are no longer present

    # Search for .git directories

    for repo in find_git_repos(args):
        if not args.quiet:
            show_progress(console.columns, repo.name)

        if not repo in config:
            config[repo] = {
                'default branch': git.branch(path=repo)
            }

        remote = git.remotes(path=repo)

        if 'origin' in remote:
            config[repo]['origin'] = remote['origin']
            config[repo]['name']= os.path.basename(remote['origin']).removesuffix('.git')
        else:
            config[repo]['name'] = os.path.basename(repo)

################################################################################

def mg_status(args, config, console):
    """Report Git status for any repo that has a non-empty status"""

    # TODO: More user-friendly output

    for repo in select_git_repos(args, config):
        if not args.quiet:
            show_progress(console.columns, repo.name)

        status = git.status(path=repo.name)
        branch = git.branch(path=repo.name)

        if status or branch != repo['default branch']:
            if branch == repo['default branch']:
                colour.write(f'[BOLD:{repo.name}]')
            else:
                colour.write(f'[BOLD:{repo.name}] - branch: [BLUE:{branch}]')

            staged = defaultdict(list)
            unstaged = defaultdict(list)
            untracked = []

            for entry in status:
                if entry[0] == '??':
                    untracked.append(entry[1])
                elif entry[0][0] == 'M':
                    staged['Updated'].append(entry[1])
                elif entry[0][0] == 'T':
                    staged['Type changed'].append(entry[1])
                elif entry[0][0] == 'A':
                    staged['Added'].append(entry[1])
                elif entry[0][0] == 'D':
                    staged['Deleted'].append(entry[1])
                elif entry[0][0] == 'R':
                    staged['Renamed'].append(entry[1])
                elif entry[0][0] == 'C':
                    staged['Copied'].append(entry[1])
                elif entry[0][1] == 'M':
                    colour.write(f'    WT Updated:      [BLUE:{entry[1]}]')
                elif entry[0][1] == 'T':
                    colour.write(f'    WT Type changed: [BLUE:{entry[1]}]')
                elif entry[0][1] == 'D':
                    unstaged['Deleted'].append(entry[1])
                elif entry[0][1] == 'R':
                    colour.write(f'    WT Renamed:      [BLUE:{entry[1]}]')
                elif entry[0][1] == 'C':
                    colour.write(f'    WT Copied:       [BLUE:{entry[1]}]')
                else:
                    staged['Other'].append(f'    {entry[0]}:    [BLUE:{entry[1]}]')

            if untracked:
                colour.write()
                colour.write('Untracked files:')

                for git_object in untracked:
                    colour.write(f'    [BLUE:{git_object}]')

            if staged:
                colour.write()
                colour.write('Changes staged for commit:')

                for item in staged:
                    for git_object in staged[item]:
                        colour.write(f'    {item}: [BLUE:{git_object}]')

            if unstaged:
                colour.write()
                colour.write('Changes not staged for commit:')

                for item in unstaged:
                    for git_object in unstaged[item]:
                        colour.write(f'    {item}: [BLUE:{git_object}]')

            colour.write()

################################################################################

def mg_fetch(args, config, console):
    """Run git fetch everywhere"""

    _ = config

    for repo in select_git_repos(args, config):
        if not args.quiet:
            show_progress(console.columns, repo.name)

        colour.write(f'Fetching updates for [BLUE:{repo.name}]')

        result = git.fetch(path=repo.name)

        if result:
            colour.write(f'[BOLD:{repo.name}]')
            for item in result:
                if item.startswith('From '):
                    colour.write(f'    [BLUE:{item}]')
                else:
                    colour.write(f'    {item}')

            colour.write()

################################################################################

def mg_pull(args, config, console):
    """Run git pull everywhere"""

    _ = config

    for repo in select_git_repos(args, config):
        if not args.quiet:
            show_progress(console.columns, repo.name)

        colour.write(f'Pulling updates for [BLUE:{repo.name}]')

        try:
            result = git.pull(path=repo.name)
        except git.GitError as exc:
            error(f'Error in {repo.name}: {exc}')

        if result and result[0] != 'Already up-to-date.':
            colour.write(f'[BOLD:{repo.name}]')
            for item in result:
                if item.startswith('Updating'):
                    colour.write(f'    [BLUE:{item}]')
                else:
                    colour.write(f'    {item}')

            colour.write()

################################################################################

def mg_push(args, config, console):
    """Run git push everywhere where the current branch isn't one of the defaults
       and where the most recent commit was the current user and was on the branch
    """

    # DONE: Add option for force-push?
    # TODO: Add option for manual confirmation?

    for repo in select_git_repos(args, config):
        if not args.quiet:
            show_progress(console.columns, repo.name)

        branch = git.branch(path=repo.name)

        if branch != repo['default branch']:
            colour.write(f'Pushing changes to [BLUE:{branch}] in [BOLD:{repo.name}]')

            result = git.push(path=repo.name, force_with_lease=args.force)

            if result:
                colour.write(result, indent=4)

            colour.write()

################################################################################

def mg_checkout(args, config, console):
    """Run git checkout everywhere.
       By default it just checks out the specified branch (or the default branch)
       if the branch exists in the repo.
       If the 'create' option is specified then branch is created"""

    # TODO: Add --create handling
    # TODO: Checkout remote branches
    # TODO: only try checkout if branch exists
    # TODO: option to fetch before checking out

    for repo in select_git_repos(args, config):
        if not args.quiet:
            show_progress(console.columns, repo.name)

        branch = branch_name(args.branch, repo['default branch'])

        if git.branch(path=repo.name) != branch:
            colour.write(f'Checking out [BLUE:{branch}] in [BOLD:{repo.name}]')

            git.checkout(branch, create=args.create, path=repo.name)

################################################################################

def mg_commit(args, config, console):
    """For every repo that has a branch checked out and changes present,
       commit those changes onto the branch"""

    # DONE: Option to amend the commit if it is not the first one on the current branch
    # DONE: Prevent commits if current branch is the default branch
    # DONE: Option to specify wildcard for files to commit (default is all files)

    for repo in select_git_repos(args, config):
        if not args.quiet:
            show_progress(console.columns, repo.name)

        branch = git.branch(path=repo.name)
        modified = git.status(path=repo.name)

        if branch != repo['default branch'] and modified:
            colour.write(f'Committing [BOLD:{len(modified)}] changes onto [BLUE:{branch}] branch in [BOLD:{repo.name}]')

            git.commit(all=True, message=args.message, path=repo.name)

################################################################################

def mg_update(args, config, console):
    """For every repo, pull the default branch and if the current branch
       is not the default branch, rebase it onto the default branch"""

    # TODO: Option to pull current branch
    # TODO: Use git-update
    # TODO: Option to delete current branch before pulling (to get updates without conflicts)
    # TODO: Option to stash changes on current branch before updating and unstash afterwards

    for repo in select_git_repos(args, config):
        if not args.quiet:
            show_progress(console.columns, repo.name)

        branch = git.branch(path=repo.name)
        default_branch = repo['default branch']

        colour.write(f'Updating branch [BLUE:{branch}] in [BOLD:{repo.name}]')

        if branch != default_branch:
            if not args.quiet:
                colour.write(f'Checking out [BLUE:{default_branch}]', indent=4)

            git.checkout(default_branch, path=repo.name)

        if not args.quiet:
            colour.write('Pulling updates from remote', indent=4)

        git.pull(path=repo.name)

        if branch != default_branch:
            if not args.quiet:
                colour.write(f'Checking out [BLUE:{branch}] and rebasing against [BLUE:{default_branch}]', indent=4)

            git.checkout(branch, path=repo.name)
            result = git.rebase(default_branch, path=repo.name)
            colour.write(result[0], indent=4)

################################################################################

def mg_clean(args, config, console):
    """Clean the repos"""

    _ = config

    for repo in select_git_repos(args, config):
        if not args.quiet:
            show_progress(console.columns, repo.name)

        result = git.clean(recurse=args.recurse, force=args.force, dry_run=args.dry_run,
                           quiet=args.quiet, exclude=args.exclude, ignore_rules=args.x,
                           remove_only_ignored=args.X, path=repo.name)

        first_skip = True

        if result:
            colour.write(f'[BOLD:{repo.name}]')

            for item in result:
                skipping = item.startswith('Skipping repository ')

                if skipping and not args.verbose:
                    if first_skip:
                        colour.write('Skipping sub-repositories', indent=4)
                        first_skip = False
                else:
                    colour.write(item.strip(), indent=4)

            colour.write()

################################################################################

def mg_dir(args, config, console):
    """Return the location of a working tree, given the name. Returns an
       error unless there is a unique match"""

    # DONE: Should return location relative to the current directory or as absolute path

    _ = console
    _ = config

    location = []
    search_dir = args.dir[0]

    for repo in select_git_repos(args, config):
        if fnmatch.fnmatch(repo['name'], search_dir):
            location.append(repo.name)

    if len(location) == 0:
        error(f'No matches with {dir}')
    elif len(location) > 1:
        error(f'Multiple matches with {dir}')

    colour.write(os.path.join(os.path.dirname(args.config), location[0]))

################################################################################

def mg_config(args, config, console):
    """Output the path to the configuration file"""

    _ = config
    _ = console

    colour.write(args.config)

################################################################################

def mg_run(args, config, console):
    """Run a command in each of the working trees, optionally continuing if
       there's an error"""

    _ = config

    cmd = shlex.split(args.cmd[0])

    for repo in select_git_repos(args, config):
        if not args.quiet:
            show_progress(console.columns, repo.name)

        run_git_status(cmd, repo.name, args.cont)

################################################################################

def mg_review(args, config, console):
    """Run the git review command"""

    # TODO: Better parsing to replace DEFAULT with default branch only where appropriate

    for repo in select_git_repos(args, config):
        if not args.quiet:
            show_progress(console.columns, repo.name)

        params = []
        for p in args.parameters:
            params += shlex.split(p.replace(DEFAULT_BRANCH, repo['default branch']))

        colour.write(f'Running review in [BOLD:{repo.name}]')
        run_git_status(['review'] + params, repo.name, cont=True, redirect=False)

################################################################################

def find_configuration(args):
    """If the configuration file name has path elements, try and read it, otherwise
       search up the directory tree looking for the configuration file.
       Returns configuration file path or None if the configuration file
       could not be found."""

    if '/' in args.config:
        config_file = args.config
    else:
        config_path = os.getcwd()
        config_file = os.path.join(config_path, args.config)

        while not os.path.isfile(config_file) and config_path != '/':
            config_path = os.path.dirname(config_path)
            config_file = os.path.join(config_path, args.config)

    return config_file if os.path.isfile(config_file) else None

################################################################################

def main():
    """Main function"""

    commands = {
       'init': mg_init,
       'status': mg_status,
       'fetch': mg_fetch,
       'pull': mg_pull,
       'push': mg_push,
       'checkout':  mg_checkout,
       'commit': mg_commit,
       'update': mg_update,
       'clean': mg_clean,
       'dir': mg_dir,
       'config': mg_config,
       'run': mg_run,
       'review': mg_review,
    }

    # Parse args in the form COMMAND OPTIONS SUBCOMMAND SUBCOMMAND_OPTIONS PARAMETERS

    parser = argparse.ArgumentParser(description='Run git commands in multiple Git repos. DISCLAIMER: This is beta-quality software, with missing features and liable to fail with stack dump, but shouldn\'t eat your data')

    parser.add_argument('--dryrun', '--dry-run', '-D', action='store_true', help='Dry-run comands')
    parser.add_argument('--debug', '-d', action='store_true', help='Debug')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbosity to the maximum')
    parser.add_argument('--quiet', '-q', action='store_true', help='Minimal console output')
    parser.add_argument('--config', '-c', action='store', default=DEFAULT_CONFIG_FILE, help=f'The configuration file (defaults to {DEFAULT_CONFIG_FILE})')
    parser.add_argument('--directory', '--dir', action='store', default='.', help='The top-level directory of the multigit tree (defaults to the current directory)')
    parser.add_argument('--repos', '-r', action='append', default=None, help='The repo names to work on (defaults to all repos and can contain shell wildcards and can be issued multiple times on the command line)')
    parser.add_argument('--modified', '-m', action='store_true', help='Select repos that have local modifications')
    parser.add_argument('--branched', '-b', action='store_true', help='Select repos that do not have the default branch checked out')

    subparsers = parser.add_subparsers(dest='command')

    # Subcommands - currently just init, status, fetch, pull, push, with more to come

    parser_init = subparsers.add_parser('init', help='Build or update the configuration file using the current branch in each repo as the default branch')

    parser_status = subparsers.add_parser('status', help='Report git status in every repo that has something to report')
    parser_fetch = subparsers.add_parser('fetch', help='Run git fetch in every repo')
    parser_pull = subparsers.add_parser('pull', help='Run git pull in every repo')

    parser_push = subparsers.add_parser('push', help='Run git push in every repo where the current branch isn\'t the default and the most recent commit was by the current user')
    parser_push.add_argument('--force', '-f', action='store_true', help='Use --force-push-with-least to update a remote branch if the local branch has been rebased')

    parser_checkout = subparsers.add_parser('checkout', help='Checkout the specified branch')
    parser_checkout.add_argument('--create', '-b', action='store_true', help='Create the specified branch and check it out')
    parser_checkout.add_argument('branch', nargs='?', default=None, action='store', help='The branch name to check out (defaults to the default branch)')

    parser_commit = subparsers.add_parser('commit', help='Commit changes')
    parser_commit.add_argument('--message', '-m', action='store', default=None, help='The commit message')

    parser_update = subparsers.add_parser('update', help='Pull the default branch and if the current branch isn\'t the default branch, rebase it onto the default branch')

    parser_clean = subparsers.add_parser('clean', help='Remove untracked files from the working tree')

    parser_clean.add_argument('--recurse', '-d', action='store_true', help='Recurse into subdirectories')
    parser_clean.add_argument('--force', '-f', action='store_true', help='If the Git configuration variable clean.requireForce is not set to false, git clean will refuse to delete files or directories unless given -f or -i')
    #parser_clean.add_argument('--interactive', '-i', action='store_true', help='Show what would be done and clean files interactively.')
    parser_clean.add_argument('--dry-run', '-n', action='store_true', help='Don’t actually remove anything, just show what would be done.')
    #parser_clean.add_argument('--quiet', '-q', , action='store_true', help='Be quiet, only report errors, but not the files that are successfully removed.')
    parser_clean.add_argument('--exclude', '-e', action='store', help='Use the given exclude pattern in addition to the standard ignore rules.')
    parser_clean.add_argument('-x', action='store_true', help='Don’t use the standard ignore rules, but still use the ignore rules given with -e options from the command line.')
    parser_clean.add_argument('-X', action='store_true', help='Remove only files ignored by Git. This may be useful to rebuild everything from scratch, but keep manually created files.')

    parser_dir = subparsers.add_parser('dir', help='Return the location of a working tree, given the repo name')
    parser_dir.add_argument('dir', nargs=1, action='store', help='The name of the working tree')

    parser_config = subparsers.add_parser('config', help='Return the name and location of the configuration file')

    parser_run = subparsers.add_parser('run', help='Run any git command in each of the working trees')
    parser_run.add_argument('--cont', '-c', action='store_true', help='Continue if the command returns an error in any of the working trees')
    parser_run.add_argument('cmd', nargs=1, action='store', help='The command to run (should be quoted)')

    parser_review = subparsers.add_parser('review', help='Review the changes in a working tree')
    parser_review.add_argument('parameters', nargs='*', action='store', help='Parameters passed to the "git review" command')

    # Parse the command line

    args = parser.parse_args()

    # Basic error checking

    if not args.command:
        error('No command specified')

    if args.command not in commands:
        error(f'Unrecognized command "{args.command}"')

    # If the configuration file exists, read it

    config = configparser.ConfigParser()

    args.config = find_configuration(args)

    if args.config:
        config.read(args.config)

    # Command-specific validation

    if args.command == 'init':
        if args.modified or args.branched:
            error('The "--modified" and "--branched" options cannot be used with the "init" subcommand')
    elif not config:
        error(f'Unable to location configuration file "{args.config}"')

    # Get the console size

    try:
        console = os.get_terminal_size()
    except OSError:
        console = None
        args.quiet = True

    # Run the subcommand

    commands[args.command](args, config, console)

    # Save the updated configuration file if it has changed (currently, only the init command will do this).

    if config and args.command == 'init':
        with open(args.config, 'w', encoding='utf8') as configfile:
            config.write(configfile)

################################################################################

def multigit():
    """Entry point"""

    try:
        main()

    # Catch keyboard aborts

    except KeyboardInterrupt:
        sys.exit(1)

    # Quietly fail if output was being piped and the pipe broke

    except BrokenPipeError:
        sys.exit(2)

    # Catch-all failure for Git errors

    except git.GitError as exc:
        sys.stderr.write(exc.msg)
        sys.exit(exc.status)

################################################################################

if __name__ == '__main__':
    multigit()
