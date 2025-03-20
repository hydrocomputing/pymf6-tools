"""Process model results."""

from pathlib import Path

import pandas as pd

from .run_models import make_df, make_simulations


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


def diff_mfsims(mf6_mfsim, other_mfsim):
    """Diff mfsim.lst created by two model runs."""
    total = 0
    diffs = 0
    skip_start_tokens = [
        'FILE TYPE:',
        'Run end date and time',
        'Elapsed run time:',
        'Character',
        'Logical',
        'Integer',
        'Real',
        'Total',
        'Virtual',
        'MEMORY MANAGER TOTAL STORAGE BY DATA TYPE',
    ]
    skip_contains_tokens = [
        'INPUT READ FROM UNIT',
    ]
    skip_after = 'System command used to initiate simulation:'
    old_line = ''
    diff_lines = {}
    with open(mf6_mfsim) as mf6, open(other_mfsim) as other:
        for line_mf6, line_other in zip(mf6, other):
            total += 1
            clean_line = line_mf6.lstrip()
            skip = False
            for to_skip in skip_start_tokens:
                if clean_line.startswith(to_skip):
                    skip = True
                    continue
            for to_skip in skip_contains_tokens:
                if to_skip in clean_line:
                    skip = True
                    continue
            if skip:
                continue
            if line_mf6 != line_other:
                if old_line.startswith(skip_after):
                    continue
                diffs += 1
                diff_lines[total] = [line_mf6.rstrip(), line_other.rstrip()]
            old_line = clean_line
    return diffs, diff_lines


class DiffsDataFrame(pd.DataFrame):
    """DataFrame with difference of `mfsin.lst` of two model runs."""

    @classmethod
    def from_diffs_dict(cls, diffs_dict, name_other='other'):
        """Create DatzaFrame from."""
        df = make_df(diffs_dict)
        df.columns = ['line_count', 'lines']
        inst = cls(df[df.line_count > 0])
        inst._name_other = name_other
        return inst

    def get_diffs(self, index, max_colwidth=100):
        """Get DataFrame with diffrence lines for one scenario."""
        lines = self.loc[index].lines
        sel = pd.DataFrame(lines).T
        sel.columns = ['mf6', self._name_other]
        sel.index.name = 'lineno'
        pd.set_option("display.max_colwidth", max_colwidth)
        return sel


def make_diffs(config, name_other, name_mf6='mf6'):
    """Create DataFrame with difference of `mfsin.lst` of two model runs."""
    other_sims = make_simulations(config['tests_path'] / name_other)
    mf6_sims = make_simulations(config['tests_path'] / name_mf6)
    mfsim_diff_counts = {}
    for name, sim in other_sims.items():
        sub_diffs = {}
        for sub_path in sim['sub_paths']:
            model_path = Path(sim['main_path']) / sub_path
            mf6_path = Path(mf6_sims[name]['main_path']) / sub_path
            sub_diffs[sub_path] = diff_mfsims(
                mf6_path / 'mfsim.lst', model_path / 'mfsim.lst'
            )
        mfsim_diff_counts[name] = sub_diffs
    df = DiffsDataFrame.from_diffs_dict(mfsim_diff_counts, name_other=name_other)
    return df
