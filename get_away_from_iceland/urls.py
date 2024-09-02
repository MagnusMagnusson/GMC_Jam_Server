
from django.urls import path
from get_away_from_iceland import views as view

urlpatterns = [
    path("api/<slug:mode>/scores", view.Highscores.as_view()),
]