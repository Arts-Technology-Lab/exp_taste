import logging
from tempfile import NamedTemporaryFile
from django.http.response import HttpResponse

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import FileResponse

from feedback.models import (
    PageCopy, 
    Feedback, 
    utc_now
    )
from feedback.forms import ActiveQuestionsForm
from feedback.utils import feedback_to_excel

logger = logging.getLogger(__name__)

def submit_feedback(request):
    intro = "We're working on some feedback questions. Please check again soon!"
    try:
        copy = PageCopy.objects.filter(current=True)[0]
        intro = copy.html
    except IndexError:
        pass
    
    if request.POST:
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

@login_required
def to_excel(request):
    ts = utc_now().isoformat()
    filename = f"ExpTaste_Feedback_{ts}.xlsx"
    wb = feedback_to_excel(Feedback.objects.all())
    tmp = NamedTemporaryFile()
    wb.save(tmp.name)
    tmp.seek(0)
    response = HttpResponse(tmp.read())
    response["Content-Type"] = "application/vnd.ms-excel"
    response["Content-Disposition"] = f"attachment; filename={filename}"
    return response