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
from flask import Blueprint, request, jsonify, abort, make_response
# locals
from config import logging
from services.identity_media import IdentityMediaService
from util.response import SuccessRes, ErrorRes


resource = Blueprint("identity", __name__)
idm_service = IdentityMediaService()


@resource.route("<string:uuid>", methods=["POST"])
def post_verify_identity(uuid: str):
    media_content = request.files.get("content")
    res = None
    error = None

    try:
        result = idm_service.get_identity_match(
            media_uuid=uuid,
            file=media_content)
        print(result)

        if not result:
            raise Exception("Coudln't proceed with identity match checks")
        res = SuccessRes(status_code=200, data=result)
    except:
        logging.warn("unexpected error", exc_info=True)
        error = ErrorRes(status_code=500)
    finally:
        return error and error.json or res.json
