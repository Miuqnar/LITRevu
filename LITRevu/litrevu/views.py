from django.http import Http404
from django.shortcuts import redirect, render
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.db.models import Q
from django.db.models import CharField, Value
from itertools import chain
from django.shortcuts import get_object_or_404

from LITRevu.litrevu import forms, models
from LITRevu.litrevu.models import Ticket, UserFollows


@login_required
def page_post(request):
    tickets = models.Ticket.objects.filter(user=request.user)
    return render(request, 'litrevu/page_post.html', context={'tickets': tickets})


@login_required
def feed(request):
    followed_user_ids = request.user.following.values_list('followed_user', flat=True)

    reviews = models.Review.objects.filter(user__in=followed_user_ids)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = models.Ticket.objects.filter(user__in=followed_user_ids)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )

    # Renderiza o template com os posts paginados
    return render(request, 'litrevu/feed.html', {'posts': posts})


class TicketCreateView(LoginRequiredMixin, CreateView):
    template_name = 'litrevu/create_ticket.html'
    form_class = forms.TicketForm
    success_url = reverse_lazy('feed')

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
    success_url = reverse_lazy('feed')

    def form_valid(self, form):
        form.instance.ticket = self.ticket
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtém todas as revisões que o usuário pode visualizar
        user_reviews = models.Review.objects.filter(
            Q(user=self.request.user) |
            Q(ticket__user=self.request.user) |
            Q(user__in=UserFollows.objects.filter(followed_user=self.request.user).values('user'))
            # Q(user__followed_by=self.request.user)   
        )

        context['reviews'] = user_reviews
        context['ticket'] = self.ticket
        context['stars'] = range(1, 6)
        print("Stars:", context['stars']) 
        return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # context['ticket'] = self.ticket
    #     # return context

    def dispatch(self, *args, **kwargs):
        self.ticket = Ticket.objects.get(id=self.kwargs['ticket_id'])
        return super().dispatch(*args, **kwargs)


class CreateTicketAndReviewView(LoginRequiredMixin, CreateView):
    model = Ticket
    template_name = 'litrevu/create_ticket_and_review.html'
    form_class = forms.TicketForm
    review_form_class = forms.ReviewForm
    success_url = reverse_lazy('feed')

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
    success_url = reverse_lazy('feed')

    def get_object(self, queryset=None):
        ticket_id = self.kwargs.get('update_id')
        return get_object_or_404(Ticket, id=ticket_id, user=self.request.user)

# FIXME: class DeleteTicketView nao funciona
class DeleteTicketView(LoginRequiredMixin, DeleteView):
    model = Ticket
    template_name = 'litrevu/delete_ticket.html'
    form_class = forms.TicketForm
    success_url = reverse_lazy('feed')

    # def get_object(self, queryset=None):
    #     obj = super().get_object(queryset)
    #     if obj.user != self.request.user:
    #         raise Http404
    #     return obj

    # def dispatch(self, request, *args, **kwargs):
    #     # Verificar se o usuário tem permissão para deletar o ticket
    #     ticket_id = kwargs.get('pk')
    #     ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)

    #     # Se o usuário não for o proprietário do ticket, retorne um erro 404
    #     if ticket.user != request.user:
    #         raise Http404
    #     return super().dispatch(request, *args, **kwargs)
