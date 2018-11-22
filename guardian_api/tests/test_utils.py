from unittest.mock import patch, Mock
from utils import pre_process_fields, stemmer, post_process_fields


@patch.object(stemmer, 'stem', lambda x: x)
def test_pre_process_fields():
    # test with blank values
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

    # test keyword normalization
    param_dict = {
                  'offset': 0,
                  'limit': 10,
                  'author': 'Some One',
                  'category': '',
                  'sub-category': '',
                  'date': '',
                  'keyword': '  whiTespacecaSensiTive'
                  }
    assert pre_process_fields(param_dict) == (0, 10, {'author': 'Some One', 'keyword': 'whitespacecasensitive'})

    # test invalid date
    param_dict = {
                  'offset': 0,
                  'limit': 10,
                  'author': '',
                  'category': '',
                  'sub-category': '',
                  'date': '12-13-14',
                  'keyword': ''
                  }
    assert pre_process_fields(param_dict) == (0, 10, {})

    # date not in proper format
    param_dict = {
                  'offset': 0,
                  'limit': 10,
                  'author': '',
                  'category': '',
                  'sub-category': '',
                  'date': '18-Dec-2018',
                  'keyword': ''
                  }
    assert pre_process_fields(param_dict) == (0, 10, {})

    # proper date input (%Y-%m-%d)
    param_dict = {
                  'offset': 0,
                  'limit': 10,
                  'author': '',
                  'category': '',
                  'sub-category': '',
                  'date': '2018-12-10',
                  'keyword': ''
                  }
    assert pre_process_fields(param_dict) == (0, 10, {'creation_date': '2018-12-10'})

    # check sub-category field name check
    param_dict = {
                  'offset': 0,
                  'limit': 10,
                  'author': '',
                  'category': '',
                  'sub-category': 'Test Data',
                  'date': '',
                  'keyword': ''
                  }
    assert pre_process_fields(param_dict) == (0, 10, {'sub_category': 'Test Data'})


def test_post_process_fields():
        param_dict = {
            'fake_field': 'value'
        }
        assert post_process_fields(param_dict) == {'fake_field': 'value'}

        param_dict = {
            'creation_date': 'somedate'
        }
        assert post_process_fields(param_dict) == {'date': 'somedate'}

        param_dict = {
            'sub_category': 'football'
        }
        assert post_process_fields(param_dict) == {'sub-category': 'football'}

        param_dict = {
            'creation_date': 'somedate',
            'fake_field': 'value'
        }
        assert post_process_fields(param_dict) == {'date': 'somedate', 'fake_field': 'value'}

