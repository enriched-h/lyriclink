from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [

  # User Profile URLs
    path('profile/<int:user_id>/', views.profile_view, name='profile'),
    
    # Post URLs
    path('posts/create/', views.create_post_view, name='create_post'),
    path('posts/<int:post_id>/', views.post_detail_view, name='post_detail'),

    # Likes and Comments URLs
    path('posts/<int:post_id>/like/', views.like_post_view, name='like_post'),
    path('posts/<int:post_id>/comment/', views.comment_post_view, name='comment_post'),

    # Follow/Followers System URLs
    path('users/<int:user_id>/follow/', views.follow_user_view, name='follow_user'),
    path('friend-requests/', views.friend_requests_view, name='friend_requests'),

    # News Feed URL
    path('news-feed/', views.news_feed_view, name='news_feed'),

    # Notifications URL
    path('notifications/', views.notifications_view, name='notifications'),

    # Search Functionality URLs
    path('search/users/', views.search_users_view, name='search_users'),
    path('search/posts/', views.search_posts_view, name='search_posts'),

    # Privacy Settings URL
    path('privacy-settings/', views.privacy_settings_view, name='privacy_settings'),

    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),

    # Edit Profile URL
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),
]
