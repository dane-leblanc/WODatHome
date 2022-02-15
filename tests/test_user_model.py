"""User model tests"""

# run tests in terminal:
#   python -m unittest tests/test_user_model.py

import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User

from app import app

os.environ['DATABASE_URL'] = "postgresql:///WODatHome_test_db"

db.create_all()


class UserModelTestCase(TestCase):
    """Test User Model"""

    def setUp(self):
        """Create test client, add sample data and test user"""
        db.drop_all()
        db.create_all()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):
        """Does the basic User Model work?"""

        u = User(
            username="TestUser",
            password="TestPass"
        )

        db.session.add(u)
        db.session.commit()

        # User should be in database with no saved workouts.
        self.assertEqual(User.query.get(1), u)
        self.assertEqual(len(u.workouts), 0)

    def test_valid_registration(self):
        u = User.register("TestUser", "TestPass")
        uid = 99
        u.id = uid
        db.session.commit()

        u = User.query.get(uid)
        self.assertIsNotNone(u)
        self.assertEqual(u.username, "TestUser")
        # Users actual password should not be stored
        self.assertNotEqual(u.password, "TestPass")
        # Bcrypt hashed strings start with $2b$
        self.assertTrue(u.password.startswith("$2b$"))

    def test_invalid_registration(self):
        """Test different ways that a user CANNOT register"""

        # Register with no Password
        with self.assertRaises(ValueError) as context:
            User.register("TestUser", "")

        # Register with no Username *****NOT PASSING*****
        # with self.assertRaises(ValueError) as context:
        # User.register("", "TestPass")

        # Register with a username that has already been taken
        u1 = User.register("TestUser", "TestPass1")
        u1id = 999
        u1.id = u1id
        db.session.commit()

        u2 = User.register("TestUser", "TestPass2")
        u2id = 888
        u2.id = u2id

        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
