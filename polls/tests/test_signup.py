"""
Unit tests for the user signup functionality in the Django application.

This module contains tests for verifying the behavior of the user signup form.
It includes tests for successful user registration and for handling errors.
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UserSignupTest(TestCase):
    """
    Test suite for the user signup functionality in the Django application.

    This test suite verifies that the user signup form behaves as expected,
    including successful user creation and handling of password mismatches.
    """

    def test_signup_form(self):
        """Test successful user registration with valid data."""
        # URL of the signup page
        url = reverse('signup')

        user_data = {
            'username': 'test_user',
            'password1': 'hackme11',
            'password2': 'hackme11',
        }

        # Post the data to the signup page
        response = self.client.post(url, data=user_data)

        # Check that the response redirects
        self.assertEqual(response.status_code, 302)

        # Ensure the user was created in the database
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_signup_form_password_mismatch(self):
        """Test handling of password mismatch in the signup form."""
        url = reverse('signup')
        user_data = {
            'username': 'test_user',
            'password1': 'hackme11',
            'password2': 'WrongPassword',
        }

        response = self.client.post(url, data=user_data)
        # Ensure the form did not validate and user was not created
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='newuser').exists())
