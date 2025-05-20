from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from django.shortcuts import get_object_or_404
# Create your views here.

@login_required
def inbox_view(request,conversation_id=None):
    
    my_conversations = Conversation.objects.filter(participants=request.user).order_by('-lastmessage_created')
    if conversation_id:
        conversation = get_object_or_404(Conversation,id=conversation_id)
    else:
        conversation = None
    
    context ={
        'conversation':conversation,
        'my_conversations':my_conversations
    }
    return render(request,'inbox/inbox.html',context)
