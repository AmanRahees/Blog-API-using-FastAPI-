from pydantic import *

class Blog(BaseModel):
    title: str
    body: str