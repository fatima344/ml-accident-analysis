import unittest
import json
from app import app
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")


class AccidentPredictionTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_home_page_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Accident Survival Prediction', response.data)

    def test_prediction_logic(self):
        # Test with valid data
        data = {
            "age": "30",
            "gender": "Male",
            "speed": "60",
            "helmet": "Yes",
            "seatbelt": "No"
        }

        response = self.client.post("/", data=data)
        self.assertEqual(response.status_code, 200)

        # Check prediction is either "Survived" or "Did not survive"
        self.assertTrue(
            b'Survived' in response.data or b'Did not survive' in response.data,
            "Prediction output not found!"
        )

    def test_invalid_data_handling(self):
        # Missing fields
        data = {
            "age": "30",
            "gender": "Male",
            "helmet": "Yes",
            "seatbelt": "No"
            # Missing 'speed'
        }

        response = self.client.post("/", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Error', response.data)  # Error message should be shown

if __name__ == '__main__':
    unittest.main()
