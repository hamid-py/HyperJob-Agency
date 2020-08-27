from django.urls import path

from .views import VacancyView, NewView

urlpatterns = [
    path('/', VacancyView.as_view()),
    path('new/', NewView.as_view())
]
