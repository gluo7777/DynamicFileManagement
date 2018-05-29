'''
Command Line end point
'''

from file import *

# Script Parameters
FileUtil.LOG = True
config_file = 'resources/config.ini'
scan_dir = ''

# Script Execution
config_ini_file(config_file)
scan_dir = get_default_watch_dir()
scan_files_in_dir(scan_dir, FileUtil.TEST)
