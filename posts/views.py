from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.forms import ModelForm
from django import forms
from bs4 import BeautifulSoup
from django.db.models import Count
import requests
from django.contrib import messages
from .form import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
# Create your views here.

def home_view(request, tag=None):
    current_tag_object = None
    ORDERING_FIELD = '-created' # Assuming 'created_at' is the correct field in your Post model

    if tag:
        current_tag_object = get_object_or_404(Tag, slug=tag)
        posts_list = Post.objects.filter(tags=current_tag_object).distinct().order_by(ORDERING_FIELD)
    else:
        posts_list = Post.objects.all().order_by(ORDERING_FIELD)

    paginator = Paginator(posts_list, 3) # Show 3 posts per page
    page_number_str = request.GET.get('page', '1')

    try:
        requested_page_number = int(page_number_str)
        current_page_obj = paginator.page(requested_page_number)
    except (PageNotAnInteger, ValueError):
        requested_page_number = 1
        current_page_obj = paginator.page(1)
    except EmptyPage:
        if request.htmx and request.GET.get('page'):
            return HttpResponse('') # Stop infinite scroll for HTMX if page is empty
        # For a direct browser request to an out-of-range page,
        # deliver last page. Or an empty page, depending on preference.
        current_page_obj = paginator.page(paginator.num_pages) # Show last page

    # Determine if the initial loader should be shown (for home.html)
    # Condition:
    # 1. There is actually a next page.
    # OR
    # 2. It's the first page of a category view AND that first page is full.
    #    (This handles the case where a category has exactly `paginator.per_page` items)
    
    is_first_page = current_page_obj.number == 1
    is_category_page = current_tag_object is not None
    # Check if the current page object list is full
    is_current_page_full = len(current_page_obj.object_list) == paginator.per_page

    # This flag is for the initial page load (home.html)
    # It will show the loader if there's more, OR if it's page 1 of a category and it's full
    display_initial_loader = current_page_obj.has_next() or \
                             (is_category_page and is_first_page and is_current_page_full)

    context = {
        'posts': current_page_obj,
        'tag': current_tag_object,
        'page': current_page_obj.number, # Actual page number being served
        'has_next': current_page_obj.has_next(), # For loop_home_posts.html (strictly for next page)
        'display_initial_loader': display_initial_loader, # For home.html (optimistic loader)
    }

    if request.htmx and request.GET.get('page'): # Subsequent HTMX pagination requests
        return render(request, 'snippets/loop_home_posts.html', context)
    
    # Initial page load (home or category)
    return render(request, 'posts/home.html', context)



@login_required
def post_create_view(request):
    form = PostCreateForm(request.POST)
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            
            website = requests.get(form.data['url'])
            sourcecode = BeautifulSoup(website.text,'html.parser')
            find_image = sourcecode.select('meta[content^="https://live.staticflickr.com/"]')
            image = find_image[0]['content']
            post.image = image
            
            find_title = sourcecode.select('h1.photo-title')
            title = find_title[0].text.strip()
            post.title = title
            
            find_artist = sourcecode.select('a.owner-name')
            artist = find_artist[0].text.strip()
            post.artist = artist
            
            post.author = request.user
            
            post.save()
            form.save_m2m()
            messages.success(request,'Post created successfully')
            return redirect('home')
    return render(request,'posts/post_create.html',{'form':form})

@login_required
def post_delete_view(request,pk):
    
    # post = Post.objects.get(id=pk)
    post = get_object_or_404(Post,id=pk,author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request,'Post deleted successfully')
        return redirect('home')
    return render(request,'posts/post_delete.html',{'post':post})

@login_required
def post_edit_view(request,pk):
    # post = Post.objects.get(id=pk)
    post = get_object_or_404(Post,id=pk,author=request.user)
    form = PostEditForm(instance=post)
    if request.method == 'POST':
        form = PostEditForm(request.POST,instance=post)
        if form.is_valid():
            form.save()
            messages.success(request,'Post updated successfully')
            return redirect('home')
    context = {'post':post,'form':form}
    
    return render(request,'posts/post_edit.html',context)

def post_page_view(request,pk):
    # post = Post.objects.get(id=pk)
    post = get_object_or_404(Post,id=pk)
    commentform = CommentCreateForm()
    replyform = ReplyCreateForm()
   
    
    if request.htmx:
        if 'top' in request.GET:
            # comments = post.comments.filter(like__isnull=False).distinct()
            comments = post.comments.annotate(num_likes=Count('like')).filter(num_likes__gt=0).order_by('-num_likes')
        else:
            comments = post.comments.all()
        return render(request,'snippets/loop_postpage_comments.html',{'comments':comments,'replyform':replyform})
  
    
    context = {
        'post':post,
        'commentform':commentform,
        'replyform':replyform,
       
    }
  
    return render(request,'posts/post_page.html',context)

@login_required
def comment_sent(request,pk):
    post = get_object_or_404(Post,id=pk)
    commentform = CommentCreateForm(request.POST)
    if request.method == 'POST':
        commentform = CommentCreateForm(request.POST)
    if commentform.is_valid():
        comment = commentform.save(commit=False)
        comment.parent_post = post
        comment.author = request.user
        comment.save()
    replyform = ReplyCreateForm()
    
    context = {
        'comment':comment,
        'post':post,
        'replyform':replyform
    }
    
        # messages.success(request,'Comment sent successfully')
    return render(request,'snippets/add_comment.html',context)

@login_required
def comment_delete_view(request,pk):
    
    # post = Post.objects.get(id=pk)
    post = get_object_or_404(Comment,id=pk,author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request,'Comment deleted successfully')
        return redirect('post-page',post.parent_post.id)
    return render(request,'posts/comment_delete.html',{'comment':post})

@login_required
def reply_sent(request,pk):
    comment = get_object_or_404(Comment,id=pk)
   
    
    if request.method == 'POST':
            commentform = ReplyCreateForm(request.POST)
    if commentform.is_valid():
            reply = commentform.save(commit=False)
            reply.parent_comment = comment
            reply.author = request.user
            reply.save()
    replyform = ReplyCreateForm()
        # messages.success(request,'Reply sent successfully')
    context = {
            'reply':reply,
            'comment':comment,
            'replyform':replyform
        }
    return render(request,'snippets/add_reply.html',context)

@login_required
def reply_delete_view(request,pk):
    
    # post = Post.objects.get(id=pk)
    reply = get_object_or_404(Reply,id=pk,author=request.user)
    if request.method == 'POST':
        reply.delete()
        messages.success(request,'Reply deleted successfully')
        return redirect('post-page',reply.parent_comment.parent_post.id)
    return render(request,'posts/reply_delete.html',{'reply':reply})
def like_toggle(model):
   def inner_func(func):
        def wrapper(request,*args,**kwargs):
            post = get_object_or_404(model,id=kwargs.get('pk'))
            user_exist = post.like.filter(username=request.user.username).exists()
    
            if post.author != request.user:
                if user_exist:
                    post.like.remove(request.user)
                else:
                    post.like.add(request.user)
            return func(request,post)
            
            
        return wrapper
   return inner_func

 
@login_required
@like_toggle(Post)
def like_post(request,post):
    return render(request,'snippets/like.html',{'post':post})

@login_required
@like_toggle(Comment)
def like_comment(request,post):
    return render(request,'snippets/like_comment.html',{'comment':post})
@login_required
@like_toggle(Reply)
def like_reply(request,post):
    return render(request,'snippets/like_reply.html',{'reply':post})

    