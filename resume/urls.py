from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.views.generic import RedirectView

from .views import MenuView, ResumeView, MySignupView, MyLoginView, HomeView, NewView, SignupView

urlpatterns = [
    path('', MenuView.as_view()),
    path('resumes/', ResumeView.as_view()),
    path('resume/new', NewView.as_view()),
    path('signup', SignupView.as_view()),
    path('login', MyLoginView.as_view()),
    path('login/', RedirectView.as_view(url='/login')),
    path('signup/', RedirectView.as_view(url='/signup')),
    path('home/', HomeView.as_view()),
    path('logout', LogoutView.as_view()),

]