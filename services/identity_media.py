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
from config import logging
# locals
from services.media_manager import MediaManager
from daos.identity_media import (
    create_identity_media,
    get_identity_media)


media_manager = MediaManager()


class IdentityMediaService:

    def save_media(self, *, file: object):
        logging.info("processing new identity media record")
        content = file.read()
        length = len(content)

        # generate face extract
        extract, extract_length = media_manager.gen_media_face_extract(content)

        result = create_identity_media(
            file.filename,
            content,
            length,
            file.content_type,
            extract,
            extract_length)

        if not result:
            loggging.warn("failed to process and save identity media")
            return None

        logging.info("identity media has been saved properly")
        uuid, created_at, name, length, extract_length = result

        return dict(
            uuid=uuid,
            created_at=str(created_at),
            filename=name,
            length=length,
            extract_length=extract_length)

    def get_media(self, *, uuid: str):
        logging.info(f"loading identity media {uuid}")

        result = get_identity_media(uuid)

        if not result:
            logging.warn(f"failed to load identity media {uuid}")
        name, \
        content, \
        length, \
        created_at, \
        content_extract, \
        extract_length, \
        updated_at = result

        return dict(
            name=name,
            content=content,
            length=length,
            created_at=created_at,
            content_extract=content_extract,
            extract_length=extract_length,
            updated_at=updated_at)
