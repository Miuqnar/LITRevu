from django.views import View
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


from LITRevu.litrevu import forms, models
from LITRevu.authentication.models import User
from LITRevu.litrevu.models import Ticket, UserFollows



# Restreigner l’accès à la page d’accueil
@login_required
def home(request):
    tickets = models.Ticket.objects.all()
    return render(request, 'litrevu/home.html', context={'tickets': tickets})

class TicketCreateView(LoginRequiredMixin, View):
    template_name = 'litrevu/create_ticket.html'
    form_class = forms.TicketForm
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})
    
    def post(self, request):
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                ticket = form.save(commit=False)
                ticket.user = request.user
                ticket.save()
                return redirect('home')
            return render(request, self.template_name, context={'form': form})
                


class FollowUserView(LoginRequiredMixin, View):
    template_name = 'litrevu/follower_user.html'
    form_class = forms.FollowUserForm
    
    def get(self, request):
        form = self.form_class()
        following = request.user.following.all()
        followers = request.user.followed_by.all()
        return render(request, self.template_name, context={'form': form, 'following': following, 'followed_users': followers})
    

    def post(self, request):
        form = self.form_class(request.POST)
        message = ''
        if form.is_valid():
            followed_username = form.cleaned_data['username']
            followed_user = User.objects.get(username=followed_username)
            
            if followed_user == request.user:
                message = "Vous ne pouvez pas vous suivre vous-même."
                return redirect('follower_user')
            elif UserFollows.objects.filter(user=request.user, followed_user=followed_user).exists():
                message = f"Vous suivez déjà {followed_username}"
                return redirect('follower_user')
            else:
                user_follows = UserFollows(user=request.user, followed_user=followed_user)
                user_follows.save()
                return redirect('follower_user')
        return render(request, self.template_name, context={'form': form, 'message': message})

        

class UnfollowUserView(LoginRequiredMixin, View):
    form_class = forms.FollowUserForm
    
    def get(self, request, user_id):
        user_to_unfollow = UserFollows.objects.get(pk=user_id)
        user_to_unfollow.delete()
        return redirect('follower_user')
    
    def post(self, request, user_id):
        form = self.form_class(request.POST)
        if form.is_valid():
            user_to_unfollow = UserFollows.objects.get(pk=user_id)
            user_to_unfollow.delete()
        return redirect('follower_user')



class ReviewCreateView(LoginRequiredMixin, View):
    template_name = 'litrevu/create_review.html'
    form_class = forms.ReviewForm
    
    def get(self, request, ticket_id):
        ticket = Ticket.objects.get(pk=ticket_id)
        form = self.form_class(initial={'ticket': ticket})
        return render(request, self.template_name, context={'form': form})
    
    def post(self, request, ticket_id):
        ticket = Ticket.objects.get(pk=ticket_id)
        form =  self.form_class(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('home')
        return render(request, self.template_name, context={'form': form, 'ticket': ticket})
    
    
    
