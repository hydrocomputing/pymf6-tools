from pathlib import Path

from pymf6tools.make_model import make_input
from pymf6tools.base_model import make_model_data


def test_base_flow():
    specific_model_data = {
        'model_path': Path(__file__).parent / 'models' / 'flow_base',
        'name': 'flowbase',
        'transport': False,
        }
    model_data = make_model_data(specific_model_data)
    make_input(model_data)