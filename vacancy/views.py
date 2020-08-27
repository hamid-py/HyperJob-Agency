from django.core.exceptions import PermissionDenied
from django.forms import forms, CharField
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from .models import Vacancy


class VacancyView(ListView):
    model = Vacancy
    template_name = 'vacancy/vacancy.html'


class NewForm(forms.Form):
    description = CharField(max_length=1024)


class NewView(View):
    def get(self, request, *args, **kwargs):
        raise PermissionDenied
    #     new_resume = NewForm
    #     return render(request, 'vacancy/new.html', context={'new_resume': new_resume})

    def post(self, request):
        new_resume = NewForm(request.POST)
        if request.user.is_authenticated:
            if request.user.is_staff:
                if new_resume.is_valid():
                    Vacancy.objects.create(description=new_resume.cleaned_data['description'], author=request.user)
                    return HttpResponseRedirect('/home')
                raise PermissionDenied
            raise PermissionDenied
        raise PermissionDenied
