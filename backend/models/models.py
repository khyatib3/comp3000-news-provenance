from pydantic import BaseModel, Field
from typing import Optional
import uuid

class Article(BaseModel):
    id: int
    title: str
    publish_date: str
    author: str
    platform: str
    