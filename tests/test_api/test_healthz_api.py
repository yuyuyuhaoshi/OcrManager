import unittest
from unittest.mock import patch


from tests.test_api import TestApi

class TestHealthz(TestApi):
    def test_healthz(self):
        res = self.client.get(
            f"/api/healthz",
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 200)



if __name__ == "__main__":
    unittest.main()
