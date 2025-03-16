"""Run plain MODFLOW 6."""


from contextlib import chdir
from subprocess import run

from process_runner import run_func


def run_model(sim_path, exe_path='mf6', dll_path=None):
    """Run one MF6 model."""
    with chdir(sim_path):
        ret = run([exe_path], capture_output=True, encoding='utf-8')
    success = True if ret.returncode == 0 else False
    err_msg = ret.stdout if ret.returncode != 0 else None
    res = {'success': success, 'error': err_msg}
    return res

if __name__ == '__main__':
    run_func(run_model)