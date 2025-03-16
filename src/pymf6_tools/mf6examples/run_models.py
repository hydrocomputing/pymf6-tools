"""Setup models."""

from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import pickle
from shutil import copytree
from subprocess import run
import sys

from config import read_config


def copy_input_files(name, config):
    """Copy MF6 input files to target dir."""
    try:
        copytree(
            src=config['mf6_examples_path'],
            dst=config['tests_path'] / name,
            dirs_exist_ok=True,
        )
    except FileExistsError:
        pass


def order_sub_simulations(sub_simulations):
    """
    Order sub simulations.

    flow < particle < transport < heat
    """
    if not sub_simulations:
        # no sub simulations --> nothing to sort
        return sub_simulations
    order = ('gwf', 'prt', 'gwt', 'gwe')
    old_subs = list(sub_simulations)
    new_subs = []
    for name_part in order:
        for index, entry in enumerate(old_subs):
            if name_part in entry:
                new_subs.append(old_subs.pop(index))
                break
    new_subs.extend(old_subs)
    return new_subs


def run_in_subprocess(runner, **kwargs):
    """Run a subprocess."""
    json_args = json.dumps(kwargs)
    ret = run(
        [sys.executable, runner, json_args],
        capture_output=True,
        encoding='utf-8',
    )
    try:
        res = json.loads(ret.stdout)
    except json.JSONDecodeError:
        print(ret.stdout)
        res = {}
    if ret.returncode != 0:
        sub_paths = kwargs['simulation_paths']['sub_paths']
        res = {
            sub_path: {
                'success': False,
                'error': 'process did not run\n' + ret.stderr,
                'run_time': 0,
            }
            for sub_path in sub_paths
        }
    return res


def make_simulations(models_path):
    """Create simulations."""
    mfsim = 'mfsim.nam'
    simulations = {}
    for sim_project in models_path.iterdir():
        index = len(sim_project.parts)
        sub_simulations = [
            sub.parts[index] for sub in sim_project.rglob(mfsim)
        ]
        sub_simulations = [
            entry if entry != mfsim else '' for entry in sub_simulations
        ]
        simulations[sim_project.stem] = {
            'main_path': str(sim_project),
            'sub_paths': order_sub_simulations(sub_simulations),
        }
    return simulations

def run_all_models(
    config,
    runners_path_name='runners',
):
    """Run all models."""
    runners = list(Path(runners_path_name).glob('run_*.py'))
    for runner in runners:
        copy_input_files(config=config, name=runner.stem.split('_', 1)[1])
    futures = {}
    results = {}
    with ThreadPoolExecutor(max_workers=8) as executor:
        for runner in runners:
            name = runner.stem.split('_', 1)[1]
            simulations = make_simulations(models_path=config['tests_path'] / name)
            for simulation_name, simulation_paths in simulations.items():
                key = (name, simulation_name)
                futures[key] = executor.submit(
                    run_in_subprocess,
                    runner,
                    simulation_paths=simulation_paths,
                    exe_path=str(config['mf6_exe_path']),
                    dll_path=str(config['mf6_dll_path']),
                )
        for key, future in futures.items():
            runner_name, model = key
            results.setdefault(runner_name, {})[model] = future.result()
    return results


def run_and_store_models(pickle_file_name='results.pcl', config_file_name='config.ini'):
    """Run models and save results."""
    config = read_config(config_file=config_file_name)
    with open(pickle_file_name, 'wb') as fobj:
        pickle.dump(run_all_models(config), file=fobj)
