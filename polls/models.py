"""
Defines models for a polling application.

Includes:
- `Question`: Represents a poll question with text, publication date, and
  end date. Provides methods for checking publication status, voting
  eligibility, and recent publication.
- `Choice`: Represents a possible answer to a poll question. Includes a
  property to count the number of votes.
- `Vote`: Represents a vote by a user for a choice in a poll question.
"""

import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Question(models.Model):
    """
    Represents a poll question.

    Attributes:
        question_text (str): The text of the question.
        pub_date (datetime): The date and time the question was published.
    """

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published", default=timezone.now)
    end_date = models.DateTimeField("end date", null=True,
                                    blank=True, default=None)

    def is_published(self):
        """
        Determine if the question has been published.

        Returns:
            bool: True if the current time is after or equal
             to the publication date, False otherwise.
        """
        return timezone.localtime(timezone.now()) >= self.pub_date

    def get_status(self):
        """
        Return whether the status of the poll is open or closed.

        Returns:
            str: 'Open', 'Closed' based on the poll's publication.
        """
        now = timezone.localtime(timezone.now())
        if self.end_date and now > self.end_date:
            return 'Closed'
        return 'Open'

    def can_vote(self):
        """
        Determine if voting is currently allowed for this question.

        Returns:
            bool: True if voting is allowed, False otherwise.
        """
        now = timezone.localtime(timezone.now())
        if self.end_date:
            return self.end_date >= now >= self.pub_date
        return now >= self.pub_date

    def was_published_recently(self):
        """Check if the question was published within the last 24 hours."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def __str__(self):
        """Return the question text."""
        return self.question_text


class Choice(models.Model):
    """A possible answer to a poll question."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    @property
    def votes(self):
        """Getter for the number of votes."""
        return self.vote_set.count()

    def __str__(self):
        """Return the choice text."""
        return self.choice_text


class Vote(models.Model):
    """A vote by a user for a choice in a poll question."""

    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
