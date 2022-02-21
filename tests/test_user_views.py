"""User view tests"""

# run tests in terminal:
#   python -m unittest tests/test_user_views.py

import os
from unittest import TestCase

from models import db, User

os.environ['DATABASE_URL'] = "postgresql:///WODatHome_test_db"

from app import app

from secret import API_SECRET_KEY

db.create_all()

# Don't have WTForms use CSRF to validate, as I don't know how to test this. 
app.config['WTF_CSRF_ENABLED'] = False

class UserViewsTestCase(TestCase):
    """Test User Views of Different Pages"""

    def setUp(self):
        """Create test user,
        fill test_db with enough data from WGER API to create a workout,
        create a workout with exercises"""
        db.drop_all()
        db.create_all()

        u1 = User.register("test1", "password")
        u1id = 1111
        u1.id = u1id

        db.session.commit()

        u1 = User.query.get(u1id)

        self.u1 = u1
        self.u1id = u1id

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
