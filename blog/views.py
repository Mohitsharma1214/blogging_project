from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login,logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Profile, Category, Post, Comment, Reply
from .forms import CommentForm, ReplyForm, PostForm , ProfileForm
import re
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Automatically log in the user after registration
            return redirect('user_home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('user_home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    # Redirect to a page after successfully logging out
    return redirect('index')  # Replace 'home' with the URL or name of your desired landing page

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('user_home')
    else:
        profile_form = ProfileForm(instance=profile)
    
    return render(request, 'profile.html', {'profile_form': profile_form})

@login_required
def user_home(request):
    posts = Post.objects.all()
    return render(request, 'user_home.html', {'posts': posts})

from django.shortcuts import render, redirect
from .forms import PostForm

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_home(request):
    if not request.user.is_superuser:
        return redirect('user_home')
    posts = Post.objects.all()
    post_form = PostForm()  # Create an instance of the PostForm
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('admin_home')
    return render(request, 'admin_home.html', {'posts': posts, 'post_form': post_form})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from .forms import CommentForm,ReplyForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, Reply
from .forms import CommentForm, ReplyForm

from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import CommentForm, ReplyForm

from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Reply
from .forms import CommentForm, ReplyForm

from django.shortcuts import get_object_or_404, redirect
from .models import Comment, Reply

from django.shortcuts import get_object_or_404, redirect, render
from .models import Post, Comment, Reply
from .forms import CommentForm, ReplyForm

from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, Reply
from .forms import CommentForm, ReplyForm
@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    image_url = post.image.url if post.image else None
    

    from bs4 import BeautifulSoup

# Extract text content from post.content while excluding images
    soup = BeautifulSoup(post.content, 'html.parser')

    # Extract image URLs and fix paths
    image_urls = [img['src'].replace('../media/uploads/', '/media/uploads/') for img in soup.find_all('img')]

    # Remove the images from the soup
    for img in soup.find_all('img'):
        img.decompose()

    # Get the remaining text
    text_content = soup.get_text(separator='\n', strip=True)

    # Create content items for text and images
    content_items = [
        {'type': 'text', 'content': text_content},
        *[{'type': 'image', 'url': url} for url in image_urls]
    ]

  
    comments = post.comments.all()
    comment_form = CommentForm()
    reply_form = ReplyForm()

    if request.method == 'POST':
        if 'comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.author = request.user
                new_comment.save()
                return redirect('post_detail', post_id=post_id)

        elif 'reply' in request.POST:
            reply_form = ReplyForm(request.POST)
            if reply_form.is_valid():
                parent_comment_id = request.POST.get('parent_comment_id')
                parent_comment = get_object_or_404(Comment, pk=parent_comment_id)
                new_reply = reply_form.save(commit=False)
                new_reply.comment = parent_comment
                new_reply.author = request.user
                new_reply.save()
                return redirect('post_detail', post_id=post_id)

        elif 'upvote_comment' in request.POST:
            comment_id = request.POST.get('upvote_comment')
            comment = get_object_or_404(Comment, pk=comment_id)
            comment.upvotes += 1
            comment.save()
            return redirect('post_detail', post_id=post_id)

        elif 'upvote_reply' in request.POST:
            reply_id = request.POST.get('upvote_reply')
            reply = get_object_or_404(Reply, pk=reply_id)
            reply.upvotes += 1
            reply.save()
            return redirect('post_detail', post_id=post_id)

        elif 'delete_comment' in request.POST:
            comment_id = request.POST.get('delete_comment')
            comment = get_object_or_404(Comment, pk=comment_id)
            if comment.author == request.user:
                comment.delete()
            return redirect('post_detail', post_id=post_id)

        elif 'delete_reply' in request.POST:
            reply_id = request.POST.get('delete_reply')
            reply = get_object_or_404(Reply, pk=reply_id)
            if reply.author == request.user:
                reply.delete()
            return redirect('post_detail', post_id=post_id)
        
        elif 'edit_comment' in request.POST:
            comment_id = request.POST.get('edit_comment')
            comment = get_object_or_404(Comment, pk=comment_id)
            if comment.author == request.user:
                comment.content = request.POST.get('edited_comment')
                comment.save()
            return redirect('post_detail', post_id=post_id)

        elif 'edit_reply' in request.POST:
            reply_id = request.POST.get('edit_reply')
            reply = get_object_or_404(Reply, pk=reply_id)
            if reply.author == request.user:
                reply.content = request.POST.get('edited_reply')
                reply.save()
            return redirect('post_detail', post_id=post_id)

    return render(request, 'post_detail.html', {'post': post, 'comments': comments,
                                               'comment_form': comment_form, 'content_items': content_items,'reply_form': reply_form,'image_url': image_url})


from django.shortcuts import redirect, get_object_or_404
from .models import Post, Comment
from .forms import CommentForm, ReplyForm

# View to add a comment to a post
from django.http import HttpResponseRedirect


# View to add a reply to a comment
from django.shortcuts import render, redirect, get_object_or_404
from .models import Comment, Reply
from .forms import ReplyForm



    # Render the form and comment details in the post_detail template
   
from django.shortcuts import render, redirect
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('admin_home')
    else:
        post_form = PostForm()
    return render(request, 'create_post.html', {'post_form': post_form})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES, instance=post)
        if post_form.is_valid():
            post_form.save()
            return redirect('admin_home')
    else:
        post_form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'post_form': post_form, 'post': post})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('admin_home')
    return render(request, 'delete_post.html', {'post': post})


    from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
from django.http import JsonResponse

from django.conf import settings
import os
from django.http import JsonResponse

from django.core.files.storage import default_storage
from django.conf import settings

from urllib.parse import urljoin

from urllib.parse import urljoin

from urllib.parse import urljoin
from django.conf import settings
import os
from django.http import JsonResponse

from django.http import JsonResponse
from django.conf import settings
from .models import Post

@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('file'):
        try:
            uploaded_image = request.FILES['file']
              
            # Define the path to save the uploaded image
            image_path = os.path.join(settings.MEDIA_ROOT, 'uploads', uploaded_image.name)

            # Save the uploaded image to the specified path
            with open(image_path, 'wb+') as destination:
                for chunk in uploaded_image.chunks():
                    destination.write(chunk)

            # Construct the URL for the uploaded image
            image_url = f"{settings.MEDIA_URL}uploads/{uploaded_image.name}"

            # Get the post instance (you'll need the post ID from the request or somewhere else)
           

            # Return the modified image URL in JSON format
            return JsonResponse({'location': image_url})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)
