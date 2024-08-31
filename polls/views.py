from django.db.models import F
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class DetailView(generic.DetailView):
    model = Question
    object = Question
    template_name = "polls/detail.html"

    def get_detail(self, request, *args, **kwargs):
        try:
            self.object = get_object_or_404(Question, pk=kwargs['pk'])
        except Http404:
            messages.error(request, f"Poll with ID {kwargs['pk']} is not exist")
            return redirect("polls:index")
        if not self.object.can_vote():
            messages.error(request, f"Poll number {self.object.pk} has ended, which is not available for voting.")
            return redirect("polls:index")
        if not self.object.is_published():
            messages.error(request, f"Poll number {self.object.pk} is not available")
            return redirect("polls:index")
        return render(request, self.template_name, {"question": self.object})


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
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
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
