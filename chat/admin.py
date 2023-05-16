from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from . models import User, Chatmessage, Thread
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Chatmessage)

class ChatMessage(admin.TabularInline):
    model = Chatmessage


class ThreadForm(forms.ModelForm):
    def clean(self):
        super(ThreadForm, self).clean()
        first_person = self.cleaned_data.get('first_person')
        second_person = self.cleaned_data.get('second_person')

        lk1 = Q(first_person=first_person) & Q(second_person=second_person)
        lk2 = Q(first_person=second_person) &  Q(second_person=first_person)
        lk = Q(lk1|lk2)

        qs = Thread.objects.filter(lk)
        if qs.exists:
            raise ValidationError(f'Thread btwn {first_person} & {second_person} already exists')
        

class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage]
    class Meta:
        model = Thread


admin.site.register(Thread, ThreadAdmin)
        