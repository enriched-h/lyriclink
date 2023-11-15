from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser, Post, Like, Comment, Relationship, Notification
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import JsonResponse
from .forms import PostForm, CommentForm



# User Profile Views
def profile_view(request, user_id):
    # Get the user object based on the provided user_id, or return a 404 error if the user does not exist
    user = get_object_or_404(CustomUser, pk=user_id)
    return render(request, 'profile.html', {'user': user})



# Post Views
@login_required
def create_post_view(request):
    # Handle POST request to create a new post or render the empty post creation form for GET request
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # If the form is valid, save the post with the current user as the author and redirect to the home page
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('core:news_feed_view')  # Redirect to the home page after creating a post
    else:
        # Render an empty form for creating a new post
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})



# View for displaying detailed information about a specific post
def post_detail_view(request, post_id):
    # Get the post object based on the provided post_id, or return a 404 error if the post does not exist
    post = get_object_or_404(Post, pk=post_id)
    # Get comments related to the post
    comments = Comment.objects.filter(post=post)
    return render(request, 'post_detail.html', {'post': post, 'comments': comments})


# Likes and Comments Views
@login_required
def like_post_view(request, post_id):
    # Get the post object based on the provided post_id, or return a 404 error if the post does not exist
    post = get_object_or_404(Post, pk=post_id)
    # Check if the user has already liked the post; if not, create a new Like object, else delete the existing Like
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return JsonResponse({'likes_count': post.likes.count()})



@login_required
def comment_post_view(request, post_id):
    # Get the post object based on the provided post_id, or return a 404 error if the post does not exist
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # If the form is valid, save the comment with the current user as the author and redirect to post detail page
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('core:post_detail', post_id=post_id)  # Redirect to the post detail page after commenting
    else:
        # Render an empty form for commenting on the post
        form = CommentForm()
    return render(request, 'comment_post.html', {'form': form, 'post': post})



# Follow/Followers System Views
@login_required
def follow_user_view(request, user_id):
    # Get the user object based on the provided user_id, or return a 404 error if the user does not exist
    user_to_follow = get_object_or_404(CustomUser, pk=user_id)
    # Check if a relationship already exists; if not, create a new Relationship object, else delete the existing one
    relationship, created = Relationship.objects.get_or_create(follower=request.user, following=user_to_follow)
    if not created:
        relationship.delete()
    return JsonResponse({'is_following': request.user.following.filter(pk=user_id).exists()})


@login_required
def friend_requests_view(request):
    # Get friend requests where the current user is the recipient and the request is not yet accepted
    friend_requests = Relationship.objects.filter(following=request.user, is_accepted=False)
    return render(request, 'friend_requests.html', {'friend_requests': friend_requests})


# News Feed Views
@login_required
def news_feed_view(request):
    # Get posts from users that the current user is following, ordered by created_at in descending order
    followed_users = request.user.following.all()
    posts = Post.objects.filter(user__in=followed_users).order_by('-created_at')
    return render(request, 'news_feed.html', {'posts': posts})


# Notifications Views
@login_required
def notifications_view(request):
    # Get unread notifications for the current user
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    return render(request, 'notifications.html', {'notifications': notifications})


# Search Functionality Views
def search_users_view(request):
    # Get the search query from the request parameters and filter users based on username containing the query
    query = request.GET.get('q')
    users = CustomUser.objects.filter(username__icontains=query)
    return render(request, 'search_users.html', {'users': users, 'query': query})


def search_posts_view(request):
    # Get the search query from the request parameters and filter posts based on content containing the query
    query = request.GET.get('q')
    posts = Post.objects.filter(content__icontains=query)
    return render(request, 'search_posts.html', {'posts': posts, 'query': query})


# Privacy Settings View
@login_required
def privacy_settings_view(request):
    if request.method == 'POST':
        # Handle privacy settings form submission and update user's privacy preferences in the database
        pass  # Placeholder for handling form submission, to be implemented as needed
    return render(request, 'privacy_settings.html')




def login_view(request):
    logout(request)  # Logout the user first
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('core:news_feed_view')
        else:
            messages.error(request, 'Invalid login credentials. Please try again.')
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})




def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Optionally, log the user in after registration
            # user = form.save()
            # login(request, user)
            return redirect('core:login')  # Redirect to the login page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'auth/register.html', {'form': form})

def edit_profile_view(request):
    if request.method == 'POST':
        bio = request.POST['bio']
        pronouns = request.POST['pronouns']
        location = request.POST['location']
        
        # Update the user's profile information
        user = CustomUser.objects.get(pk=request.user.id)
        user.bio = bio
        user.pronouns = pronouns
        user.location = location
        user.save()

        return redirect('core:profile')  # Redirect to the user's profile page after saving changes

    return render(request, 'auth/edit_profile.html', {'user': request.user})