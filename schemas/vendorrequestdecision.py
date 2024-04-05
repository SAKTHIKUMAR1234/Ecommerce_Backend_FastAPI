from pydantic import BaseModel, validator
from common.exceptions import InvalidDataException

class VendorRequestDecision(BaseModel):
  
  decision : str
  request_id : int
  
  @validator('decision')
  def validate_decision(cls, v):
    if v not in ['ACCEPT','REJECT']:
      raise InvalidDataException('Invalid Decision Statement')
    return v