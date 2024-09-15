"""
Configuration for the Polls application.

Sets the default auto field type and the name of the app.
"""
from django.apps import AppConfig


class PollsConfig(AppConfig):
    """
    Configuration for the Polls application.

    Sets the default auto field type to `BigAutoField` and specifies the
    name of the application as 'polls'.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
