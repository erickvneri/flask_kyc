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


resource = Blueprint("identity_media", __name__)
idm_service = IdentityMediaService()


@resource.route("", methods=["POST"])
def post_create_identity_media():
    media_content = request.files.get("content")
    res = None
    error = None

    try:
        result = idm_service.create_media(file=media_content)

        if not result:
            raise Exception()
        res = SuccessRes(status_code=201, data=result)
    except:
        logging.warn("failed to create identity media", exc_info=True)
        error = ErrorRes(status_code=500)
    finally:
        return error and error.json or res.json


@resource.route("<string:uuid>", methods=["GET"])
def get_identity_media(uuid: str):
    res = None
    error = None

    try:
        result = idm_service.get_media(uuid=uuid)
        if not result: raise Exception()

        res = make_response(result["content_extract"].tobytes())
        res.headers.set("Content-Type", "image/jpeg")
        res.headers.set(
            "Content-Disposition",
            "attachment",
            filename=result["name"])
    except:
        logging.warn(exc_info=True)
        error = ErrorRes(status_code=500)
    finally:
        return error and error.json or res

@resource.route("<string:uuid>", methods=["DELETE"])
def delete_identity_media(uuid: str):
    res = None
    error = None

    try:
        result = idm_service.delete_media(uuid=uuid)
        if not result: raise Exception("failed to delete media")
        res = make_response("No Content")
        res.status_code = 204
    except:
        logging.warn(exc_info=True)
        error = abort(jsonify(status="ERROR", error=["failed to save media"]), status_code=500)
    finally:
        if error: return error
        return res
