from typing import Optional

from pydantic import BaseModel


class NewPlayer(BaseModel):
    api: Optional[str] = None
