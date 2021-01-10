from typing import List, Optional, Tuple, Iterable

import os
import sys
import enum
import shutil
import argparse

# CLI related stuff to parse commands and arguments ---------------------------
# Based on https://mike.depalatis.net/blog/simplifying-argparse.html

cli = argparse.ArgumentParser()
subparsers = cli.add_subparsers(dest="subcommand")

def command(args=[], parent=subparsers):
    def decorator(func):
        parser = parent.add_parser(func.__name__, description=func.__doc__)
        for arg in args:
            parser.add_argument(*arg[0], **arg[1])
        parser.set_defaults(func=func)
    return decorator

def arg(*name_or_flags, **kwargs):
    return ([*name_or_flags], kwargs)


# Utilities -------------------------------------------------------------------

def banner(): 
    info("dotfiles installer")


def ask(question: str, valid_options=None, *, one_shot=False):
    prompt = f"{question} {valid_options}: "
    while True:
        value = input(prompt)
        if one_shot or value in valid_options:
            return value


def error(message: str, *, exit_status: int = None, end: str = "\n"):
    if message != "":
        print(f"[ERROR] {message}", end=end)
    if exit_status is not None:
        exit(exit_status)


def warning(message: str, *, end: str = "\n"):
    print(f"[WARNING] {message}", end=end)
    

def info(message: str, *, end: str = "\n"):
    print(message, end=end)


# Config management -----------------------------------------------------------
def get_config_prefix(name: Optional[str]=None) -> str:
    prefix = "configs"
    if name is None:
        return prefix
    
    prefix = os.path.abspath(os.path.join(prefix, name))
    
    # if not prefix.endswith(os.sep):
    #     prefix = prefix + os.sep

    return prefix

def get_config_list() -> List[Tuple[str, str]]:
    for root, dirs, _ in os.walk(get_config_prefix()):
        for d in dirs:
            yield d, os.path.join(root, d)
        break # we don't want to recurse subdirectories


def get_config_location(name: str) -> Optional[str]:
    location = os.path.join(get_config_prefix(), name)
    if os.path.exists(location) and os.path.isdir(location):
        return location
    return None


def get_default_config_target() -> str:
    """ Get the default target location to put the config files. Depends on
    operating system """
    platform = sys.platform

    if platform == "linux":
        return os.path.expanduser("~")
    else:
        error(f"Unsupported platform: {platform}", exit_status=-1)


def get_config_target(name: str) -> str:
    if not exists_config(name):
        error(f"Can't find target location for config: {name}", exit_status=-1)

    target = get_default_config_target()

    # TODO: we may need a config target override, for example on Windows
    #   the files may have a different layout or be located in different
    #   folders than $HOME...    
    return target
    

def get_config_message(name: str) -> List[str]:
    message_file = os.path.join(get_config_prefix(), f"{name}.message")
    if os.path.exists(message_file):
        with open(message_file) as f:
            return f.readlines()
    else:
        return []


def exists_config(name: str) -> bool:
    return get_config_location(name) is not None


def get_diff(source_file: str, target_file: str) -> Iterable[str]:
    import difflib
    with open(source_file, "r") as source:
        with open(target_file, "r") as target:
            diff = difflib.unified_diff(
                source.readlines(),
                target.readlines(),
                fromfile = source_file,
                tofile=target_file
            )
            return diff


def _copy_config(name: str, source: str, target_folder: str, *, overwrite=False) -> bool:
    prefix = get_config_prefix(name)
    assert source.startswith(prefix)
    
    sub_path = os.path.relpath(source, prefix)
    final_location = os.path.join(target_folder, sub_path)
    final_folder = os.path.dirname(final_location)
    
    info(f"    [{source}] -> [{final_location}]")
    if not final_location.startswith(target_folder):
        error("Final location is not within target?", exit_status=-1)

    if os.path.exists(final_location) and not overwrite:
        diff = [x for x in get_diff(source, final_location)]
        if len(diff) == 0:
            warning("File already present with same contents. Ignored.")
            # same files, same content...
            return True

        error("File already exists. Use --overwrite to override the content.")        
        info("Here is a diff for your convenience:\n")
        for line in diff:
            info(f"    {line}", end="")
        error("", exit_status=-1)
        return False
    
    os.makedirs(final_folder, exist_ok=True)
    shutil.copy(source, final_location)
    return True
    

class InstallMode(enum.Enum):
    Copy = 0 # Copy files to final location (cp)
    Link = 1 # Link files to final location (akin to ln -s)


def install_config(name: str, *, mode: InstallMode = InstallMode.Copy, overwrite=False) -> bool:
    location = get_config_location(name)
    if not location:
        error("Config doesn't exist", exit_status=-1)

    info(f"Installing config for: {name}")
    info(f"- Overwrite files?: {overwrite}")
    info(f"- Install mode: {mode.name}")

    target = get_config_target(name)
    info(f"- Target: {target}")    

    for root, _, files in os.walk(location):
        # for dir in dirs:
        #     info(os.path.join(root, dir))
        for file in files:
            # info(os.path.join(root, file))
            if mode == InstallMode.Copy:
                source_path = os.path.abspath(os.path.join(root, file))
                if not _copy_config(name, source_path, target, overwrite=overwrite):
                    error("Cannot copy file to target. Does the file exist already?")

    message = get_config_message(name)
    if len(message) > 0:
        info("- Message:")
        for line in message:
            info(f"    {line.rstrip()}")


# Command implementation ------------------------------------------------------

@command()
def list(args):
    info("Available configs:")
    for name, location in get_config_list():
        info(f"- {name} ({location})")


@command([
    arg("-n", "--name", help="Name of the config to install", required=False)
    , arg("--overwrite", help="Overwrite all config files", required=False, default=False, action="store_true")
])
def install(args):
    if not args.name:
        if "yes" == ask("Install all configuration files?", ["yes", "no"], one_shot=True):
            for name, _ in get_config_list():
                warning(f"TODO: install everything: {name}")
        return
    install_config(
        args.name,
        overwrite=args.overwrite
    )

# Main ------------------------------------------------------------------------

def main():
    banner()
    args = cli.parse_args()
    if args.subcommand is None:
        cli.print_help()
    else:
        args.func(args)


if __name__ == "__main__":
    main()