"""Run as process."""

import json
from pathlib import Path
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
        start = timeit.default_timer()
        try:
            sub_res = func(**kwargs)
        except Exception as err:
            sub_res = {'success': False, 'error': str(err)}
        end = timeit.default_timer()
        sub_res['run_time'] = end - start
        res[sub_path] = sub_res
    print(json.dumps(res))
