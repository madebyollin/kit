#!/usr/bin/env python
import subprocess as sh
import sys

# Gradually fixing all of the things I hate about git

class Kit:
    @staticmethod
    def init():
        sh.run(["git", "init"])

    @staticmethod
    def stage(files=None):
        if not files:
            files = ["."]
        sh.run(["git", "add"] + files)

    @staticmethod
    def unstage(files=None):
        if not files:
            files = ["."]
        sh.run(["git", "reset", "HEAD", "--"] + files)

    @staticmethod
    def diff(files=None):
        if not files:
            files = ["."]
        sh.run(["git", "diff", "--cached"] + files)

    @staticmethod
    def status():
        sh.run(["git", "status"])

    @staticmethod
    def save(name=None):
        if not name:
            print("Please name your new version (e.g. kit save 'Fix bug')")
            return
        else:
            sh.run(["git", "commit", "-m"] + name)

    @staticmethod
    def upload():
        sh.run(["git", "push"])

    @staticmethod
    def download():
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
