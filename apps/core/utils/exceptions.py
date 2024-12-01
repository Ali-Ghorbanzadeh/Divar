from rest_framework.exceptions import APIException


class CustomAPIException(APIException):
    def __init__(self, message=None, status_code=400):
        if message is None:
            message = 'ارور ناشناخته!'
        super().__init__(message)
        self.status_code = status_code
