from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.forms import ModelForm
from django import forms
from bs4 import BeautifulSoup
import requests
from django.contrib import messages
from .form import *
from django.contrib.auth.decorators import login_required
# Create your views here.

def home_view(request,tag=None):
    if tag:
        posts = Post.objects.filter(tags__slug=tag)
        tag = get_object_or_404(Tag,slug=tag)
    else:
        posts = Post.objects.all()
    
    categories = Tag.objects.all()
    context = {'posts':posts,'categories':categories,'tag':tag}
    
    return render(request,'posts/home.html',context)



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
  
    return render(request,'posts/post_page.html',{'post':post})

