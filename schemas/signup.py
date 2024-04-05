from pydantic import BaseModel, validator
import re
from common.exceptions import InvalidDataException

class Signup(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

    @validator("first_name", "last_name")
    def validate_name(cls, v):
        if not v.strip().isalpha():
            raise InvalidDataException("Name must contain only alphabets and spaces")
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
