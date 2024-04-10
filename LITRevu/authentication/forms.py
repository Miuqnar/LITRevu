from typing import Any
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'placeholder': 'Nom d’utilisateur'}) ,label='')
    password = forms.CharField(max_length=64, widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}), label='')
    

class SignupForm(UserCreationForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].help_text = ''
            self.fields[field_name].label = ''
        self.fields['password1'].widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'})
        self.fields['password2'].widget=forms.PasswordInput(attrs={'placeholder': 'Confirmer mot de passe'})
        
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Nom d’utilisateur'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Prenom'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Nom'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email'}),
            # 'password1': forms.PasswordInput(attrs={'placeholder': 'Mot de pass'}),
            # 'password2': forms.PasswordInput(attrs={'placeholder': 'Confirmer le mot de pass'}),
        }
        