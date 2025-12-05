class FetchArticleError(Exception):
    """
    Unable to Fetch the Aritcle from web.
    The given site might not be Supported by us.
    """
class QdrantDBError(Exception):
    """
    Something went Wrong with Qdrant
    """
class MongoDBError(Exception):
    """
    Something went Wrong with Mongo-DB
    """