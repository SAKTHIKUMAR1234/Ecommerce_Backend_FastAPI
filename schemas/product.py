from pydantic import BaseModel, validator

class Products(BaseModel):
   
   product_name : str
   product_price : float

class ProductList(BaseModel):
  
  products_list : list[Products]