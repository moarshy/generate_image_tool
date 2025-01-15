from pydantic import BaseModel
from typing import Optional

class InputSchema(BaseModel):
    tool_name: str
    tool_input_data: str
    input_dir: Optional[str] = None