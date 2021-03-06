import unittest
import json
from api import app
from api.v1 import requests
from api.v1.rides.model import rides
from .notification_tests import create_sample_notification


def create_sample_ride_request(request_id, user_id, ride_id):
    ride_request = {
        "id": request_id,
        "user_id": user_id,
        "ride_id": ride_id,
        "status": "pending"
    }
    return ride_request


class RequestTestCases(unittest.TestCase):
    json_headers = {'Content-Type': 'application/json'}
    sample_ride_request = create_sample_ride_request(1, 1, 1)

    def setUp(self):

        self.test_client = app.test_client()

    def test_create_ride_request(self):
        data = json.dumps({"status": "pending"})
        response = self.test_client.post('/api/v1/requests/request_ride/1/1', data=data, headers=self.json_headers)
        self.assertEqual(response.status_code, 200)

    def test_get_ride_requests(self):
        response = self.test_client.get('/api/v1/ride_requests/requests/1')
        results = json.loads(response.data.decode())
        if rides:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(results, {"ride_requests": [self.sample_ride_request]})

    def test_approve_ride__request(self):
        data = json.dumps({"request_id": "1", "user_id": 1, "approval": "yes"})
        response = self.test_client.post('/api/v1/requests/approve/1/1', data=data, headers=self.json_headers)
        if type(response.data.decode()) == str:
            print(response.data.decode())
            self.assertEqual(response.status_code, 400)
        else:
            results = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(results, {
                "notification": create_sample_notification(1, 1, "Your request has been rejected"),
                "ride_request": {"id": 1, "ride_id": 1, "status": "no", "user_id": 1}})

    def test_l_delete_request(self):
        response = self.test_client.delete('/api/v1/rides/ride_requests/delete/1')
        results = json.loads(response.data.decode())
        if requests:
            self.assertEqual(results,{'remaining_requests': {'error': 'Request not Found'}})
        self.assertEqual(response.status_code, 200)

