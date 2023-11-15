from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, User

# Custom User model extending AbstractUser
class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)  # User's biography
    pronouns = models.CharField(max_length=255, blank=True)  # User's preferred pronouns
    location = models.CharField(max_length=255, blank=True)  # User's location
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # User's profile picture

    # Add related_name to the groups and user_permissions fields
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)

    def __str__(self):
        return self.username  # Return the username as the string representation of the user object
    
    class Meta:
        permissions = [
            # Define custom permissions if needed
        ]




# Post model for user posts
class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # User who created the post
    content = models.TextField()  # Content of the post
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for post creation

    def __str__(self):
        return f'Post by {self.user.username}'  # Return a formatted string indicating the post's author


# Like model representing likes on posts
class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # User who liked the post
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # Post that is liked

    def __str__(self):
        return f'Like by {self.user.username}'  # Return a formatted string indicating the like's creator


# Comment model for user comments on posts
class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # User who made the comment
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # Post on which the comment is made
    content = models.TextField()  # Content of the comment
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)  # Parent comment if applicable
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for comment creation

    def __str__(self):
        return f'Comment by {self.user.username}'  # Return a formatted string indicating the comment's author


# Relationship model representing follower-following relationships between users
class Relationship(models.Model):
    follower = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE)  # User who is following
    following = models.ForeignKey(CustomUser, related_name='followers', on_delete=models.CASCADE)  # User who is being followed
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for relationship creation

    def __str__(self):
        return f'{self.follower.username} follows {self.following.username}'  # Return a formatted string indicating the relationship



# Define the Notification model, representing notifications for users
class Notification(models.Model):
    # Define a foreign key relationship with the built-in User model, indicating the user associated with the notification.
    # If the referenced user is deleted, also delete the associated notifications.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Define a field to store the message content of the notification (can be a text message, HTML content, etc.)
    message = models.TextField()
    
    # Define a boolean field indicating whether the notification has been read (default is set to False)
    is_read = models.BooleanField(default=False)
    
    # Define a field to store the timestamp when the notification was created. auto_now_add=True sets the value
    # to the current timestamp when a new notification instance is created.
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Define a human-readable representation of the notification, useful for debugging and administration purposes.
    def __str__(self):
        return self.message