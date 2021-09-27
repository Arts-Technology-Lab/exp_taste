import logging

from django import forms
from django.conf import settings
from django.forms.widgets import RadioSelect, Textarea


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, Div

from feedback.models import Question, Response, Feedback
from feedback.utils import verify_captcha

logger = logging.getLogger(__name__)

class ActiveQuestionsForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "feedback-form"
        self.helper.form_method = "POST"
        self.helper.form_action = "."
        self.helper.label_class = "question"
        questions = Question.objects.filter(active=True)
        for question in questions:
            if question.qtype == 1:
                field = forms.CharField(
                    max_length=500, 
                    label=question.text,
                    required=question.required,
                    widget=Textarea(attrs={"rows": 1}))
            elif question.qtype == 2:
                options = question.multichoiceoption_set.all()
                field = forms.ChoiceField(
                    choices = [(o.id, o.text2) for o in options],
                    label=question.text,
                    required=question.required,
                    widget=RadioSelect
                )
            self.fields[f"question_{question.id}"] = field
        self.helper.layout = Layout(
            *(Field(key) for key in self.fields.keys()),
            Div(css_class="g-recaptcha",
                data_sitekey=settings.RECAPTCHA_SITE,
                data_callback="enableSubmit",
                data_expired_callback="captchaExpired"),
            Div(
                Submit(
                    'submit', 
                    'Submit', 
                    css_class="btn btn-primary", 
                    disabled=True,
                    id='feedback-submit'),
                css_class="form-group d-flex flex-row-reverse"
            )
        )

    def clean(self):
        cleaned_data = super().clean()
        token = self.request.POST.get("g-recaptcha-response", None)
        captcha = verify_captcha(token)
        if not captcha.get('success', False):
            logger.info(captcha)
            raise forms.ValidationError("Captcha Failed")
        if not any(cleaned_data.values()):
            raise forms.ValidationError("Please answer at least one question")
        return cleaned_data

    def save(self):
        feedback = Feedback()
        feedback.save()
        logger.info(self.cleaned_data)
        for key, value in self.cleaned_data.items():
            if not key.startswith("question_"): 
                continue
            q_id = key.split("_")[1]
            question = Question.objects.get(id=q_id)
            response = Response(feedback=feedback, question=question)
            if question.qtype == 1:
                response.text = value
            elif question.qtype == 2:
                option = question.multichoiceoption_set.get(id=int(value))
                response.selected = option
            response.save()
        
                

