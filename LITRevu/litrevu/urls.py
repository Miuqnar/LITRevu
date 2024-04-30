from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from LITRevu.litrevu.views import home, TicketCreateView, FollowUserView, \
    UnfollowUserView, ReviewCreateView, CreateTicketAndReviewView, UpdateTicketView, \
    DeleteTicketView

urlpatterns = [
    path('home/', home, name='home'),
    path('create_ticket/', TicketCreateView.as_view(), name='create_ticket'),
    path('follower_user/', FollowUserView.as_view(), name='follower_user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow_user'),
    path('ticket-review/<int:ticket_id>/', ReviewCreateView.as_view(), name='ticket-review'),
    path('create-review/', CreateTicketAndReviewView.as_view(), name='create_ticket_and_review'),
    path('update-ticket/<int:update_id>/', UpdateTicketView.as_view(), name='update-ticket'),
    path('delete-ticket/<int:pk>/', DeleteTicketView.as_view(), name='delete-ticket'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


