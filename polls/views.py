from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from .models import Choice, Question, Vote
from django.contrib.auth.decorators import login_required
import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

logger = logging.getLogger('polls')


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip_addr = get_client_ip(request)
    logger.info(f"{user.username} logged in from {ip_addr}")


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    ip_addr = get_client_ip(request)
    logger.info(f"{user.username} logged out from {ip_addr}")


def get_client_ip(request):
    """Get the visitor’s IP address using request headers."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class IndexView(generic.ListView):
    """
    Displays a list of the latest poll questions that have been published.
    """
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()).order_by('-pub_date')


class DetailView(generic.DetailView):
    """Displays the choices of a specific poll question and allow voting."""
    model = Question
    object = Question
    template_name = "polls/detail.html"

    def get(self, request, *args, **kwargs):
        """Handle GET requests for the poll question."""
        try:
            self.object = get_object_or_404(Question, pk=kwargs['pk'])
        except Http404:
            messages.error(request,
                           f"Poll with ID {kwargs['pk']} does not exist")
            return redirect("polls:index")
        if not self.object.can_vote():
            messages.error(request,
                           f"Poll number {self.object.pk} has ended, "
                           f"which is not available for voting.")
            return redirect("polls:index")
        if not self.object.is_published():
            messages.error(request,
                           f"Poll number {self.object.pk} is not available")
            return redirect("polls:index")
        return render(request, self.template_name, {"question": self.object})


class ResultsView(generic.DetailView):
    """Display results of a specific poll question."""
    model = Question
    template_name = "polls/results.html"


@login_required()
def vote(request, question_id):
    """Process a vote for a poll question."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    # Reference to the current user
    user = request.user

    # Get the user's vote
    # Increment votes by creating or updating a Vote object, as you've done in your try/except block
    try:
        vote = user.vote_set.get(choice__question=question)
        vote.choice = selected_choice
        vote.save()
        messages.success(request, f"Your vote was updated to '{selected_choice.choice_text}'")
    except Vote.DoesNotExist:
        Vote.objects.create(user=user, choice=selected_choice)
        messages.success(request, f"Your vote for '{selected_choice.choice_text}' was recorded successfully")

    # Redirect to the results page
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
