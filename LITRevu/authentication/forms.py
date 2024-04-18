from typing import Any
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'placeholder': 'Nom d’utilisateur'}), label='')
    password = forms.CharField(max_length=64, widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}), label='')


class SignupForm(UserCreationForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].help_text = ''
            self.fields[field_name].label = ''
        # self.fields['username'].label = 'Nom d’utilisateur'
        # self.fields['password1'].label = 'Mot de passe'
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': 'Mot de passe'})
        # self.fields['password2'].label = 'Confirme le mot de passe'
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Confirme le mot de passe'})

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Nom d’utilisateur'}),
        }
