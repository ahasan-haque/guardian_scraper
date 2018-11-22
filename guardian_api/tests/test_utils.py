from unittest.mock import patch, Mock
from utils import pre_process_fields


def test_pre_process_fields():
    param_dict = {
                  'offset': 0,
                  'limit': 10,
                  'author': '',
                  'category': '',
                  'sub-category': '',
                  'date': '',
                  'keyword': ''
                  }
    assert pre_process_fields(param_dict) == (0, 10, {})