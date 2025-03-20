"""Read config."""

from configparser import ConfigParser, ExtendedInterpolation
from pathlib import Path

import pymf6

def read_config(config_file):
    """Read config."""
    if not Path(config_file).exists():
        raise FileNotFoundError(config_file)
    config = ConfigParser(interpolation=ExtendedInterpolation())
    config.read(config_file)
    for name in ['mf6_exe_path', 'mf6_dll_path']:
        if not config['paths'][name]:
            config['paths'][name] = str(pymf6.info[name.split('_', 1)[1]])
    return {name: Path(value) for name, value in dict(config['paths']).items()}