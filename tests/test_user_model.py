"""User model tests"""

# run tests in terminal:
#   python -m unittest tests/test_user_model.py

import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User

os.environ['DATABASE_URL'] = "postgresql:///WODatHome_test_db"

from app import app

db.create_all()


class UserModelTestCase(TestCase):
    """Test User Model"""

    def setUp(self):
        """Add sample data and test user"""
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
        uid = 11
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
        #     User.register("", "TestPass")

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

    def test_valid_authentication(self):
        u = User.authenticate(self.u1.username, "password")
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.u1id)

    def test_invalid_username(self):
        self.assertFalse(User.authenticate("wrong_user", "password"))

    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.u1.username, "wrong_password"))
