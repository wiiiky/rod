# encoding=utf-8


class HttpExecption(Exception):
    """HTTP 错误"""

    def __init__(self, status_code, message=''):
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return self.message
