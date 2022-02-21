"""User view tests"""

# run tests in terminal:
#   python -m unittest tests/test_external_API_requests.py

import os
import requests
from unittest import TestCase

from models import db, Category

os.environ['DATABASE_URL'] = "postgresql:///WODatHome_test_db"

from app import app

from secret import API_SECRET_KEY

db.create_all()

API_BASE_URL = 'https://wger.de/api/v2/'

headers = {
    "Authorization": f"Token {API_SECRET_KEY}",
    "Accept": "application/json; indent=4"}


class APIRequestTestCase(TestCase):
    """Test External API Requests"""
    def setUp(self):
        db.drop_all()
        db.create_all()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_request_categories(self):
        """Can we get categories from WGER API?"""
        response = requests.get(
            f"{API_BASE_URL}exercisecategory?limit=1", headers=headers)
        res_json = response.json()
        results = res_json['results']

        self.assertIsNotNone(results)
        self.assertEqual(results[0]['name'], "Abs")

    def test_request_exercises(self):
        """Can we get exercises from WGER API?"""
        response = requests.get(
            f"{API_BASE_URL}exercise?limit=1", headers=headers)
        res_json = response.json()
        results = res_json['results']

        self.assertIsNotNone(results)
        self.assertEqual(results[0]['id'], 345)

    def test_request_equipment(self):
        """Can we get equipment from WGER API?"""
        response = requests.get(
            f"{API_BASE_URL}equipment?limit=1", headers=headers)
        res_json = response.json()
        results = res_json['results']

        self.assertIsNotNone(results)
        self.assertEqual(results[0]['name'], "Barbell")

    def test_request_exercise_image(self):
        """Can we get exercise images from WGER API?"""
        response = requests.get(
            f"{API_BASE_URL}exerciseimage?limit=1", headers=headers)
        res_json = response.json()
        results = res_json['results']

        self.assertIsNotNone(results)
        self.assertEqual(results[0]['id'], 3)

    def test_adding_to_db(self):
        """Can we take use API data to fill our database?"""
        response = requests.get(
            f"{API_BASE_URL}exercisecategory?limit=1", headers=headers)
        res_json = response.json()
        results = res_json['results']

        new_category = Category(id=results[0]['id'], name=results[0]['name'])
        db.session.add(new_category)
        db.session.commit()

        self.assertEqual(Category.query.get(10).name, "Abs")
