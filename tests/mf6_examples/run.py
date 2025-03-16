"""Setup a  model."""

from pymf6_tools.mf6examples.run_models import run_and_store_models
from pymf6_tools.mf6examples.process_results import store_dfs


def main(pickle_file='out/results.pcl', out_path='out'):
    run_and_store_models(pickle_file)
    store_dfs(pickle_file=pickle_file, out_path=out_path)

if __name__ == '__main__':
    main()
