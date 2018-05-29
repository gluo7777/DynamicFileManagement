import re
from collections import namedtuple

'''
Regex that matches part of file name string
'''
PREFIX = r'(?P<prefix>[A-Za-z]+)'
JOIN = r'(?:_|-|\.|%)'
FILE_NAME = r'(?P<name>(\w|-|\.|\s)+)'
SUFFIX = r'(?P<suffix>[A-Za-z]+)'
EXTENSION = r'(?P<extension>\.[A-Za-z]+)'

'''
Reusable Regex Object
'''
file_pattern = re.compile(PREFIX + JOIN + FILE_NAME + JOIN + SUFFIX + EXTENSION, re.IGNORECASE)

'''
Named tuple for conveniently accessing matched file parts
'''
file_parts = namedtuple('FileParts', [
    'prefix',
    'name',
    'suffix',
    'extension'
])


def get_file_parts(file_name):
    """

    :rtype: FileParts
    :type file_name: str
    """
    file_match = file_pattern.match(file_name)
    if file_match:
        return file_parts(
            file_match.group('prefix'),
            file_match.group('name'),
            file_match.group('suffix'),
            file_match.group('extension')
        )
    else:
        return None
