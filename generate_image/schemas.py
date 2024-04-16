from typing import Optional
from pydantic import BaseModel


class InputSchema(BaseModel):
    prompt: str
    output_path: Optional[str] = None
