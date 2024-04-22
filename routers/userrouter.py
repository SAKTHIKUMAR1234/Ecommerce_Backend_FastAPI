from fastapi import APIRouter
from common import response,exceptions
from services.database import SessionLocal
from services.payment_services import client,get_random_id
from services.securityconfig import get_current_user
from models import CartModel,UsersModel,ProductsModel,ProductCartModel,OrdersModel,OrderItemModel,VendorModel,VendorStatus
from http import HTTPStatus
import traceback

user_router = APIRouter(prefix='/user')


def get_cart_product_price(cart_model:CartModel):
  cart_products_price = {
    'price' : 0.0,
    'product_list' : []
  }
  for products in cart_model.cart_product_list:
    cart_products_price['price'] += (products.product.product_price * products.quantity)
    product_details = {
      'product_name' : products.product.product_name,
      'product_count' : products.quantity,
      'product_price' : products.product.product_price,
      'products_images' : [
        {
          'image_url' : image.picture_url
        }
        for image in products.product.product_images
      ]
    }
    cart_products_price['product_list'].append(product_details)
  return cart_products_price

@user_router.get('')
def user_details():
  try:
    session = SessionLocal()
    session.begin()
    user = session.query(UsersModel).filter(UsersModel.email == get_current_user()['email']).first()
    vendor = session.query(VendorModel).filter(VendorModel.user == user,VendorModel.status == VendorStatus.accepted.value).first()
    is_vendor = False
    vendor_details = {}
    if vendor is not None:
      is_vendor = True
      vendor_details = {
        'vendor_address' : vendor.vendor_address,
        'vendor_name' : vendor.vendor_name
      }
    response_body = {
      'user_name' : user.first_name+" "+user.last_name,
      'email_id' : user.email,
      'phone_number' : user.phone_number,
      'is_dev' : user.isdev,
      'is_vendor' : is_vendor,
      'vendor_details' : vendor_details
    }
    session.commit()
    session.close()
    return response.response_sender(
      data=response_body,
      message="DETAILS FETCHED",
      http=HTTPStatus.OK
    )
    
  except Exception as e:
    traceback.print_exception(e)
    session.rollback()
    session.close()
    raise exceptions.CustomeException("OOP'S SOMETHNIG WENT WRONG")

@user_router.post('/add_to_cart')
def add_to_cart(product_id : int):
  try:
    session = SessionLocal()
    session.begin()
    email = get_current_user()['email']
    user : UsersModel = session.query(UsersModel).filter(UsersModel.email == email).first()
    cart : CartModel = user.user_cart
    product = session.query(ProductsModel).filter(ProductsModel.id == product_id).first()
    if product is None:
      session.close()
      return response.response_sender(data={'product_id':product_id},message='THE PRODUCT NOT FOUND',http=HTTPStatus.NOT_FOUND)
    if product.product_count == 0:
      session.close()
      return response.response_sender(data={'product_id':product_id},message='OUT OF STOCK',http=HTTPStatus.CONFLICT)
    product_cart_model = session.query(ProductCartModel).filter(ProductCartModel.cart == cart , ProductCartModel.product == product).first()
    if product_cart_model is None:
      product_cart_model = ProductCartModel()
      product_cart_model.product = product
      product_cart_model.cart = cart
      product.product_count = product.product_count -1
    else:
      product_cart_model.quantity = product_cart_model.quantity + 1
      product.product_count = product.product_count -1
    session.add(product_cart_model)
    session.add(product)
    session.commit()
    session.close()
    return response.response_sender(data=None,message='PRODUCT ADDED TO THE CART',http=HTTPStatus.OK)
  except Exception as e:
    session.rollback()
    session.close()
    raise exceptions.CustomeException("OOP'S SOMETHNIG WENT WRONG")
  
@user_router.put('/remove_from_cart')
def remove_from_cart(product_id : int):
  try:
    session = SessionLocal()
    session.begin()
    email = get_current_user()['email']
    user : UsersModel = session.query(UsersModel).filter(UsersModel.email == email).first()
    cart : CartModel = user.user_cart
    product = session.query(ProductsModel).filter(ProductsModel.id == product_id).first()
    if product is None:
      session.close()
      return response.response_sender(data={'product_id':product_id},message='THE PRODUCT NOT FOUND',http=HTTPStatus.NOT_FOUND)
    product_cart_model = session.query(ProductCartModel).filter(ProductCartModel.cart == cart , ProductCartModel.product == product).first()
    if product_cart_model is None:
      session.close()
      return response.response_sender(data={'product_id':product_id},message='THE PRODUCT NOT IN YOUR CART',http=HTTPStatus.NOT_FOUND)
    product.product_count += product_cart_model.quantity
    session.delete(product_cart_model)
    session.add(product)
    session.commit()
    session.close()
    return response.response_sender(data=None,message='PRODUCT REMOVED FROM THE CART',http=HTTPStatus.OK)
  except Exception as e:
    session.rollback()
    session.close()
    raise exceptions.CustomeException("OOP'S SOMETHNIG WENT WRONG")
  
