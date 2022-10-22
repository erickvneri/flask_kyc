# MIT License
#
# Copyright (c) 2022 erickvneri
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
from flask import jsonify


class BaseResponse:
    """
    BaseResponse supporting only
    the status code and data references

    ::param status_code int
    ::param **data      dict
    """
    def __init__(self, status_code: int, data: dict) -> "BaseResponse":
        self.status_code = status_code
        self.data = data


class ErrorRes(BaseResponse):
    """
    Implements BaseResponse and sets
    status code 400 and status "ERROR"
    by default

    ::param status_code int
    ::param **data      dict
    """
    def __init__(self, *, status_code: int = 400, data: dict = {}) -> "ErrorRes":
        BaseResponse.__init__(self, status_code, data)
        self.data["status"] = "ERROR"
        self.json = jsonify(self.data)
        self.json.status_code = self.status_code


class SuccessRes(BaseResponse):
    """
    Implements BaseResponse and sets
    status code 200 and status "SUCCESS"
    by default

    ::param status_code int
    ::param **data      dict
    """
    def __init__(self, *, status_code: int = 200, data: dict = {}) -> "SuccessRes":
        BaseResponse.__init__(self, status_code, data)
        data["status"] = "SUCCESS"
        self.json = jsonify(self.data)
        self.json.status_code = self.status_code