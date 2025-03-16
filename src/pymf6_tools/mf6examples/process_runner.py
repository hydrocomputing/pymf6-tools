"""Run as process."""

from contextlib import redirect_stdout, redirect_stderr
import json
from pathlib import Path
import io
import sys
import timeit


def run_func(func):
    """Run function with cmd args."""
    kwargs = json.loads(' '.join(sys.argv[1:]))
    simulation_paths = kwargs.pop('simulation_paths')
    main_path = simulation_paths['main_path']

    res = {}
    for sub_path in simulation_paths['sub_paths']:
        sim_path = str(Path(main_path) / sub_path)
        kwargs['sim_path'] = sim_path
        stdout = io.StringIO()
        stderr = io.StringIO()
        start = timeit.default_timer()
        try:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                func(**kwargs)
            sub_res = {'success': True, 'error': ''}
        except Exception as err:
            stdout.seek(0)
            stderr.seek(0)
            sub_res = {
                'success': False,
                'error': '\n'.join([str(err), stderr.read().strip(), stdout.read().strip()])}
        end = timeit.default_timer()
        sub_res['run_time'] = end - start
        res[sub_path] = sub_res
    print(json.dumps(res))
