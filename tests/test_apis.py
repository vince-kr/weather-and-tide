import apis
import unittest

class TestApiResponseFormatter(unittest.TestCase):
    def test_sanity(self):
        self.assertTrue(True)

    def test_givenTideResponseAsDict_returnOnlyUsefulDataAsIterableOfDict(self):
        with open('cached_api_responses/tide.json', 'rb') as tf:
            mock_response = tf.read()
        expected = [
            {
                "height": -0.9988243040347612,
                "time": "2024-09-26T18:31:00+00:00",
                "type": "low"
            },
            {
                "height": 0.7589072356111228,
                "time": "2024-09-27T00:49:00+00:00",
                "type": "high"
            },
            {
                "height": -0.7107499006668393,
                "time": "2024-09-27T07:07:00+00:00",
                "type": "low"
            }
        ]
        actual = apis._pertinent_content(mock_response)
        self.assertEqual(expected, actual)
