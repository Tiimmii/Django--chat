from django.shortcuts import render
from django.views import generic, View
from .models import User, Thread
# Create your views here.

class Landing(generic.TemplateView):
    template_name = 'first.html'
    
class chat(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'threads'
    
    def get_queryset(self):
        qs = Thread.objects.by_user(user=self.request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
        return qs


