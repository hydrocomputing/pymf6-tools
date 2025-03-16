"""Run pymf6 without solution loop."""



from pymf6.mf6 import MF6

from pymf6_tools.mf6examples.process_runner import run_func


def run_model(sim_path, exe_path=None, dll_path=None):
    """Run one MF6 model with pymf6 without solution loop."""

    mf6 = MF6(sim_path=sim_path, dll_path=dll_path, do_solution_loop=False)
    for model in mf6.model_loop():
        pass

if __name__ == '__main__':
    run_func(run_model)
