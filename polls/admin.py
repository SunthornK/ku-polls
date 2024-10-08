"""
Admin site configuration for the polling application.

Registers the following models with the Django admin interface:
- `Question`
- `Choice`
- `Vote`
"""
from django.contrib import admin

from .models import Question, Choice, Vote

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Vote)
