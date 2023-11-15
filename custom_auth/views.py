from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from core.models import CustomUser

# View for handling user login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate user using provided username and password
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # If authentication is successful, log in the user and redirect to the home page
            login(request, user)
            return redirect('home')
        else:
            # If authentication fails, display an error message to the user
            messages.error(request, 'Invalid username or password. Please try again.')

    # Render the login form template
    return render(request, 'login.html')



# View for handling user registration
def register_view(request):
    if request.method == 'POST':
        # Check if the submitted registration form is valid
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # If the form is valid, save the new user and redirect to the login page
            form.save()
            return redirect('login')
    else:
        # If the request method is not POST, display the registration form
        form = UserCreationForm()
    # Render the registration form template with the form object
    return render(request, 'register.html', {'form': form})


# View for editing user profile information
@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        # Retrieve the updated profile information from the submitted form
        bio = request.POST['bio']
        pronouns = request.POST['pronouns']
        location = request.POST['location']
        
        # Retrieve the user object based on the current user's ID
        user = CustomUser.objects.get(pk=request.user.id)
        # Update the user's profile fields with the new information
        user.bio = bio
        user.pronouns = pronouns
        user.location = location
        # Save the updated user object
        user.save()

        # Redirect to the user's profile page after saving changes
        return redirect('profile')

    # Render the edit profile form template with the current user's information
    return render(request, 'edit_profile.html', {'user': request.user})
