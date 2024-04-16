from http import HTTPStatus
from fastapi import APIRouter, Form, UploadFile
from services.database import SessionLocal
from common.exceptions import CustomeException
from common import response
from services.securityconfig import get_current_user
from services.database import SessionLocal
from models import UsersModel,VendorModel, CategoryModel, ProductsModel, PictureModel
from models.VendorModel import VendorStatus
from schemas.vendorrequest import VendorRequest
from schemas.vendorrequestdecision import VendorRequestDecision
from schemas.category import Category
import traceback 
from typing import List
from services.firebaseconfig import get_storage_bucket
from services.time_services import get_current_milli_seconds


vendorrouter = APIRouter(prefix='/vendor')

@vendorrouter.get('/request')
def request_for_vendor(vendorrequest : VendorRequest):
  
  try:
    current = get_current_user()
    session = SessionLocal()
    session.begin()
    user = session.query(UsersModel).filter(UsersModel.email == current['email']).first()
    if user is None:
      response_body = {'email':current['email']}
      session.close()
      return response.response_sender(data=response_body,message='NOT FOUND',http=HTTPStatus.NOT_FOUND)
    vendor_model = session.query(VendorModel).filter(VendorModel.user == user).first()
    if vendor_model is not None and vendor_model.status == VendorStatus.accepted.value:
      session.close()
      return response.response_sender(data=None,message='YOU ARE ALREADY AN VENDOR',http=HTTPStatus.CONFLICT)
    else :
      
      if vendor_model is None:
        vendor_model = VendorModel()
        exist_name_vendor = session.query(VendorModel).filter(VendorModel.vendor_name == vendorrequest.name).first()
        if exist_name_vendor is not None:
          return response.response_sender(data=None,message='THE VENDOR NAME ALREADY TAKEN',http=HTTPStatus.CONFLICT)
      vendor_model.status = VendorStatus.pending.value
      vendor_model.user = user
      vendor_model.vendor_address = vendorrequest.address
      vendor_model.vendor_name = vendorrequest.name
      session.add(vendor_model)
      session.commit()
      session.close()
      return response.response_sender(data=None,message='REQUESTED WAIT FOR THE ADMIN APPROVAL',http=HTTPStatus.OK)
    
  except Exception as e:
    traceback.print_exception(e)
    session.rollback()
    session.close()
    raise CustomeException("OOP'S SOMETHNIG WENT WRONG")
  
@vendorrouter.get('/admin/requests')
def get_pending_request():
  try:
    session = SessionLocal()
    session.begin()
    vedor_requests = session.query(VendorModel).filter(VendorModel.status == VendorStatus.pending.value).all()
    response_body = [
      {
          'vendor_request_id' : vendor.id,
          'vendor_name' : vendor.vendor_name,
          'vendor_address' : vendor.vendor_address,
          'vendor_email' : vendor.user.email
      }
      for vendor in vedor_requests
    ]
    session.close()
    return response.response_sender(data=response_body,message='VENDOR REQUESTS FETCHED',http=HTTPStatus.OK)
    
  except Exception as e:
    traceback.print_exception(e)
    session.rollback()
    session.close()
    raise CustomeException("OOP'S SOMETHNIG WENT WRONG")
  
@vendorrouter.put('/admin/request/decision')
def make_decision(decision : VendorRequestDecision):
  
  try:
    session = SessionLocal()
    vendor_request = session.query(VendorModel).filter(VendorModel.id == decision.request_id).first()
    if vendor_request is None:
      session.close()
      return response.response_sender(data={'request_id':decision.request_id},message='THE REQUEST ID NOT FOUND',http=HTTPStatus.NOT_FOUND)
    if decision.decision == 'ACCEPT':
      vendor_request.status = VendorStatus.accepted.value
    else : 
      vendor_request.status = VendorStatus.rejected.value
    session.add(vendor_request)
    session.commit()
    session.close()
    return response.response_sender(data=None,message='STATUS UPDATED',http=HTTPStatus.OK)
  except Exception as e:
    traceback.print_exception(e)
    session.rollback()
    session.close()
    raise CustomeException("OOP'S SOMETHNIG WENT WRONG")
  
  
@vendorrouter.post('/category/create')
def create_category(category : Category):
  
  try:
    session = SessionLocal()
    session.begin()
    category_model = session.query(CategoryModel).filter(CategoryModel.category_name == category.category_name).first()
    if category_model is not None:
      session.close()
      return response.response_sender(data={'category_name':category.category_name},message='CATEGORY NAME ALREADY EXIST',http=HTTPStatus.CONFLICT)
    category_model = CategoryModel()
    category_model.category_name = category.category_name
    category_model.category_description = category.category_description
    session.add(category_model)
    session.commit()
    session.close()
    return response.response_sender(data=None,message='CATEGORY CREATED',http=HTTPStatus.CREATED)
  except Exception as e:
    traceback.print_exception(e)
    session.rollback()
    session.close()
    raise CustomeException("OOP'S SOMETHNIG WENT WRONG")
  
@vendorrouter.post('/products/add')
def create_products(product_name : str = Form(...), product_price :str = Form(...), count : str = Form(...), category_id : str = Form(...), images : List[UploadFile] = Form(...)):
  try:  
    session = SessionLocal()
    session.begin()
    exist_product = session.query(ProductsModel).filter(ProductsModel.product_name == product_name).first()
    if exist_product is not None:
      session.close()
      return response.response_sender(data={'product_name':product_name},message='PRODUCT NAME ALREADY EXIST',http=HTTPStatus.CONFLICT)
    category = session.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if category is None:
      session.close()
      return response.response_sender(data={'category_id':category_id},message="CATEGORY DOES NOT EXIST",http=HTTPStatus.NOT_FOUND)
    product_model = ProductsModel()
    product_model.product_name = product_name
    product_model.product_count = count
    product_model.product_price = product_price 
    product_model.category = category
    user = session.query(UsersModel).filter(UsersModel.email == get_current_user()['email']).first()
    vendor = session.query(VendorModel).filter(VendorModel.user == user , VendorModel.status == 0).first()
    if vendor is None:
      session.close()
      return response.response_sender(data=None,message="VENDOR IS NOT REGISTERED",http=HTTPStatus.FORBIDDEN)
    product_model.vendor = vendor
    session.add(product_model)
    bucket = get_storage_bucket()
    for image in images:
      picture_model = PictureModel()
      picture_model.picture_original_name = image.filename
      blob = bucket.blob('images/'+get_current_milli_seconds()+image.filename)
      blob.upload_from_file(image.file)
      blob.make_public()
      picture_model.picture_url = blob.public_url
      picture_model.product = product_model
      session.add(picture_model)
    session.commit()
    session.close()
    return response.response_sender(data=None,message='PRODUCT ADDED SUCCESSFULLY',http=HTTPStatus.CREATED)
  except Exception as e:
    traceback.print_exception(e)
    session.rollback()
    session.close()
    raise CustomeException("OOP'S SOMETHNIG WENT WRONG")