@user_router.get('/cart/inc/dec')
def cart_product_increament_decreament(product_id : int ,option : str):
  
  try:
    session = SessionLocal()
    session.begin()
    if option not in ['inc','dec']:
      session.close()
      return response.response_sender(data=None,message='INVALID ACTION',http=HTTPStatus.BAD_REQUEST)
    user = session.query(UsersModel).filter(UsersModel.email == get_current_user()['email']).first()
    product = session.query(ProductsModel).filter(ProductsModel.id == product_id).first()
    cart : CartModel = user.user_cart
    product_cart_model = session.query(ProductCartModel).filter(ProductCartModel.cart == cart , ProductCartModel.product == product).first()
    if product_cart_model is None:
      session.close()
      return response.response_sender(data={'product_id':product_id},message='THE PRODUCT NOT FOUND',http=HTTPStatus.NOT_FOUND)
    if option == 'dec':
      product.product_count +=1
      if product_cart_model.quantity == 1:
        session.delete(product_cart_model)
        session.add(product)
      else:
        product_cart_model.quantity -=1
        session.add(product_cart_model)
        session.add(product)
    else : 
      if product.product_count == 0:
        session.close()
        return response.response_sender(data={'product_id':product_id},message='OUT OF STOCK',http=HTTPStatus.CONFLICT)
      product.product_count -=1
      product_cart_model.quantity +=1
      session.add(product)
      session.add(product_cart_model)
    session.commit()
    return response.response_sender(data=None,message='DONE',http=HTTPStatus.OK)
    
  except Exception as e:
    session.rollback()
    session.close()
    raise exceptions.CustomeException("OOP'S SOMETHNIG WENT WRONG")
  
  
@user_router.get('/cart')
def cart_details():
  try:
    session = SessionLocal()
    session.begin()
    user = session.query(UsersModel).filter(UsersModel.email == get_current_user()['email']).first()
    cart_model = session.query(CartModel).filter(CartModel.user == user).first()
    cart_products_price = get_cart_product_price(cart_model) 
    response_body = {
      'cart_id' : cart_model.id,
      'cart_products' : cart_products_price['product_list'],
      'total_price' : cart_products_price['price']
    }
    session.close()
    return response.response_sender(data=response_body,message='CART DATA FETCHED SUCCESSFULLY',http=HTTPStatus.OK)
  except Exception as e:
    session.rollback()
    session.close()
    raise exceptions.CustomeException("OOP'S SOMETHNIG WENT WRONG")

@user_router.post('/order')
def make_order():
  try:
    session = SessionLocal()
    session.begin()
    user = session.query(UsersModel).filter(UsersModel.email == get_current_user()['email']).first()
    cart : CartModel = user.user_cart
    cart_products : list[ProductCartModel] = cart.cart_product_list
    if len(cart_products) == 0:
      session.close()
      return response.response_sender(data=None,message='YOUR CART IS EMPTY',http=HTTPStatus.NOT_FOUND)
    total_cost = 0
    order_model = OrdersModel()
    order_model.user = user
    session.add(order_model)
    for product in cart_products:
      order_item_model = OrderItemModel()
      order_item_model.order = order_model
      order_item_model.quantity = product.quantity
      order_item_model.product = product.product
      session.add(order_item_model)
      total_cost += product.product.product_price
      session.delete(product)
    data = {
      'amount' : total_cost*100,
      'currency' : 'INR',
      'receipt' : get_random_id()
    }
    order = client.order.create(data = data)
    order_model.razor_pay_order_id = order['id']
    response_body = {
      "order_id":order['id'],
      "payment_details":data,
      "user_details":{
        "user_name" : user.first_name+" "+user.last_name,
        "user_email" : user.email,
        "phone_number" : user.phone_number
      }
    }
    session.add(order_model)
    # session.commit()
    session.close()
    return response.response_sender(data=response_body,message='ORDER_PLACED',http=HTTPStatus.OK)
  except Exception as e:
    traceback.print_exception(e)
    session.rollback()
    session.close()
    raise exceptions.CustomeException("OOP'S SOMETHNIG WENT WRONG")
  