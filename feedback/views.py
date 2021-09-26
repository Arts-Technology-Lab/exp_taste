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


def submit_feedback(request):
    intro = "We're working on some feedback questions. Please check again soon!"
    try:
        copy = PageCopy.objects.filter(current=True)[0]
        intro = copy.html
    except IndexError:
        pass
    questions = Question.objects.filter(active=True)

    context = {
        "intro": intro,
        "questions": questions,
        "captcha_error": False
    }
    if request.POST:
        data = request.POST.copy()
        captcha = data.get("g-recaptcha-response", None)
        if not captcha:
            context["captcha_error"] = True
        else:
            feedback = Feedback(
                name=data["name"], 
                email=data["email"], 
                location=data["location"])
            feedback.save()
            for key, value in data.items():
                if key.startswith("question_"):
                    q_id = key.split("_")[1]
                    question = questions.get(id=int(q_id))
                    if question.qtype == 1:
                        fr = FreeResponse(question=question, 
                                        feedback=feedback, 
                                        response=value)
                        fr.save()
                    elif question.qtype == 2:
                        selected = MultiChoiceOption.objects.get(id=int(value))
                        mcr = MultiChoiceResponse(question=question, 
                                                feedback=feedback, 
                                                selected=selected)
                        mcr.save()
            return redirect("feedback:thankyou")
    return render(
        request, 
        "feedback/form.html", context=context
        )

class FeedbackList(LoginRequiredMixin, ListView):
    model = Feedback
    template_name = "feedback/list.html"
    paginate_by = 25


class FeedbackDetail(LoginRequiredMixin, DetailView):
    model = Feedback
    template_name = "feedback/detail.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        all_responses = (list(self.object.freeresponse_set.all()) + 
                         list(self.object.multichoiceresponse_set.all()))
        all_responses.sort(key=lambda r: r.question.order)
        context["all_responses"] = all_responses
        return context