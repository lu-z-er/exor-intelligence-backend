from pydantic import BaseModel

class Proctor_Post_Data(BaseModel):
    claim: str


class Fetch_Article_Post_Data(BaseModel):
    url: str


class Sumzee_Post_Data(BaseModel):
    user_id: str
    article_id: str


