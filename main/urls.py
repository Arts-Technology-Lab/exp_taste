from django.urls import path

import main.views as views

app_name = "main"

urlpatterns = [
    path("", 
         views.Home.as_view(),
         name="home"),
    path("about/",
         views.about,
         name="about")
]
