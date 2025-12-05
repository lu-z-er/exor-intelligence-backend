import logging
from os import getenv

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from operators.db_ops import MongoStorage
from operators.exor_errors import FetchArticleError, MongoDBError, QdrantDBError
from operators.exor_types import Fetch_Article_Post_Data, Proctor_Post_Data, Sumzee_Post_Data
from operators.secptor import Kepler, MotherShip
from operators.utils import taskmaster

logger_r = logging.getLogger()
logger_r.setLevel(logging.INFO)



var_loaded = load_dotenv()


app = FastAPI()

try:
    if not var_loaded:
        raise RuntimeError("Env Failed to Load!!")
    database = MongoStorage(url=getenv("MONGODB_URI"))
    kepler = Kepler()
    ship = MotherShip()
    logger_r.info("Connected to the DataBases Successfully")
except QdrantDBError as e:
    raise SystemError(
        "BootStraping Error: Something went wrong with QdrantDB.") from e
except MongoDBError as e:
    raise SystemError(
        "BootStraping Error: Something went wrong with MongoDB") from e
except Exception:
    raise SystemError("Error While BootStraping!!!")


@app.get("/sumzee")
def sum_api(article_id):
    try:
        db_article: dict | None = database.query_articles(article_id)
        if not db_article:
            raise HTTPException(status_code=404, detail="Article not found")
        summary = ship.summarize(db_article["description"])
        return {
            "summary": summary[0]["summary_text"],
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error :(")


@app.post("/sumzee")
def sum_u_api(data: Sumzee_Post_Data):
    try:
        db_article = database.query_user_articles(
            data.user_id, data.article_id)
        if not db_article:
            raise HTTPException(
                status_code=404, detail="Article or User not found")
        db_article = db_article["uploadedArticles"][0]
        summary = ship.summarize(db_article["description"])
        return {
            "summary": summary[0]["summary_text"],
        }
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error :(")


@app.post("/proctor")
def proc_api(data: Proctor_Post_Data):
    try:
        kepler.primodius(ship.kepler_belt)
        result = kepler.overlord(data.claim)
        return result
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error :(")


@app.post("/fetch-article")
def fa_api(data: Fetch_Article_Post_Data):
    try:
        mydb_u = database.user_collection_ref()
        result = taskmaster(data.url, ship.classify, mydb_u.insert_one)
        return result
    except HTTPException:
        raise
    except FetchArticleError:
        raise HTTPException(
            status_code=501,
            detail="Unable to Fetch the Aritle. Site might not be Supported by Us!!",
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error :(")
