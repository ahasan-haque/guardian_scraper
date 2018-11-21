from conf import services
from utils import evaluate_query_param
from bson import ObjectId
from flask import request
from flask_restful import Resource, reqparse
from nltk import SnowballStemmer
from nltk.corpus import stopwords

stemmer = SnowballStemmer('english')
stop_words = stopwords.words('english')


class ArticleByID(Resource):
    """
    Retrieve Single article by ID
    """
    def get(self, article_id):
        article_db = services.mongo.guardian.news

        # not exposing `keyword` field as it's for internal queries
        article = article_db.find_one(
            {
                '_id': ObjectId(article_id)
            },
            {
                'keyword': 0
            }
        )
        article['id'] = str(article.pop('_id'))

        return article, 200


class ArticlesByKeyword(Resource):
    """
    Retrive Articles by keyword

    """

    parser = reqparse.RequestParser()
    parser.add_argument('keyword', type=str, default='')

    # can optionally pass `limit` and `offset`
    # To customize pagination parameters
    parser.add_argument('limit', type=int, default=10)
    parser.add_argument('offset', type=int, default=0)

    def get(self):
        query_params = self.parser.parse_args()
        offset = query_params.pop('offset')
        limit = query_params.pop('limit')

        keyword = query_params.pop('keyword').strip().lower()

        if keyword:
            # Stemming the keyword, as keywords saved in db also stemmed
            query_params['keyword'] = stemmer.stem(keyword)

        # Taking query_params as search criteria (except limit and offset)
        # This way a single endpoint can handle multiple field to filter
        search_criteria = query_params

        response = self.perform_query(offset, limit, search_criteria)
        return response, 200

    def perform_query(self, offset, page_size, search_criteria):
        article_db = services.mongo.guardian.news
        cursor = article_db.find(
            search_criteria,
            {
                'keyword': 0,
            }
        )
        # Cursor is trimmed with pagination paramters
        paginated_documents = cursor.limit(page_size).skip(offset)

        # Send empty dict if no document is matched
        document_count = paginated_documents.count()
        if not document_count:
            return {}

        # casting `_id` to str as ObjectID isn't serializable
        data = []
        for document in paginated_documents:
            document['id'] = str(document.pop('_id'))
            data.append(document)

        # Calculating offset for next and previous page
        previous_offset = offset - page_size
        next_offset = offset + page_size

        response = {'articles': data}

        if previous_offset > 0:
            # param_dict is formed to dynamically build the query param part
            # of the pagination URLs
            param_dict = dict(search_criteria)
            param_dict.update({
                'offset': previous_offset,
                'limit': page_size
            })
            response['previous_page'] = '{}?{}'.format(request.base_url,evaluate_query_param(param_dict))

        if next_offset < document_count:
            param_dict = dict(search_criteria)
            param_dict.update({
                'offset': next_offset,
                'limit': page_size
            })
            response['next_page'] = '{}?{}'.format(request.base_url,evaluate_query_param(param_dict))

        return response
