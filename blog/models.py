from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    # Add more fields as needed for the user profile

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=100)
    # Add more fields as needed for the category

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = HTMLField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='post_images/', null=True)  # For post images
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    flagged = models.BooleanField(default=False)  # Flagging comments
    upvotes = models.PositiveIntegerField(default=0)  # Count of upvotes
    editable = models.BooleanField(default=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    flagged = models.BooleanField(default=False)  # Flagging replies
    upvotes = models.PositiveIntegerField(default=0)  # Count of upvotes
    editable = models.BooleanField(default=True)

    def __str__(self):
        return f"Reply by {self.author.username} on {self.comment.post.title}"
