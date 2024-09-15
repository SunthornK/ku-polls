"""
Tests for the Polls Index View.

This module contains unit tests for the `index` view of the Polls app.
The tests check the visibility of questions on the index page based on their
publication dates, ensuring that only questions with past publication dates
are displayed to users.
"""
from django.urls import reverse
from django.test import TestCase
from .utils import create_question


class QuestionIndexViewTests(TestCase):
    """
    Unit tests for the index view of the Polls app.

    These tests verify the correct behavior of the `index` view
    when displaying poll questions based on their publication date.
    """

    def test_no_questions(self):
        """If no questions exist, an appropriate message is displayed."""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """Questions with a pub_date in the past are displayed."""
        question = create_question(question_text="Past question.",
                                   pub_date=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        """Questions with a pub_date in the future aren't displayed."""
        create_question(question_text="Future question.", pub_date=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """Only past questions are displayed."""
        question = create_question(question_text="Past question.",
                                   pub_date=-30)
        create_question(question_text="Future question.", pub_date=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_two_past_questions(self):
        """The index page may display multiple past questions."""
        question1 = create_question(question_text="Past question 1.",
                                    pub_date=-30)
        question2 = create_question(question_text="Past question 2.",
                                    pub_date=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )
