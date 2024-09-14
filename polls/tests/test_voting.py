from django.test import TestCase
from .utils import create_question


class QuestionVotingTests(TestCase):
    def test_cannot_vote_after_end_date(self):
        """Cannot vote if the end_date is in the past."""
        question_with_end_date = create_question(
            question_text="Question with End Date",
            pub_date=-2,
            end_date=-1
        )
        self.assertFalse(question_with_end_date.can_vote())

    def test_can_vote_within_voting_period(self):
        """Can vote if the current time is within the voting period."""
        question_with_open_voting = create_question(
            question_text="Question with no end date",
            pub_date=-1)
        self.assertTrue(question_with_open_voting.can_vote())

    def test_cannot_vote_if_not_published(self):
        """Cannot vote if the question is not yet published."""
        future_question = create_question(
            question_text="Future Question",
            pub_date=1
        )
        self.assertFalse(future_question.can_vote())

    def test_can_vote_with_future_end_date(self):
        """Can vote if the current time is within the voting period
        and the end_date is in the future."""
        question_with_future_end_date = create_question(
            question_text="Question with Future End Date",
            pub_date=-2,
            end_date=1
        )
        self.assertTrue(question_with_future_end_date.can_vote())
