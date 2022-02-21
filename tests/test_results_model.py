""" Results Model tests"""

# run tests in terminal:
#   python -m unittest tests/test_results_model.py

import os
from unittest import TestCase

from models import db, User, Workout, Result

os.environ['DATABASE_URL'] = "postgresql:///WODatHome_test_db"

from app import app

db.create_all()


class ResultModelTestCase(TestCase):
    """Test Result Model."""

    def setUp(self):
        """Add test user and test workout"""
        db.drop_all()
        db.create_all()

        test_user = User.register("testUser", "testPass")
        test_user_id = 555
        test_user.id = test_user_id

        db.session.commit

        test_workout = Workout(
            user_id=test_user_id,
            type="RFT",
            name="Test RFT",
            stages=5,
            stage_time=0
        )
        db.session.add(test_workout)
        db.session.commit()

        self.test_user = test_user
        self.test_workout = test_workout

    def test_result_model(self):
        """Does the basic Result Model work?"""
        new_result = Result(
            workout_id=self.test_workout.id,
            user_id=self.test_user.id,
            note="This is a test log."
        )
        db.session.add(new_result)
        db.session.commit()

        self.assertEqual(Result.query.get(1), new_result)
        self.assertEqual(new_result.workout_id, self.test_workout.id)
        self.assertEqual(new_result.note, "This is a test log.")

        # Test result-workout relationship
        self.assertEqual(new_result.workout, self.test_workout)

        # Test result-user relationship
        self.assertEqual(new_result.user, self.test_user)