from django import forms


class LoginForm(forms.Form):
    usarname = forms.CharField(max_length=64, label='Nom d’utilisateur ')
    password = forms.CharField(max_length=64, widget=forms.PasswordInput, label='Mot de passe')