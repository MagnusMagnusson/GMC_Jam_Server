
from django.urls import path
from jam42_babel import views as view

urlpatterns = [
    path("api/<slug:mode>/scores", view.Highscores.as_view()),
    path("api/<slug:mode>/user/<slug:uid>", view.Users.as_view())
]