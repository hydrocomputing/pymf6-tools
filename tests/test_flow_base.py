from pathlib import Path

from pymf6tools.make_model import make_input
from pymf6tools.base_model import make_model_data


def get_full_model_path(path_name):
    return Path(__file__).parent / 'models' / path_name


def test_base_flow():
    model_path = get_full_model_path('flow_base')
    specific_model_data = {
        'model_path': model_path,
        'name': 'flowbase',
        'transport': False,
        }
    model_data = make_model_data(specific_model_data)
    model_file_names = make_input(model_data)
    assert model_file_names == set(path.name for path in model_path.glob('*'))
