from pydantic import BaseModel
from typing import Optional # For optional fields

class Breed(BaseModel):
    name: str
    country: str
    size: str
    life_expectancy: int
    