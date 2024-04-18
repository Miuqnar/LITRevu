from django import forms

from LITRevu.litrevu.models import Ticket, Review


class TicketForm(forms.ModelForm): 
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'image')


class FollowUserForm(forms.Form):
    username = forms.CharField(max_length=150, label="Nom d'utilisateur")
    
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('ticket', 'rating', 'headline', 'body')