"""
URL configuration for codesren project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from posts.views import *
from users.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_view,name='home'),
    path('accounts/', include('allauth.urls')),
    path('category/<str:tag>/',home_view, name='category'),
    path('post/create-post/',post_create_view, name='post-create'),
    path('post/delete-post/<uuid:pk>/',post_delete_view, name='post-delete'),
    path('post/edit-post/<uuid:pk>/',post_edit_view, name='post-edit'),
    path('post/post-page/<uuid:pk>/',post_page_view, name='post-page'),
    path('post/post-page/like/<uuid:pk>',like_post, name='like-post'),
    path('post/post-page/like-comment/<uuid:pk>',like_comment, name='like-comment'),
    path('post/post-page/like-reply/<uuid:pk>',like_reply, name='like-reply'),
    path('profile/edit/', profile_edit_view, name='profile-edit'),
    path('profile/delete/', profile_delete_view, name='profile-delete'),
    path('profile/', profile_view, name='profile'),
    path('profile/<username>/', profile_view, name='userprofile'),
    path('profile-onboarding/', profile_edit_view, name='profile-onboarding'),
    path('comment/<uuid:pk>/sent',comment_sent,name='comment-sent'),
    path('comment/<uuid:pk>/delete',comment_delete_view,name='comment-delete'),
    path('reply/<uuid:pk>/sent',reply_sent,name='reply-sent'),
    path('reply/<uuid:pk>/delete',reply_delete_view,name='reply-delete'),
    
   
    
] 
urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
