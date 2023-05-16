from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
# Create your models here.

class User(AbstractUser):
    pass

class ThreadManager(models.Manager):
    def by_user(self, **kwargs):
        user = kwargs.get('user')
        lookup = Q(first_person=user)|Q(second_person=user)
        qs = self.get_queryset().filter(lookup).distinct()
        return qs

class Thread(models.Model):
    first_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_first_person')
    second_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_second_person')

    objects = ThreadManager()
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['first_person', 'second_person']

class Chatmessage(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, null=True, blank=True, related_name='chatmessage_thread')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

