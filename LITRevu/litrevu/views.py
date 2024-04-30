from django.shortcuts import redirect, render
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.views.generic import DeleteView


from LITRevu.litrevu import forms, models
from LITRevu.litrevu.models import Ticket, UserFollows


# Restreigner l’accès à la page d’accueil
@login_required
def home(request):
    tickets = models.Ticket.objects.all()
    return render(request, 'litrevu/home.html', context={'tickets': tickets})


class TicketCreateView(LoginRequiredMixin, CreateView):
    template_name = 'litrevu/create_ticket.html'
    form_class = forms.TicketForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class FollowUserView(LoginRequiredMixin, CreateView):
    template_name = 'litrevu/follower_user.html'
    # model = UserFollows
    form_class = forms.FollowUserForm
    success_url = reverse_lazy('follower_user')

    def get_form_kwargs(self):
        kwargs = super(FollowUserView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['following'] = self.request.user.following.all()
        context['followed_users'] = self.request.user.followed_by.all()
        return context


class UnfollowUserView(LoginRequiredMixin, DeleteView):
    template_name = 'litrevu/follower_user.html'
    form_class = forms.FollowUserForm
    success_url = reverse_lazy('follower_user')

    def get_object(self, queryset=None):
        user_id = self.kwargs.get('user_id')
        return UserFollows.objects.get(pk=user_id)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class ReviewCreateView(LoginRequiredMixin, CreateView):
    template_name = 'litrevu/ticket-review.html'
    form_class = forms.ReviewForm
    success_url = reverse_lazy('home') 

    def form_valid(self, form):
        form.instance.ticket = self.ticket
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ticket'] = self.ticket
        return context
    
    def dispatch(self, *args, **kwargs):
        self.ticket = Ticket.objects.get(id=self.kwargs['ticket_id'])
        return super().dispatch(*args, **kwargs)

    
# class ReviewCreateView(LoginRequiredMixin, View):
#     template_name = 'litrevu/ticket-review.html'
#     form_class = forms.ReviewForm

#     def get(self, request, ticket_id):
#         ticket = Ticket.objects.get(pk=ticket_id)
#         form = self.form_class()
#         return render(request, self.template_name, context={'form': form, 'ticket': ticket})

#     def post(self, request, ticket_id):
#         ticket = Ticket.objects.get(pk=ticket_id)
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.ticket = ticket
#             review.user = request.user
#             review.save()
#             return redirect('home')
#         return render(request, self.template_name, context={'form': form, 'ticket': ticket})


class CreateTicketAndReviewView(LoginRequiredMixin, CreateView):
    model = Ticket
    template_name = 'litrevu/create_ticket_and_review.html'
    form_class = forms.TicketForm
    review_form_class = forms.ReviewForm
    success_url = reverse_lazy('home') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = self.review_form_class()
        return context

    def form_valid(self, form):
        review_form = self.review_form_class(self.request.POST)
        self.object = form.save(commit=False)
        # usuário do ticket /  self.object.user = self.request.user  
        form.instance.user = self.request.user
        self.object.user = self.request.user  
        self.object.save()
        review = review_form.save(commit=False)
        review.ticket = self.object
        # usuário da crítica / review.user = self.request.user  
        review.user = self.request.user  
        review.save()
        return super().form_valid(form)

    

class UpdateTicketView(LoginRequiredMixin, UpdateView):
    model = Ticket 
    template_name = 'litrevu/update_ticket.html'
    form_class = forms.TicketForm
    success_url = reverse_lazy('home') 
    
    def get_object(self, queryset=None):
        ticket_id = self.kwargs.get('update_id')
        return Ticket.objects.get(id=ticket_id)


class DeleteTicketView(LoginRequiredMixin, DeleteView):
    model = Ticket
    template_name = 'litrevu/delete_ticket.html'
    form_class = forms.TicketForm
    success_url = reverse_lazy('home')