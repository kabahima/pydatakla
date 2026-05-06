from django.urls import path

from . import views

app_name = 'conference'

urlpatterns = [
    path('', views.home, name='home'),
    path('talks/', views.talks, name='talks'),
    path('talks/<int:pk>/', views.talk_detail, name='talk_detail'),
    path('programs/', views.programs, name='programs'),
    path('programs/<slug:slug>/', views.program_detail, name='program_detail'),
    path('programs/<slug:slug>/call-for-proposals/', views.program_proposals, name='program_proposals'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('speakers/', views.speakers, name='speakers'),
    path('schedule/', views.schedule, name='schedule'),
    path('sponsors/', views.sponsors, name='sponsors'),
    path('conduct/', views.conduct, name='conduct'),
    path('about/', views.about, name='about'),
    path('meetups/', views.meetups, name='meetups'),
    path('meetups/<slug:slug>/', views.meetup_detail, name='meetup_detail'),
    path('projects/', views.projects, name='projects'),
    path('become-a-sponsor/', views.sponsor_apply, name='sponsor_apply'),
]
