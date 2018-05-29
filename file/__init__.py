"""
__init__.py is to tell Python that there are submodules in this directory.
Note: modules refer to *.py files
Helps distinguish user modules named similarly to system modules (e.g. string, datetime).
Can declare 'global' variables here and import by 'import <module-name>'
You can also import other modules in this file so other people can simply import your parent folder
e.g. from module1 import *
"""

from file.FileUtil import config_ini_file
from file.FileUtil import get_default_watch_dir
from file.FileUtil import scan_files_in_dir
