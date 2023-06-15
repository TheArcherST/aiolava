from pydantic import BaseModel


class LavaType(BaseModel):
    class Config:
        allow_mutation = False
