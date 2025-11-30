import logging
from fastapi import FastAPI
import pymongo
from dotenv import load_dotenv
import os
from bson.objectid import ObjectId
from pydantic import BaseModel
from operators.secptor import MotherShip, Kepler

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


_ = load_dotenv()


class Claim(BaseModel):
    claim: str


database_url = os.getenv("MONGODB_URI")

app = FastAPI()

myclient = pymongo.MongoClient(database_url)
mydb = myclient["test"]["articles"]

ship = MotherShip()
kepler = Kepler()


def query(id_db):
    try:
        myquery = {"_id": ObjectId(id_db)}
        mydoc = mydb.find_one(myquery)
        return mydoc
    except:
        raise


@app.get("/sumzee")
def sum_api(opid):
    try:
        db_article: dict | None = query(opid)
        if db_article:
            summary = ship.summarize(db_article["description"])
            return {
                "summary": summary[0]["summary_text"],
            }

    except Exception:
        raise


@app.post("/proctor")
def proc_api(data: Claim):
    try:
        kepler.primodius(ship.kepler_belt)
        result = kepler.overlord(data.claim)
        return result
    except Exception:
        raise

