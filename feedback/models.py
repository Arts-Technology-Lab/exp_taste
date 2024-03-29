import datetime
import uuid

import markdown

from django.db import models

def utc_now():
    return datetime.datetime.now(tz=datetime.timezone.utc)


class Feedback(models.Model):
    id = models.UUIDField("id", primary_key=True, default=uuid.uuid4)
    name = models.CharField("Name", max_length=150, default="", blank=True)
    email = models.EmailField("Email", default="", blank=True)
    location = models.CharField("Location", max_length=200, default="")
    created = models.DateTimeField("Timestamp", default=utc_now)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return str(self.created)


class Question(models.Model):
    class QuestionTypes(models.IntegerChoices):
        FREE_RESPONSE = 1
        MULTIPLE_CHOICE = 2
        
    text = models.TextField("Question")
    active = models.BooleanField("Active", default=True)
    qtype = models.PositiveSmallIntegerField("Question Type", 
                                             choices=QuestionTypes.choices,
                                             default=1)
    order = models.PositiveSmallIntegerField("Order", default=1)
    required = models.BooleanField("Required", default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.text[:20]


class MultiChoiceOption(models.Model):
    order = models.PositiveSmallIntegerField("Order", default=1)
    text2 = models.CharField("Text", max_length=280, default="")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    weight = models.IntegerField("Weight", default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.text2[:20]


class Response(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField("Free Response", default="", blank=True)
    selected = models.ForeignKey(
        MultiChoiceOption, 
        on_delete=models.CASCADE,
        blank=True, null=True)

    class Meta:
        ordering = ["question__order"]

class FreeResponse(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response = models.TextField("Response")
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE)


class MultiChoiceResponse(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected = models.ForeignKey(MultiChoiceOption, on_delete=models.CASCADE)
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE)


class PageCopy(models.Model):
    text = models.TextField("Text")
    current = models.BooleanField("Current", default=True)

    class Meta:
        verbose_name = "Feedback Page Intro"

    def __str__(self):
        return self.text[:20]

    @property
    def html(self):
        return markdown.markdown(self.text)
            
