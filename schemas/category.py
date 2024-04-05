from pydantic import BaseModel

class Category(BaseModel):
  
  category_name : str
  category_description : str