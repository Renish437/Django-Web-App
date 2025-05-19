from django.shortcuts import render,get_object_or_404
from .forms import *
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Count
from posts.form import ReplyCreateForm
# Create your views here.



@login_required
def profile_view(request, username=None):
    # If username is provided, check if it matches the logged-in user
    if username and request.user.username != username:
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(Profile, user=user)
    else:
        # If no username, just fetch the logged-in user's profile
        profile = request.user.profile  # Profile is now created automatically by the signal
    
    posts = profile.user.posts.all()
    if request.htmx:
        if 'top-posts' in request.GET:
            posts = profile.user.posts.annotate(num_likes=Count('like')).filter(num_likes__gt=0).order_by('-num_likes')
            
        elif 'top-comments' in request.GET:
            comments = profile.user.comments.annotate(num_likes=Count('like')).filter(num_likes__gt=0).order_by('-num_likes')
            replyform = ReplyCreateForm()
            return render(request,'snippets/loop_profile_comments.html',{'comments':comments,'replyform':replyform})
        elif 'liked-posts' in request.GET:
            posts = profile.user.likedposts.order_by('-likedpost__created').filter(like__isnull=False).distinct()
            
        return render(request,'snippets/loop_profile_posts.html',{'posts':posts})
    context ={'profile': profile,'posts':posts}
    return render(request, 'users/profile.html',context)

@login_required
def profile_edit_view(request):
    form = ProfileForm(instance=request.user.profile)

    # Choose the template based on the path (do this early!)
    if request.path == reverse('profile-onboarding'):
        template = 'users/profile_onboarding.html'
    else:
        template = 'users/profile_edit.html'

    # If the form is submitted
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')

    return render(request, template, {'form': form})

@login_required
def profile_delete_view(request):
    user = request.user
    if request.method == 'POST':
        logout(request)
        user.delete()
        messages.success(request,'Account deleted successfully')
        return redirect('home')
    return render(request,'users/profile_delete.html')
