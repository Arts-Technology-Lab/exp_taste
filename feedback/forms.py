from django import forms
from django.conf import settings

import requests

from feedback.models import Question, Response

class ActiveQuestionsForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
        

    