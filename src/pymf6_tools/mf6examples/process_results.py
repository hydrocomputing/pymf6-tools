"""Process model results."""

from pathlib import Path

import pandas as pd


class PostProcessor:
    """Post processor for model run time results."""

    def __init__(self, config):
        self._results = {
            file_name.stem: pd.read_hdf(file_name)
            for file_name in config['out_path'].glob('*.h5')
        }
        for name, obj in self._results.items():
            setattr(self, name, obj)

    def get_errors(self, name):
        """Get runs with errors."""
        df = self.results[name]
        return df[~df.success]
