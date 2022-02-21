"""User model tests"""

# run tests in terminal:
#   python -m unittest tests/test_workout_model.py

import os
from unittest import TestCase
# from sqlalchemy import exc

from models import db, Workout, User

os.environ['DATABASE_URL'] = "postgresql:///WODatHome_test_db"

from app import app

db.create_all()


class WorkoutModelTestCase(TestCase):
    """Test Workout Model"""

    def setUp(self):
        """Add test user"""
        db.drop_all()
        db.create_all()

        test_user = User.register("testUser", "testPass")
        test_user_id = 555
        test_user.id = test_user_id

        db.session.commit()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_workout_model(self):
        """Does the basic Workout Model work?"""
        test_workout = Workout(
            user_id=555,
            type="AMRAP",
            name="Test AMRAP",
            stages=3,
            stage_time=3)
        db.session.add(test_workout)
        db.session.commit()

        self.assertEqual(Workout.query.get(1), test_workout)
        self.assertEqual(test_workout.name, "Test AMRAP")
        self.assertEqual(test_workout.type, "AMRAP")
        self.assertEqual(test_workout.stages, 3)

        # Test user-workout relationship
        self.assertEqual(test_workout.user, User.query.get(555))
