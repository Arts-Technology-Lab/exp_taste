import logging

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from feedback.models import (
    PageCopy, 
    Question, 
    Feedback, 
    FreeResponse, 
    MultiChoiceResponse,
    MultiChoiceOption
    )
from feedback.forms import ActiveQuestionsForm

logger = logging.getLogger(__name__)

def submit_feedback(request):
    intro = "We're working on some feedback questions. Please check again soon!"
    try:
        copy = PageCopy.objects.filter(current=True)[0]
        intro = copy.html
    except IndexError:
        pass
    
    if request.POST:
        logger.info(request.POST)
        data = request.POST.copy()
        form = ActiveQuestionsForm(data, request=request)
        if form.is_valid():
            form.save()        
            return redirect("feedback:thankyou")
    else:
        form = ActiveQuestionsForm(request=request)
    context = {
        "intro": intro,
        "form": form,
    }
    return render(request, "feedback/form.html", context=context)

class FeedbackList(LoginRequiredMixin, ListView):
    model = Feedback
    template_name = "feedback/list.html"
    paginate_by = 25


class FeedbackDetail(LoginRequiredMixin, DetailView):
    model = Feedback
    template_name = "feedback/detail.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["all_responses"] = self.object.response_set.all()
        return context