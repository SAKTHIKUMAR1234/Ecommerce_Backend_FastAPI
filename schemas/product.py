from pydantic import BaseModel
from typing import Annotated, List
from fastapi import UploadFile,File,Form


class ProductCreateSchema(BaseModel):
  
  product_name : str
  product_price : str
  count : str
  category_id : str
  # images : UploadFile = Form(...)