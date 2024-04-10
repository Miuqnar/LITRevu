from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Restreigner l’accès à la page d’accueil
@login_required
def home(request):
    return render(request,  'homepage/home.html')
