from conf import services
from bson import ObjectId
from flask_restful import Resource


class ArticleByID(Resource):
    """
    Retrive single article by ID

    """

    def get(self, article_id):
        article_db = services.mongo.guardian.news

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
    pass