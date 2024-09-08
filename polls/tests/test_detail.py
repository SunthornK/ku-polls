from django.urls import reverse
from django.test import TestCase
from .utils import create_question


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """The detail view of a future question returns a 404 not found."""
        future_question = create_question(question_text='Future question.', pub_date=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """The detail view of a past question displays the question's text."""
        past_question = create_question(question_text='Past Question.', pub_date=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
