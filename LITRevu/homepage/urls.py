from django.urls import path

from LITRevu.homepage.views import home

urlpatterns = [
    path('', home, name='home')
]