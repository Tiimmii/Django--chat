from django.urls import path
from . import views

urlpatterns = [
    path('', views.Landing.as_view()),
    path('chat/', views.chat.as_view(), name='user')
]