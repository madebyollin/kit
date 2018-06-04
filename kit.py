#!/usr/bin/env python
import subprocess as sh
import sys
import re

class ansi:
    BOLD = '\033[1;97m'
    ENDBOLD = '\033[21;97m'
    WHITE = '\033[0;97m'
    YELLOW = '\033[0;33m'
    YELLOW_B = '\033[0;33m'
    RED = '\033[0;31m'
    RED_B = '\033[1;31m'
    BLUE = '\033[0;94m'
    GREEN = '\033[0;32m'
    BLUE_B = '\033[1;94m'
    CYAN = '\033[0;36m'
    CYAN_B = '\033[1;36m'
    ENDC = '\033[0m'

# Gradually fixing all of the things I hate about git

class Kit:
    @staticmethod
    def init():
        """Initialize a new kit repository in the current directory."""
        sh.run(["git", "init"])

    @staticmethod
    def stage(files=None):
        """Stage files to be included in the next save. `kit stage` stages all files; `kit stage f1 f2 f3` stages {f1, f2, f3}."""
        if not files:
            files = ["."]
        sh.run(["git", "add"] + files)
        Kit.status()

    @staticmethod
    def unstage(files=None):
        """Unstage files from being included in the next save. `kit unstage` unstages all files; `kit unstage f1 f2 f3` unstages {f1, f2, f3}."""
        if not files:
            files = ["."]
        sh.run(["git", "reset", "HEAD", "--"] + files)
        Kit.status()

    @staticmethod
    def diff(files=None):
        if not files:
            files = ["."]
        sh.run(["git", "diff", "--cached"] + files)

    @staticmethod
    def undo(files=None):
        """Undo changes to files, returning them to the last saved version. `kit undo` undoes all changes; `kit undo f1 f2 f3` undoes changes to {f1, f2, f3}."""
        if not files:
            sh.run(["git", "stash"])
            sh.run(["git", "reset", "--hard", "HEAD"])
        else:
            sh.run(["git", "checkout"] + files)

    @staticmethod
    def status():
        branch_regex = r'On branch.*'

        staged_regex = r'Changes.*\n.*unstage\)'
        staged_message = "Staged for next save:"

        unstaged_regex = r'Changes.*\n.*\n.*directory\)'
        unstaged_message = "Unstaged:"

        no_changes_regex = r'no changes added to commit.*\)'

        clean_regex = r'nothing to commit, working tree clean'
        clean_message = '🐱 All changes saved.'

        # Get the status, including colors
        git_status = sh.run(["git", "-c", "color.status=always", "status"], stdout=sh.PIPE)
        git_status_string = git_status.stdout.decode()
        # Remove the branch name; it's already in my prompt
        git_status_string = re.sub(branch_regex, "", git_status_string)
        # Replace other messages
        git_status_string = re.sub(staged_regex, staged_message, git_status_string, flags=re.MULTILINE)
        git_status_string = re.sub(unstaged_regex, unstaged_message, git_status_string, flags=re.MULTILINE)
        git_status_string = re.sub(clean_regex, clean_message, git_status_string, flags=re.MULTILINE)
        # If we don't *have* a staged message, add one
        if re.search(no_changes_regex, git_status_string):
            git_status_string = re.sub(no_changes_regex, "", git_status_string)
            git_status_string = staged_message + "\n" + ansi.CYAN + "\tnone" + ansi.ENDC + "\n" + git_status_string
        # Remove line breaks and over-indenting
        git_status_string = re.sub(r"^\s*\n", "", git_status_string, flags=re.MULTILINE)
        git_status_string = re.sub(r"\t", " " * 4, git_status_string, flags=re.MULTILINE)
        print(git_status_string)

    @staticmethod
    def save(name=None):
        """Save current staged changes into a new version."""
        if not name:
            print("Please name your new version (e.g. kit save 'Fix bug')")
            return
        else:
            sh.run(["git", "commit", "-m"] + name)

    @staticmethod
    def upload():
        """Upload current version to remote server."""
        sh.run(["git", "push"])

    @staticmethod
    def version():
        """Show information about the most recently-saved version."""
        git_commit = sh.run(["git", "-c", "color.ui=always", "show", "--summary"], stdout=sh.PIPE)
        git_commit_string = git_commit.stdout.decode()
        git_commit_string = re.sub("commit", "Version", git_commit_string, count=1)
        print(git_commit_string)

    @staticmethod
    def download():
        """Attempt to combine current version with remote server."""
        sh.run(["git", "pull"])

def main():
    args = sys.argv[1:]
    assert len(args) > 0
    action = args[0]

    if hasattr(Kit, action):
        # if we support it, do it
        method = getattr(Kit, action)
        remaining_args = args[1:]
        if remaining_args:
            method(remaining_args)
        else:
            method()
    else:
        # otherwise, fall back to normal git
        sh.run(["git"] + args)

if __name__ == "__main__":
    main()
