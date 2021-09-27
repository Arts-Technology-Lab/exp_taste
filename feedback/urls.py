from django.urls import path
from django.views.generic import TemplateView

import feedback.views as views

app_name = "feedback"

urlpatterns = [
    path("", 
         views.submit_feedback,
         name="form"),
    path("thankyou",
        TemplateView.as_view(template_name="feedback/thankyou.html"), 
        name="thankyou"),
    path("list",
         views.FeedbackList.as_view(),
         name="list"),
    path("detail/<uuid:pk>",
         views.FeedbackDetail.as_view(),
         name="detail"),
     path('export/excel',
          views.to_excel,
          name="export_excel")
]