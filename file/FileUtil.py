'''
Utility constants and methods for operating on a directory
'''


from configparser import ConfigParser, ExtendedInterpolation
from pathlib import Path
from datetime import datetime, timezone
from file.RegexUtil import get_file_parts

# constants
CLOUD = 'cloud'
LOCAL = 'local'
TEST = 'test'

# Logging
LOG = True
TOKEN = '-'
INC = 3

# Global variables
file_parser = None


'''
In-Script Methods
'''


def log(output, level=0):
    if LOG:
        print(TOKEN * level * INC, output)


def config_ini_file(file_path='resources/config.ini'):
    # Specify global vars so they can be modified in local/function scope
    global file_parser
    # Make sure file exists
    config_file = Path(file_path)
    assert all([config_file.exists()])
    # Initialize parser
    file_parser = ConfigParser(allow_no_value=True,
                               comment_prefixes='#',
                               strict=True,
                               empty_lines_in_values=False,
                               interpolation=ExtendedInterpolation())
    file_parser.read(config_file)
    if LOG:
        log('Configuration File Paths:', 0)
        for section in file_parser.sections():
            log(f'In section {section}', 1)
            for item in file_parser.items(section):
                log(f'{item[0]}={item[1]}', 2)


def get_default_watch_dir():
    global file_parser
    return file_parser['Default']['watch']


def expand_file_path(prefix='default', suffix='default', root='default'):
    global file_parser
    root = file_parser['Base'][root] if root in file_parser['Base'] else file_parser['Base']['default']
    prefix = file_parser['Prefix'][prefix] if prefix in file_parser['Prefix'] else file_parser['Prefix']['default']
    suffix = file_parser['Suffix'][suffix] if suffix in file_parser['Suffix'] else file_parser['Suffix']['default']
    return Path(root) / prefix / suffix


def move_file(src, dest):
    assert src is not None and dest is not None
    if not dest.exists():
        src.rename(dest)
    else:
        print(f'\'{dest}\' already exists.')


def append_time_stamp(name):
    return name + '_' + datetime.now(timezone.utc).strftime('%Y_%m_%d_%H_%M_%S_%f')


'''
End of In-Script Methods
'''


def scan_files_in_dir(file_path, root_dir=TEST):
    """
    Optional file_path. Overrides get_default_watch_dir().
    Iterates each file in file_path and ones that match format will be moved and renamed to the new mapped file paths.
    :param root_dir: str
    :rtype: None
    :type file_path: str
    """
    watch_dir = Path(file_path)
    assert all([watch_dir.exists(), watch_dir.is_dir()])
    log(f'Files in \'{watch_dir}\':', 0)
    for src in watch_dir.iterdir():
        parts = get_file_parts(src.name)
        log(src.name, 1)
        log(parts, 2)
        if parts:
            root = expand_file_path(
                parts.prefix,
                parts.suffix,
                root=root_dir
            )
            dest = root / (parts.name + parts.extension)
            log(f'Expanded File Path: {dest}', 3)
            # move, not copy, to above path
            if not dest.exists():
                # Creates any missing in-between parent directories
                parent = Path(dest.parent)
                if not parent.exists():
                    parent.mkdir(parents=True, exist_ok=True)
                src.rename(dest)
            else:
                log(f'\'{dest}\' already exists.', 3)
                # handling dupes -> append time stamp
                name_ts = append_time_stamp(parts.name)
                dest = root / (name_ts + parts.extension)
                log(f'Expanded File Path: {dest}', 3)
                src.rename(dest)
