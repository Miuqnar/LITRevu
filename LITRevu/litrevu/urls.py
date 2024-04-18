from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from LITRevu.litrevu.views import home, TicketCreateView, FollowUserView, UnfollowUserView, ReviewCreateView

urlpatterns = [
    path('home/', home, name='home'),
    path('create_ticket/', TicketCreateView.as_view(), name='create_ticket'),
    path('follower_user/', FollowUserView.as_view(), name='follower_user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow_user'),
    path('tickets/<int:ticket_id>/create_review/', ReviewCreateView.as_view(), name='create_review'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    