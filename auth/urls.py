from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    # Other URL patterns for your app...
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),
]
