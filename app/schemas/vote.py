from pydantic import BaseModel

class VotePayload(BaseModel):
    post_id: int