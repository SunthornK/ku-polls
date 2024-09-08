import datetime
from django.utils import timezone
from django.test import TestCase
from .utils import create_question
from polls.models import Question

class QuestionModelTests(TestCase):
    def test_question_with_future_pub_date(self):
        """Question with future pub date should not be shown"""
        future_question = create_question(
            question_text="Future Question",
            pub_date=1
        )
        self.assertFalse(future_question.is_published())

    def test_question_with_past_pub_date(self):
        """Question with pub date in the past should be published."""
        past_question = create_question(
            question_text="Past Question",
            pub_date=-1
        )
        self.assertTrue(past_question.is_published())

    def test_question_with_default_pub_date(self):
        """Question with the default pub date should be published now."""
        present_question = Question.objects.create(
            question_text="Present Question",
            pub_date=timezone.now()
        )
        self.assertTrue(present_question.is_published())

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        future_question = create_question(pub_date=30, question_text="Future Question")
        self.assertFalse(future_question.was_published_recently())

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        old_time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question.objects.create(pub_date=old_time, question_text="Old Question")
        self.assertFalse(old_question.was_published_recently())

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        recent_time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question.objects.create(pub_date=recent_time, question_text="Recent Question")
        self.assertTrue(recent_question.was_published_recently())
