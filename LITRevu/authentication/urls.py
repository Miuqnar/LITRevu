from django.contrib.auth.views import LogoutView
from django.urls import path


from LITRevu.authentication.views import LoginPageView, SignupPageView

urlpatterns = [
    path('login/', LoginPageView.as_view(), name='login'),
    path('signup/', SignupPageView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
