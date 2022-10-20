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
import cv2
import os
from datetime import datetime
# locals
from config import logging


_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + \
    "haarcascade_frontalface_default.xml")


class MediaManager:
    tmp_path = "services/tmp/"

    def gen_media_face_extract(self, media_bytes: bytes) -> tuple:
        media_path = self.gen_media_path()

        with open(media_path, "wb") as tmp:
            tmp.write(media_bytes)

        _media = cv2.imread(media_path)
        _gray_scaled = cv2.cvtColor(_media, cv2.COLOR_BGR2GRAY)
        _extract = _cascade.detectMultiScale(
            _gray_scaled,
            scaleFactor=1.2,
            minNeighbors=3,
            minSize=(30, 30))
        logging.info(f"faces found in extract {len(_extract)}")

        if len(_extract) > 1: return None, None
        extract_path = self.process_media_extract(_media, _extract)

        with open(extract_path, "rb") as media_extract:
            _content = media_extract.read()

        self.tear_down_tmp_file(media_path)
        self.tear_down_tmp_file(extract_path)
        return _content, len(_content)

    def process_media_extract(self, media: list, extract: list) -> str:
        extract_media_path = None
        for (x,y,w,h) in extract:
            cv2.rectangle(media, (x,y), (x+w, y+h), (0,0,0), 0)
            roi_color = media[y:y + h, x:x + w]
            extract_media_path = self.gen_media_path() + ".jpg"
            cv2.imwrite(extract_media_path, roi_color)
            logging.info(f"temp extract media written at {extract_media_path}")
        return extract_media_path

    def gen_media_path(self) -> str:
        return self.tmp_path + str(datetime.now())

    @staticmethod
    def tear_down_tmp_file(file_path: str) -> bool:
        try:
            os.remove(file_path)
        except OSError as err:
            logging.warn(err)
            return False
        else:
            return True
