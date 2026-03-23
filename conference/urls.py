from django.urls import path

from . import views

app_name = 'conference'

urlpatterns = [
    path('', views.home, name='home'),
    path('talks/', views.talks, name='talks'),
    path('talks/<int:pk>/', views.talk_detail, name='talk_detail'),
    path('speakers/', views.speakers, name='speakers'),
    path('schedule/', views.schedule, name='schedule'),
    path('sponsors/', views.sponsors, name='sponsors'),
    path('conduct/', views.conduct, name='conduct'),
    path('about/', views.about, name='about'),
]
