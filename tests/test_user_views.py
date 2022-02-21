"""User view tests"""

# run tests in terminal:
#   python -m unittest tests/test_user_views.py

import os
from unittest import TestCase

from models import db, User, Workout, Result

os.environ['DATABASE_URL'] = "postgresql:///WODatHome_test_db"

from app import app

db.create_all()

# Don't have WTForms use CSRF to validate, as I don't know how to test this.
app.config['WTF_CSRF_ENABLED'] = False


class UserViewsTestCase(TestCase):
    """Test User Views of Different Pages"""

    def setUp(self):
        """Create test user and sample workout"""
        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        u1 = User.register("test1", "password")
        u1id = 1111
        u1.id = u1id

        db.session.commit()

        u1 = User.query.get(u1id)

        self.u1 = u1
        self.u1id = u1id

        w1 = Workout(
            user_id=u1.id,
            type="RFT",
            name="Test RFT",
            stages=5,
            stage_time=0
        )

        db.session.add(w1)
        w1id = 2222
        w1.id = w1id

        db.session.commit()

        self.w1 = w1
        self.w1id = w1id

        test_result = Result(
            workout_id=w1id,
            user_id=u1id,
            note="This is a test log."
        )

        db.session.add(test_result)
        db.session.commit()

    def tearDown(self):
        res = super().tearDown()
        db.session.delete(self.u1)
        db.session.commit()
        db.session.rollback()
        return res

    def test_guest_root(self):
        """Test base view for user not signed in."""
        with self.client as c:
            resp = c.get('/', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Create Account", str(resp.data))

    def test_guest_browse(self):
        """Test browse page for user not signed in."""
        with self.client as c:
            resp = c.get('/browse')

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Browse Exercises", str(resp.data))

    def test_guest_signup_view(self):
        """Test sign up page view."""
        with self.client as c:
            resp = c.get('/register')

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Create a New Account", str(resp.data))

    def test_register_new_user(self):
        """Test registering a new user."""
        with self.client as c:
            resp = c.post('/register', data={
                "username": "testNewUser",
                "password": "testNewPassword"}, follow_redirects=True)

            user = User.query.filter_by(username="testNewUser").one()

            self.assertIsNotNone(user)
            self.assertEqual(user.username, "testNewUser")
            self.assertIn("Your Workouts", str(resp.data))

            db.session.delete(user)
            db.session.commit()

    def test_valid_login(self):
        """Test user login."""
        with self.client as c:
            resp = c.post('/login', data={
                "username": "test1",
                "password": "password"
            }, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Welcome back, test1", str(resp.data))

    def test_invalid_login(self):
        """Test invalid login attempt."""
        with self.client as c:
            resp = c.post('/login', data={
                "username": "test1",
                "password": "wrongpassword"
            }, follow_redirects=True)

        self.assertIn("Invalid username/password", str(resp.data))

    def test_user_home_view(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess["username"] = self.u1.username
            resp = c.get('/', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Welcome back, test1", str(resp.data))

    def test_create_workout_view(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess["username"] = self.u1.username
            resp = c.get(f'/users/{self.u1.username}/workout/create')

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Create New Workout", str(resp.data))

    def test_create_new_workout(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess["username"] = self.u1.username
            resp = c.post(
                f'/users/{self.u1.username}/workout/create', data={
                    "type": "RFT",
                    "name": "Test RFT"
                },
                follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test RFT", str(resp.data))

    def test_workout_view(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess["username"] = self.u1.username
            resp = c.get(
                f'/users/{self.u1.username}/workout/{self.w1id}')

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test RFT", str(resp.data))
            self.assertIn(
                "Complete 5 rounds as quickly as possible", str(resp.data))

    def test_history_view(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess["username"] = self.u1.username
            resp = c.get(
                f'/users/{self.u1.username}/history')

            self.assertEqual(resp.status_code, 200)
            self.assertIn("workout history", str(resp.data))
            self.assertIn("This is a test log.", str(resp.data))

    def test_execute_view(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess["username"] = self.u1.username
            resp = c.get(
                f'/users/{self.u1.username}/workout/{self.w1id}/execute')

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test RFT", str(resp.data))
            self.assertIn(
                "complete this set 5 times.", str(resp.data))


    # redirecting to home???
    # def test_log_results(self):
    #     with self.client as c:
    #         with c.session_transaction() as sess:
    #             sess["username"] = self.u1.username
    #         resp = c.post(
    #             f'/users/{self.u1id}/workout/{self.w1id}/log',
    #             data={
    #                 "workout_id": self.w1id,
    #                 "user_id": self.u1id,
    #                 "note": "This is a test note."
    #             },
    #             follow_redirects=True)

    #         self.assertEqual(resp.status_code, 200)
    #         self.assertIn("This is a test log", str(resp.data))
