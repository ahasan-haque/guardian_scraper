from views import ArticleByID, ArticlesByKeyword
import utils
from conf import services
from nltk import SnowballStemmer
import bson
from unittest.mock import patch, Mock

stemmer = SnowballStemmer('english')


def test_single_article_endpoint_fake_id():
    request_object = ArticleByID()
    mocked_db_object = Mock()
    mocked_db_object.find_one.return_value = {"_id": 1}
    request_object.article_db = mocked_db_object

    # First sending a fake attribute_id
    attr_id = "sad121309923188980921a34"
    response = request_object.get(attr_id)
    mocked_db_object.assert_not_called()
    assert response == ({}, 404)


def test_single_article_endpoint_valid_id():
    request_object = ArticleByID()
    mocked_db_object = Mock()
    attr_id = str(bson.ObjectId())
    mocked_db_object.find_one.return_value = {"_id": attr_id}
    request_object.article_db = mocked_db_object

    response = request_object.get(attr_id)
    mocked_db_object.find_one.assert_called_once_with(
        {
            '_id' : bson.ObjectId(attr_id)
        },
        {
            'keyword': 0
        }
    )
    assert response == ({'id': attr_id}, 200)


@patch.object(stemmer, 'stem', lambda x: x)
def test_articles_endpoint_with_keyword():
    request_object = ArticlesByKeyword()
    parser_object = Mock()
    parser_object.parse_args.return_value = {
        "offset": 1,
        "limit": 2,
        "keyword": " ThreE "
    }
    request_object.parser = parser_object

    query_function = Mock()
    query_function.return_value = {'key': 'value'}
    request_object.perform_query = query_function

    response = request_object.get()

    request_object.perform_query.assert_called_once_with(1, 2, {'keyword': 'three'})

    assert response == ({'key': 'value'}, 200)


@patch.object(stemmer, 'stem', lambda x: x)
def test_articles_endpoint_without_keyword():
    request_object = ArticlesByKeyword()
    parser_object = Mock()
    parser_object.parse_args.return_value = {
        "offset": 1,
        "limit": 2,
        "keyword": ""
    }
    request_object.parser = parser_object

    query_function = Mock()
    query_function.return_value = {}
    request_object.perform_query = query_function

    response = request_object.get()

    request_object.perform_query.assert_called_once_with(1, 2, {})

    assert response == ({}, 404)


def test_perform_query_empty():
    request_object = ArticlesByKeyword()
    mocked_db_object = Mock()
    mocked_db_object.find.\
        return_value.limit.\
        return_value.skip.\
        return_value.count.\
        return_value = 0
    request_object.article_db = mocked_db_object
    response = request_object.perform_query(1,2, {})
    assert response == {}