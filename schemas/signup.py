from pydantic import BaseModel, validator
import re
from common.exceptions import InvalidDataException

class Signup(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number : str
    password: str

    @validator("first_name", "last_name")
    def validate_name(cls, v):
        pattern = r'^[A-Za-z]+(?: [A-Za-z]+)?$'
        if not re.match(pattern, v):
            raise InvalidDataException("Name must contain only alphabets and at most one space")
        return v.strip()

    @validator("email")
    def validate_email(cls, v):
        email_regex = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
        if not re.match(email_regex, v):
            raise InvalidDataException("Invalid email format")
        return v

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise InvalidDataException("Password must be at least 8 characters long")
        return v
    
    @validator('phone_number')
    def validate_phone_number(cls,v):
        phone_number_regex = r'^[0-9]'
        if not re.match(phone_number_regex,v) or len(v)!=10:
            raise InvalidDataException("Enter Valid Phone Number")
        return v
