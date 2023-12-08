from django.urls import path
from .views import user_login, user_register,home,view_profile
from .views import change_profile_picture,edit_profile,friend_requests, send_friend_request,search_friends, accept_friend_request, reject_friend_request
urlpatterns = [
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('login/', user_login, name='login'),
    path('register/', user_register, name='register'),
    path('', home, name='home'),
    path('profile/', view_profile, name='view_profile'),
    path('change_profile_picture/', change_profile_picture, name='change_profile_picture'),
    path('friend-requests/', friend_requests, name='friend_requests'),
    path('send-friend-request/<int:to_user_id>/', send_friend_request, name='send_friend_request'),
    path('accept-friend-request/<int:friend_request_id>/', accept_friend_request, name='accept_friend_request'),
    path('reject-friend-request/<int:friend_request_id>/', reject_friend_request, name='reject_friend_request'),
    path('search-friends/', search_friends, name='search_friends'),  # Add this line

]


















'''from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('register/', views.register, name='register'),
    # Add paths for comments if implemented
]
'''