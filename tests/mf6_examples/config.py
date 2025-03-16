from pathlib import Path

import pymf6

# BASE_PATH = Path('models/2025_02_06')
BASE_PATH = Path('models/nogit_short')
MF6_EXAMPLES_PATH = BASE_PATH / 'mf6examples'
TESTS_PATH = BASE_PATH / 'tests'
MF6_EXE_PATH = pymf6.info['exe_path']
MF6_DLL_PATH = pymf6.info['dll_path']
