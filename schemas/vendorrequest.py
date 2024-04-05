
from pydantic import BaseModel
from common.exceptions import InvalidDataException

class VendorRequest(BaseModel):
    name: str
    address: str