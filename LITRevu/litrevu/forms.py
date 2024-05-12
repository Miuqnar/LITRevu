from django import forms
from typing import Any
from LITRevu.litrevu.models import Ticket, Review
from LITRevu.litrevu.models import UserFollows
from LITRevu.authentication.models import User


class TicketForm(forms.ModelForm):
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['title'].label = "Titre"
        self.fields['title'].label = "Titre"
        
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'image')
        

# class TicketReviewForm(forms.ModelForm):
#     rating = forms.ChoiceField()
#     headline = forms.ChoiceField()
#     body = forms.TextField()
#     class Meta:
#         model = Ticket
#         fields = ('title', 'description', 'image')

#     def save(self, commit=True):
#         ticket = super().save(commit=True)
#         review = Review.objects.create(ticket=ticket, 
#                                        ratings=self.cleaned_data['ratings'],
#                                        headline=self.cleaned_data['headline'], 
#                                        body=self.cleaned_data['body'])
class ReviewForm(forms.ModelForm):
    RATING_CHOICES = (
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect)
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['headline'].label = "Titre"
        self.fields['rating'].label = "Note"
        self.fields['body'].label = "Commentaire"
        
    class Meta:
        model = Review
        fields = ('headline', 'rating', 'body')
        



class FollowUserForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=100)

    class Meta:
        model = UserFollows
        fields = []

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(FollowUserForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        if username == self.user.username:
            raise forms.ValidationError('You cannot follow yourself.')

        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'User {username} does not exist.')

        if UserFollows.objects.filter(user=self.user, followed_user__username=username).exists():
            raise forms.ValidationError(f'You are already following {username}.')

        return User.objects.get(username=username)

    def save(self, commit=True):
        return UserFollows.objects.create(
            user=self.user,
            followed_user=self.cleaned_data['username']
        )
