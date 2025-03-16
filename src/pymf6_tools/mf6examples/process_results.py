"""Process model results."""

import pickle
from pathlib import Path

import pandas as pd


def make_df(dic):
    """Create data frame from dictionary."""
    transposed_dict = {(key, sub_key): sub_values for key, values in dic.items()
                       for sub_key, sub_values in values.items()}
    return pd.DataFrame(transposed_dict.values(), index=transposed_dict.keys())


def store_dfs(pickle_file, out_path=Path()):
    """"Store model results as data frames."""
    with open(pickle_file, 'rb') as fobj:
        res = pickle.load(fobj)
    for name, data in res.items():
        df = make_df(data)
        df.to_hdf(out_path / f'{name}.h5', key=name)
