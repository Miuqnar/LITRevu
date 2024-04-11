from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views import View

from LITRevu.authentication import forms



class LoginPageView(View):
    template_name = 'authentication/login.html'
    form_class = forms.LoginForm
    

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})
        
    
    def post(self, request):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('home')
        message = 'Identifiant invalide.'
        return render(request, self.template_name, context={'form': form, 'message': message})
 
 

class SignupPageView(View):
    template_name = 'authentication/signup.html'
    form_class = forms.SignupForm
    

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        return render(request, self.template_name, context={'form': form})
    

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')