
import pytest
from pymf6tools.make_model import clone_model

from pytest_utils import get_full_model_path


@pytest.mark.parametrize(
    'model_name', ['flow_base', 'transport_base'])
def test_base_clone_flow(model_name):
    """Test"""
    model_path = get_full_model_path(model_name)
    clone_model(model_path)
