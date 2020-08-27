from django.contrib.auth.models import User
from django.forms import forms, CharField, BooleanField, PasswordInput, NullBooleanField, EmailField
from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponseForbidden, HttpResponse
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied

from vacancy.models import Vacancy
from .models import Resume


class MenuView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'resume/menu.html', context={})


class ResumeView(ListView):
    model = Resume
    template_name = 'resume/resume.html'


class MySignupView(CreateView):
    form_class = UserCreationForm
    success_url = 'login'
    template_name = 'resume/signup.html'


class MyLoginView(LoginView):
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    template_name = 'resume/login.html'


class NewForm(forms.Form):
    description = CharField(max_length=1024)


class HomeView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = NewForm
            staff = request.user.is_staff
            # resume_list = Resume.objects.filter(author=request.user)
            # vacancy_list = Vacancy.objects.filter(author=request.user)
            # return render(request, 'resume/home.html',
            #               context={'resume_list': resume_list, 'vacancy_list': vacancy_list})
            return render(request, 'resume/home.html', context={'form': form, 'staff': staff})
        return HttpResponseRedirect('/login')

    def post(self, request, *args, **kwargs):
        if 'vacancy' in request.POST:
            # if request.user.is_authenticated:
            # if request.user.is_staff:
            return HttpResponseRedirect('/vacancy/new')
        # raise PermissionDenied
        # return HttpResponseForbidden()
        # raise PermissionDenied
        elif 'resume' in request.POST:
            # if request.user.is_authenticated:
            #     if not request.user.is_staff:
            return HttpResponseRedirect('/resume/new')
        # raise PermissionDenied
        # raise PermissionDenied




class NewView(View):

    def get(self, request, *args, **kwargs):
        raise PermissionDenied
    #     new_resume = NewForm
    #     return render(request, 'resume/new.html', context={'new_resume': new_resume})

    def post(self, request, *args, **kwargs):
        new_resume = NewForm(request.POST)
        if request.user.is_authenticated:
            if not request.user.is_staff:
                if new_resume.is_valid():
                    Resume.objects.create(description=new_resume.cleaned_data['description'], author=request.user)
                    return HttpResponseRedirect('/home')
                raise PermissionDenied
            raise PermissionDenied
        raise PermissionDenied


#
#
class SignUpForm(UserCreationForm):
    is_staff = BooleanField()

    # first_name = CharField(max_length=30, required=False, help_text='Optional.')
    # last_name = CharField(max_length=30, required=False, help_text='Optional.')
    # email = EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'is_staff')


class SignupView(View):
    def get(self, request, *args, **kwargs):
        signupform = SignUpForm()
        return render(request, 'resume/signup.html', context={'signupform': signupform})

    def post(self, request, *args, **kwargs):
        signupform = SignUpForm(request.POST)
        if signupform.is_valid():
            data = signupform.cleaned_data
            User.objects.create_user(username=data['username'], password=data['password2'], is_staff=data['is_staff'])
            return HttpResponseRedirect('/login/')
        return HttpResponseRedirect('signup')
