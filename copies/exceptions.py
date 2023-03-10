from rest_framework.exceptions import APIException


class CustomDoesNotExists(APIException):
    status_code = 404
    default_detail = "not found"

    def __init__(self, detail=None, code=None):
        super().__init__(detail, code)
