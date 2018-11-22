from urllib.parse import urlencode
from datetime import datetime
from nltk import SnowballStemmer
from nltk.corpus import stopwords

stemmer = SnowballStemmer('english')
stop_words = stopwords.words('english')


def evaluate_query_param(param_dict):
    query_param = [(key, value) for key, value in param_dict.items()]
    return urlencode(query_param)


def pre_process_fields(param_dict):
    offset = param_dict.pop('offset')
    limit = param_dict.pop('limit')

    keyword = param_dict.pop('keyword').strip().lower()

    if keyword:
        # Stemming the keyword, as keywords saved in db also stemmed
        param_dict['keyword'] = stemmer.stem(keyword)

    # Checked if date is vaild
    if 'date' in param_dict:
        try:
            datetime.strptime(param_dict['date'], '%Y-%m-%d')
        except ValueError:
            del param_dict['date']
        else:
            param_dict['creation_date'] = param_dict.pop('date')

    if not param_dict['author']:
        del param_dict['author']

    if not param_dict['category']:
        del param_dict['category']

    if param_dict['sub-category']:
        param_dict['sub_category'] = param_dict.pop('sub-category')
    else:
        del param_dict['sub-category']

    return offset, limit, param_dict


def post_process_fields(param_dict):
    print(param_dict)
    if 'creation_date' in param_dict:
        param_dict['date'] = param_dict.pop('creation_date')

    if 'sub_category' in param_dict:
        param_dict['sub-category'] = param_dict.pop('sub_category')

    return param_dict