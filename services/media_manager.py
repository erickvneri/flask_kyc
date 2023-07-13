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
import face_recognition as fr
from datetime import datetime

# locals
from config import logging


_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


class MediaManager:
    def gen_media_face_extract(self, media_bytes: bytes) -> (bytes, int):
        """
        Implements OpenCV to extract a face
        from a an image bytes provided.

        It will fail in case of finding less or
        greater than 1 faces in the byte array.

        Param ref: https://stackoverflow.com/questions/20801015/recommended-values-for-opencv-detectmultiscale-parameters

        ::param media_bytes bytes
        """
        media_path = self.gen_media_path()

        assert self.write_tmp_file(media_path, media_bytes)

        _media = cv2.imread(media_path)
        _gray_scaled = cv2.cvtColor(_media, cv2.COLOR_BGR2GRAY)
        _extract = _cascade.detectMultiScale(
            _gray_scaled, scaleFactor=1.05, minNeighbors=6, minSize=(40, 40)
        )

        # if len(_extract) != 1:
        # logging.warn("failed to collect face extract from media bytes")
        # return None, None

        extract_path = self.process_media_extract(_media, _extract)

        with open(extract_path, "rb") as media_extract:
            _content = media_extract.read()

        self.teardown_tmp_file(media_path)
        self.teardown_tmp_file(extract_path)
        return _content, len(_content)

    def process_media_extract(self, media: list, extract: list) -> str:
        """
        Implements OpenCV to recollect
        an encoding extract of a ful
        processed media and saves its
        output into a temporary filesystem.

        ::param media   list
        ::param extract list
        """
        extract_media_path = None
        for x, y, w, h in extract:
            cv2.rectangle(media, (x, y), (x + w, y + h), (0, 0, 0), 0)
            roi_color = media[y : y + h, x : x + w]
            extract_media_path = self.gen_media_path()
            cv2.imwrite(extract_media_path, roi_color)
            logging.info(f"temp extract media written at {extract_media_path}")
        return extract_media_path

    def media_recon_percentage(
        self, media_bytes: bytes, target_media_bytes: bytes
    ) -> float:
        """
        It takes two byte parameters to build
        two temp images for further analysis.

        First, it converts them into face-recognition
        compatible encodings, then compares them and
        gets a match percentage.

        Finally, it tears down the temp image files
        from the file system

        ::param media_bytes        bytes
        ::param target_media_bytes bytes
        """
        _media_path = self.gen_media_path()
        _target_media_path = self.gen_media_path()

        # Build up tmp files
        assert self.write_tmp_file(_media_path, media_bytes)
        assert self.write_tmp_file(_target_media_path, target_media_bytes)

        # Gen encodings
        media_encoding = self.gen_image_encodings(_media_path)
        target_encoding = self.gen_image_encodings(_target_media_path)

        # Track match percentage
        match_percentage = self.get_media_match_percentage(
            media_encoding, target_encoding
        )

        # Teardown tmp files
        assert self.teardown_tmp_file(_media_path)
        assert self.teardown_tmp_file(_target_media_path)
        return match_percentage

    @staticmethod
    def gen_media_path() -> str:
        """
        Generates a string path pointing
        to a temp folder.
        """
        tmp_path = "services/tmp/"
        return tmp_path + str(datetime.now()) + ".jpg"

    @staticmethod
    def teardown_tmp_file(file_path: str) -> bool:
        """
        Removes a file from the file
        system according to the provided
        path.

        ::param file_path str
        """
        os.remove(file_path)
        return True

    @staticmethod
    def write_tmp_file(path: str, content: bytes) -> bool:
        """
        Writes a binary file into the filesystem
        according to the path provided and
        its content.

        ::param path    str
        ::param content bytes
        """
        with open(path, "wb") as tmp:
            tmp.write(content)
        return True

    @staticmethod
    def gen_image_encodings(path: str) -> list:
        """
        Takes a path to generate the
        face_recognition-compatible
        encodings.

        ::param path str
        """
        load = fr.load_image_file(path)
        encodings = fr.face_encodings(load)[0]
        return encodings

    @staticmethod
    def get_media_match_percentage(
        base_encoding: list, target_encoding: list, decimals: int = 2
    ):
        """
        Implements face_recognition library
        and process the encodings provided
        to collect the distance of match
        and returns a match percentace.

        ::param base_encoding   list
        ::param target_encoding list
        ::param decimals        int
        """
        distance = fr.face_distance([base_encoding], target_encoding)

        percent = [(1 - dist) * 100 for dist in distance]
        return round(percent[0], decimals)
