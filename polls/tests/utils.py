"""
Utility functions for the Polls app.

Contains helper functions for the test cases, such as
creating poll questions and handling user votes.
"""

from django.utils import timezone
from polls.models import Question


def create_question(question_text, pub_date=None, end_date=None):
    """Create a question with the given `question_text`.

    And publish it with the given number of `days` offset to now
    (negative for past, positive for future).
    """
    if pub_date is not None:
        pub = timezone.now() + timezone.timedelta(days=pub_date)
    else:
        pub = pub_date

    if end_date is not None:
        end = timezone.now() + timezone.timedelta(days=end_date)
    else:
        end = end_date
    return Question.objects.create(question_text=question_text,
                                   pub_date=pub, end_date=end)
