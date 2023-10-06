from pydantic import BaseModel

class GenericModel(BaseModel):
    class Config:
        extra = 'allow'
