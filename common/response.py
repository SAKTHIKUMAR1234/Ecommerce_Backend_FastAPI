from fastapi import Response
from http import HTTPStatus
import json

def response_sender(data: any, message: str, http: HTTPStatus) -> Response:
    response_body = {
        'http_status': http.phrase,
        'message': message,
        'data': data
    }
    return Response(content=json.dumps(response_body), status_code=http.value, media_type='application/json')