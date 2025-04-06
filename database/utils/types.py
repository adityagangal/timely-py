from typing import TypeVar
from beanie import Document
from pydantic import BaseModel

T = TypeVar("T", bound=Document)
P = TypeVar("P", bound=BaseModel)
