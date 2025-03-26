"""Run controlled models."""

from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import pickle
from shutil import copy2, copytree
from subprocess import run
import sys

import pandas as pd

from pymf6_tools.mf6examples.config import read_config


INPUT_DIR = 'input'


def model_iterdir(base_path, input_dir=INPUT_DIR):
    """Get model directory with controlled inputs."""
    for directory in base_path.iterdir():
        has_sub_dir = False
        for sub_dir in directory.iterdir():
            if sub_dir.is_dir():
                if sub_dir.name == input_dir:
                    continue
                has_sub_dir = True
                yield sub_dir
        if not has_sub_dir:
            yield directory


def copy_model_files(config, input_dir=INPUT_DIR):
    """Copy model input files."""
    controlled_in_path = config['controlled_in_path']
    mf6_examples_path = config['mf6_examples_path']
    tests_path = config['tests_path']
    exe_model_paths = []
    for model_dir in model_iterdir(controlled_in_path):
        parentless_model_dir = Path('/'.join(model_dir.parts[1:]))
        src = mf6_examples_path / parentless_model_dir
        dst = tests_path / model_dir
        dst.mkdir(parents=True, exist_ok=True)
        copytree(src, dst, dirs_exist_ok=True)
        for file in (model_dir / input_dir).iterdir():
            copy2(file, dst / file.name)
        exe_model_paths.append(
            (model_dir.absolute() / 'run.py', dst.absolute())
        )
    return exe_model_paths


def run_controlled(config_file_name='config.ini'):
    """Run all models and store result in HDF5 files."""
    config = read_config(config_file=config_file_name)
    exe_model_paths = copy_model_files(config)
    for exe, model_path in exe_model_paths:
        run(['python', str(exe), str(model_path)], check=True)
