from django import forms
from django.conf import settings

from feedback.models import Question, Response
from feedback.utils import verify_captcha

class ActiveQuestionsForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        questions = Question.objects.filter(active=True)
        for question in questions:
            if question.qtype == 1:
                field = forms.CharField(
                    max_length=500, 
                    label=question.text)
            elif question.qtype == 2:
                options = question.multichoiceoption_set.all()
                field = forms.ChoiceField(
                    choices = [(o.id, o.text2) for o in options],
                    label=question.text
                )
            self.fields[f"question_{question.order}"] = field


    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
        

    