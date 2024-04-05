from fastapi import Request
from http import HTTPStatus
from common.response import response_sender
from common.exceptions import CustomeException,InvalidDataException

async def handle_500(request : Request,exc : CustomeException):
  return response_sender(data=None,message=str(exc),http=HTTPStatus.INTERNAL_SERVER_ERROR)


async def handle_validation_error(request:Request, exc : InvalidDataException):
  return response_sender(data=exc.__dict__,message = str(exc),http=HTTPStatus.BAD_REQUEST)