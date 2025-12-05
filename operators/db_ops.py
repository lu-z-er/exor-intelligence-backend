from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import pymongo
from bson import ObjectId


class QdrantStorage:
    def __init__(self, url="http://localhost:6333", collection="news", dim=768):
        try:
            self.client = QdrantClient(url=url, timeout=30)
            self.collection = collection
            if not self.client.collection_exists(self.collection):
                self.client.create_collection(
                    collection_name=self.collection,
                    vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
                )
        except Exception:
            raise

    def upsert(self, ids, vectors, payloads):
        try:
            points = [PointStruct(id=ids[i], vector=vectors[i], payload=payloads[i]) for i in range(len(ids))]
            self.client.upsert(self.collection, points=points)
        except Exception:
            raise

    def search(self, query_vector, top_k: int = 5):
        try: 
            results = self.client.search(
                collection_name=self.collection,
                query_vector=query_vector,
                with_payload=True,
                limit=top_k,
            )
            contexts = []
            sources = []

            for r in results:
                payload = getattr(r, "payload", None) or {}
                text = payload.get("text", "")
                source = payload.get("source", "")
                if text:
                    contexts.append(text)
                    sources.append(source)

            return {"documents": contexts, "sources": sources}
        except Exception:
            raise
    
class MongoStorage:
    def __init__(self, url="http://localhost:5271", db="test"):
        try:
            self.mongo_client = pymongo.MongoClient(url)
            self.articles_collection= self.mongo_client[db]["articles"]
            self.user_collection = self.mongo_client[db]["users"]
        except Exception: 
            raise

    def query_articles(self, article_id):
        try:
            myquery = {"_id": ObjectId(article_id)}
            mydoc = self.articles_collection.find_one(myquery)
            return mydoc
        except Exception:
            raise
    def query_user_articles(self, user_id, article_id):
        try:
            my_query = {
                "_id": ObjectId(user_id),
                "uploadedArticles._id": ObjectId(article_id)
            }
            my_doc = self.user_collection.find_one(my_query, {
                "_id": 0,
                "uploadedArticles.$": 1   
            })
            return my_doc
        except Exception:
            raise
    def user_collection_ref(self):
        return self.user_collection
    def article_collection_ref(self):
        return self.articles_collection