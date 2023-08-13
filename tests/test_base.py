import os
from pathlib import Path

from pymf6tools.make_model import make_input
from pymf6tools.base_model import make_model_data

from pytest_utils import get_full_model_path, rmtree

def do_test(specific_model_data, model_path):
    rmtree(model_path)
    model_data = make_model_data(specific_model_data)
    make_input(model_data)
    found_files = set(path.name for path in model_path.glob('*'))
    found_files.remove('.internal')
    model_file_names = set((model_path / '.internal' / 'model_files'
                        ).read_text().split('\n'))
    assert model_file_names == found_files


def test_base_flow():
    model_path = get_full_model_path('flow_base')
    specific_model_data = {
        'model_path': model_path,
        'name': 'flowbase',
        'transport': False,
        }
    do_test(specific_model_data, model_path)


def test_base_transport():
    model_path = get_full_model_path('transport_base')
    specific_model_data = {
        'model_path': model_path,
        'name': 'transportbase',
        'transport': True,
        }
    do_test(specific_model_data, model_path)
