from django.shortcuts import render, redirect

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
    if request.POST:
        data = request.POST.copy()
        feedback = Feedback(name=data["name"], email=data["email"])
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
        "feedback/form.html", context={
            "intro": intro,
            "questions": questions
            }
        )


