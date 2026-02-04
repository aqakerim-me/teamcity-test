from pydantic import BaseModel as BM
from pydantic import ConfigDict


class BaseModel(BM):
    model_config = ConfigDict(validate_assignment=True)
