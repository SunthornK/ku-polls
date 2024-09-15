"""
Tests for Poll Voting Logic.

This module contains unit tests for the voting logic in the Polls app.
Specifically, it tests various scenarios for determining whether a user
can vote on a poll question based on its publication and end dates.
"""
from django.test import TestCase
from .utils import create_question


class QuestionVotingTests(TestCase):
    """
    Tests for the voting functionality of the Question model.

    These tests check whether users can vote on poll questions based on
    different conditions, such as the publication date and the voting end date.
    """

    def test_cannot_vote_after_end_date(self):
        """
        Test that voting is not allowed after the end_date has passed.

        This test ensures that a question with an end date in the past
        does not allow any more votes.
        """
        question_with_end_date = create_question(
            question_text="Question with End Date",
            pub_date=-2,
            end_date=-1
        )
        self.assertFalse(question_with_end_date.can_vote())

    def test_can_vote_within_voting_period(self):
        """
        Test that voting is allowed when within the voting period.

        This test verifies that users can vote on a question that is currently
        published and does not have an end date.
        """
        question_with_open_voting = create_question(
            question_text="Question with no end date",
            pub_date=-1
        )
        self.assertTrue(question_with_open_voting.can_vote())

    def test_cannot_vote_if_not_published(self):
        """
        Test that voting is not allowed if the question is not yet published.

        This test checks whether users are prevented from voting on questions
        that have a publication date set in the future.
        """
        future_question = create_question(
            question_text="Future Question",
            pub_date=1
        )
        self.assertFalse(future_question.can_vote())

    def test_can_vote_with_future_end_date(self):
        """
        Test that voting is allowed if the end_date is in the future.

        This test ensures that a question is open for voting if the current
        date is before the end date.
        """
        question_with_future_end_date = create_question(
            question_text="Question with Future End Date",
            pub_date=-2,
            end_date=1
        )
        self.assertTrue(question_with_future_end_date.can_vote())
