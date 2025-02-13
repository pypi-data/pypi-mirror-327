# Thingy

Licence: GPL v3

Author: John Skilleter v0.99

Collection of shell utilities and configuration stuff for Linux and MacOS. Untested on other operating systems.

Permanently (for the forseeable future!) in a beta stage - usable, with a few rough edges, and probably with bugs when used in way I'm not expecting!

The following commands are documented in detail in the help output that can be displayed by running the command with the '--help' option.

This README just contains a summary of the functionality of each command.

# Git Utilities

## ggit

Run a git command in all working trees under the current directory (note that this is not related to multigit (see below)).

## ggrep

Run 'git grep' in all repos under the current directory (note that this is not related to multigit (see below)).

## gitprompt

Output a string containing colour-coded shell nesting level, current directory and git working tree status (used in the shell prompt).

## git ca

Improved version of 'git commit --amend'. Updates files that are already in the commit and, optionally, adds and commits additional files.

## git cleanup

List or delete branches that have already been merged and delete tracking branches that are no longer on the remote.

## git co

Equivalent to 'git checkout' but with intelligent branch matching, so specifying a partial branch name will work if it uniquely matches an existing branch

## git parent

Attempt to determine the parent branch for the specified branch (defaulting to the current one)

## git update

Update the repo from the remote, rebase branches against their parents, optionally run git cleanup

## git wt

Output the top level directory of the git working tree or return an error if we are not in a git working tree.

## git review

Console-based git change review tool.

## multigit

Manage a collection of related git repoitories.

## GitLab Commands

### git mr

Push a feature branch to GitLab and create a merge request

### gl

Command line for GitLab

# General Commands

## addpath

Update a $PATH-type variable by adding or removing entries.

## docker-purge

Stop or kill docker instances and/or remove docker images.

## ffind

Simple file find utility

Implements the functionality of the find command that is regularly used in a simpler fashion and ignores all the options that nobody ever uses.

## linecount

Count lines of code in a directory tree organised by file type.

## py-audit

Query api.osv.dev to determine whether a specified version of a particular Python package is subject to known security vulnerabilities

## readable

Pipe for converting colour combinations to make them readable on a light background

## remdir

Recursively delete empty directories

## rmdupe

Search for duplicate files

## rpylint

Run pylint on all the Python source files in the current tree

## s3-sync

Synchronise files from S3 to local storage.

## strreplace

Simple search and replace utility for those times when trying to escape characters in a regexp to use sed is more hassle than it is worth.

## tfm

Console-based file-manager, similar to Midnight Commander but aiming to be better.

## tfparse

Read JSON Terraform output and convert back to human-readable text
This allows multiple errors and warnings to be reported as there's
no way of doing this directly from Terraform

## trimpath

Intelligently trim a path to fit a given width (used by gitprompt)

## venv-create

Create a script to create/update a virtual environment and run a python script in it.

## xchmod

Command to run chmod only on files that need it (only modifies files that don't have the required permissions already).

## yamlcheck

YAML validator - checks that a file is valid YAML (use yamllint to verify that it is nicely-formatted YAML).

# Obsolescent Utilities

These will be moved to the skilleter-extras package in due course.

## borger

Wrapper for the borg backup utility to make it easier to use with a fixed set of options.

## consolecolours

Display all available colours in the console.

## diskspacecheck

Check how much free space is available on all filesystems, ignoring read-only filesystems, /dev and tmpfs.

Issue a warning if any are above 90% used.

## gphotosync

Utility for syncing photos from Google Photos to local storage

## moviemover

Search for files matching a wildcard in a directory tree and move them to an equivalent location in a different tree

## phototidier

Perform various tidying operations on a directory full of photos:

* Remove leading '$' and '_' from filenames
* Move files in hidden directories up 1 level
* If the EXIF data in a photo indicates that it was taken on date that doesn't match the name of the directory it is stored in (in YYYY-MM-DD format) then it is moved to the correct directory, creating it if necessary.

All move/rename operations are carried out safely with the file being moved having
a numeric suffix added to the name if it conflicts with an existing file.

## photodupe

Search for duplicate images in a directory tree

## splitpics

Copy a directory full of pictures to a destination, creating subdiretories with a fixed number of pictures in each in the destination directory for use with FAT filesystems and digital photo frames.

## sysmon

Simple console system monitor

## window-rename

Monitor window titles and rename them to fit an alphabetical grouping in 'Appname - Document' format.
