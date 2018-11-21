from urllib.parse import urlencode


def evaluate_query_param(param_dict):
    query_param = [(key, value) for key, value in param_dict.items()]
    return urlencode(query_param)
