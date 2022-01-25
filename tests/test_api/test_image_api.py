# -*- coding: utf-8 -*-
import unittest
from unittest.mock import patch
from os import path
import pathlib

from tests.test_api import TestApi


class TestImageApi(TestApi):
    @patch("manager.clients.image.ImageClient.get_image")
    @patch("manager.clients.ocr.OCRClient.get_content")
    def test_image_url_ocr(self, mock_get_content, mock_get_image):
        content = ['愚园路', '西', '东', '315', '309', 'Yuyuan Rd.', 'W', 'E']
        mock_get_content.return_value = content
        mock_get_image.return_value = bytes()
        res = self.client.post(
            f"/api/v1/image/ocr",
            json={
                "url": "https://github.com/JaidedAI/EasyOCR/blob/master/examples/chinese.jpg",
                
            },
        )
        self.assertEqual(res.status_code, 200)
        data = res.json
        self.assertEqual(data["status"], "success")
        image = data["image"]
        self.assertEqual(image["content"], content)

        res = self.client.post(
            f"/api/v1/image/ocr",
            json={
                "url1": "https://github.com/JaidedAI/EasyOCR/blob/master/examples/chinese.jpg",
                
            },
        )
        self.assertEqual(res.status_code, 400)

    @patch("manager.clients.ocr.OCRClient.get_content")
    def test_image_url_ocr_file(self, mock_get_content):
        content = ['愚园路', '西', '东', '315', '309', 'Yuyuan Rd.', 'W', 'E']
        mock_get_content.return_value = content

        image_path = pathlib.Path(path.dirname(__file__)) / "example2.png"
        with open(image_path , "rb") as f:
            res = self.client.post(
                f"/api/v1/image/ocr/file",
                content_type="multipart/form-data",
                data={"file": (f, str(image_path).split("/")[-1])}
            )
            self.assertEqual(res.status_code, 200)
            data = res.json
            self.assertEqual(data["status"], "success")
            image = data["image"]
            self.assertEqual(image["content"], content)


if __name__ == "__main__":
    unittest.main()