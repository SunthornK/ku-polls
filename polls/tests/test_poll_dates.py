"""
Tests for Poll Question Logic.

This module contains unit tests for the question logic in the Polls app.
Specifically, it tests various scenarios for determining whether a user
can see a poll question based on its publication and end dates.
"""
import datetime
from django.utils import timezone
from django.test import TestCase
from .utils import create_question
from polls.models import Question


class QuestionModelTests(TestCase):
    """Unit tests for the Question model's publication logic."""

    def test_question_with_future_pub_date(self):
        """
        Test that a question with a future publication date is not published.

        Ensures that the `is_published()` method returns False when
        the `pub_date` is in the future, meaning the question should not
        be visible to users yet.
        """
        future_question = create_question(
            question_text="Future Question",
            pub_date=1
        )
        self.assertFalse(future_question.is_published())

    def test_question_with_past_pub_date(self):
        """
        Test that a question with a past publication date is published.

        Ensures that the `is_published()` method returns True for questions
        whose `pub_date` is in the past, meaning the question should be visible
        to users.
        """
        past_question = create_question(
            question_text="Past Question",
            pub_date=-1
        )
        self.assertTrue(past_question.is_published())

    def test_question_with_default_pub_date(self):
        """
        Test that a question with a current publication date is published.

        Verifies that a question with `pub_date` set to the current time
        is considered published.
        """
        present_question = Question.objects.create(
            question_text="Present Question",
            pub_date=timezone.now()
        )
        self.assertTrue(present_question.is_published())

    def test_was_published_recently_with_future_question(self):
        """
        Test that`was_published_recently()`returns False for future questions.

        Ensures that a question with a future `pub_date` does not return True
        for the `was_published_recently()` method.
        """
        future_question = create_question(
            question_text="Future Question",
            pub_date=30
        )
        self.assertFalse(future_question.was_published_recently())

    def test_was_published_recently_with_old_question(self):
        """
        Test that `was_published_recently()` returns False for old questions.

        Ensures that a question whose `pub_date` is more than 1 day in the past
        does not return True for the `was_published_recently()` method.
        """
        old_time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question.objects.create(
            question_text="Old Question",
            pub_date=old_time
        )
        self.assertFalse(old_question.was_published_recently())

    def test_was_published_recently_with_recent_question(self):
        """
        Test that `was_published_recently()` returns True for recent questions.

        Ensures that a question whose `pub_date` is within the last 24 hours
        returns True for the `was_published_recently()` method.
        """
        recent_time = timezone.now() - datetime.timedelta(
            hours=23, minutes=59, seconds=59
        )
        recent_question = Question.objects.create(
            question_text="Recent Question",
            pub_date=recent_time
        )
        self.assertTrue(recent_question.was_published_recently())
