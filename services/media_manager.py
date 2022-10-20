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
import face_recognition as recon
from datetime import datetime
# locals
from config import logging


_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + \
    "haarcascade_frontalface_default.xml")

train_encodings = None

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
            extract_media_path = self.gen_media_path()
            cv2.imwrite(extract_media_path, roi_color)
            logging.info(f"temp extract media written at {extract_media_path}")
        return extract_media_path

    def gen_media_path(self) -> str:
        return self.tmp_path + str(datetime.now()) + ".jpg"

    @staticmethod
    def tear_down_tmp_file(file_path: str) -> bool:
        try:
            os.remove(file_path)
        except OSError as err:
            logging.warn(err)
            return False
        else:
            return True

    def media_recon_percentage(self, media_bytes: bytes, target_media_bytes: bytes) -> float:
        _media_path = self.gen_media_path()
        _target_media_path = self.gen_media_path()

        with open(_media_path, "wb") as tmp:
            tmp.write(media_bytes)

        with open(_target_media_path, "wb") as tmp2:
            tmp2.write(target_media_bytes)

        _media_load = recon.load_image_file(_media_path)
        _media_encoding = recon.face_encodings(_media_load)[0]

        _target_load = recon.load_image_file(_target_media_path)
        _target_encoding = recon.face_encodings(_target_load)[0]

        distance = recon.face_distance([_media_encoding, *train_encodings], _target_encoding)

        recon_match_percentage = 0
        for i, dist in enumerate(distance):
            if dist < 0.15:
                recon_match_percentage = (1 - dist) * 100

        # teardown tmp files
        self.tear_down_tmp_file(_media_path)
        self.tear_down_tmp_file(_target_media_path)

        return round(recon_match_percentage, 2)

    @staticmethod
    def load_train_encodings() -> list:
        logging.info("loading face recognition training samples")
        encodings = []
        for path in os.listdir("train"):
            _load = recon.load_image_file("train/" + path)
            _encoding = recon.face_encodings(_load)
            if len(_encoding) > 0:
                encodings.append(_encoding[0])
        logging.info("finished loading face recognition training samples")
        return encodings


train_encodings = MediaManager.load_train_encodings()