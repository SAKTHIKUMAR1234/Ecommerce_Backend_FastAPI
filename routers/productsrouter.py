from fastapi import APIRouter
from services.database import SessionLocal
from common.exceptions import CustomeException
from common import response
from models import CategoryModel, ProductsModel
from http import HTTPStatus

products_router = APIRouter(prefix='/products')


@products_router.get('/categories')
def get_all_categories():
  try:
    session = SessionLocal()
    session.begin()
    category_list = session.query(CategoryModel).all()
    response_body = [
      {
        'category_id' : category.id,
        'category_name' : category.category_name,
        'category_description' : category.category_description
      }
      for category in category_list
    ]
    return response.response_sender(data=response_body,message='CATEGORIES FETCHED SUCCESSFULLY',http=HTTPStatus.OK)
  except Exception as e:
    session.rollback()
    session.close()
    raise CustomeException("OOP'S SOMETHNIG WENT WRONG")
  
@products_router.get('')
def get_all_products():
  try:
    session = SessionLocal()
    session.begin()
    products_list = session.query(ProductsModel).all()
    respose_body = [
      {
        'product_id' : product.id,
        'product_name' : product.product_name,
        'product_category' : product.category.category_name,
        'product_prize' : product.product_price,
        'product_count' : product.product_count,
        
        'products_images' : [
          {
            'image_url' : image.picture_url
          }
          for image in product.product_images
        ]
      }
      for product in products_list
    ]
    session.commit()
    session.rollback()
    return response.response_sender(data=respose_body,message='PRODUCT\'S FETCHED SUCCESSFULLY',http=HTTPStatus.OK)
  except Exception as e:
    session.rollback()
    session.close()
    raise CustomeException("OOP'S SOMETHNIG WENT WRONG")
  
