from django.shortcuts import render
from django.views import View

class LoginPageView(View):
    template_name = 'authentication/login.html'
    # class_form = 