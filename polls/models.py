import datetime

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
    end_date = models.DateTimeField(null=True, blank=True)

    def is_published(self):
        return timezone.localtime(timezone.now()) >= self.pub_date

    def can_vote(self):
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
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Return the choice text."""
        return self.choice_text
