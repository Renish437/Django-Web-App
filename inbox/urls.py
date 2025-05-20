from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('',inbox_view,name='inbox'),
    path('c/<uuid:conversation_id>/',inbox_view,name='inbox')
]