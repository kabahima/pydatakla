from django.urls import path
from . import views

app_name = 'portal'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.portal_login, name='login'),
    path('logout/', views.portal_logout, name='logout'),

    # Speakers
    path('speakers/', views.speaker_list, name='speaker_list'),
    path('speakers/new/', views.speaker_create, name='speaker_create'),
    path('speakers/<int:pk>/edit/', views.speaker_edit, name='speaker_edit'),
    path('speakers/<int:pk>/delete/', views.speaker_delete, name='speaker_delete'),

    # Talks
    path('talks/', views.talk_list, name='talk_list'),
    path('talks/new/', views.talk_create, name='talk_create'),
    path('talks/<int:pk>/edit/', views.talk_edit, name='talk_edit'),
    path('talks/<int:pk>/delete/', views.talk_delete, name='talk_delete'),

    # Schedule
    path('schedule/', views.slot_list, name='slot_list'),
    path('schedule/new/', views.slot_create, name='slot_create'),
    path('schedule/<int:pk>/edit/', views.slot_edit, name='slot_edit'),
    path('schedule/<int:pk>/delete/', views.slot_delete, name='slot_delete'),

    # Sponsors
    path('sponsors/', views.sponsor_list, name='sponsor_list'),
    path('sponsors/new/', views.sponsor_create, name='sponsor_create'),
    path('sponsors/<int:pk>/edit/', views.sponsor_edit, name='sponsor_edit'),
    path('sponsors/<int:pk>/delete/', views.sponsor_delete, name='sponsor_delete'),

    # Jobs
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/new/', views.job_create, name='job_create'),
    path('jobs/<int:pk>/edit/', views.job_edit, name='job_edit'),
    path('jobs/<int:pk>/delete/', views.job_delete, name='job_delete'),

    # Hero Slides
    path('slides/', views.slide_list, name='slide_list'),
    path('slides/new/', views.slide_create, name='slide_create'),
    path('slides/<int:pk>/edit/', views.slide_edit, name='slide_edit'),
    path('slides/<int:pk>/delete/', views.slide_delete, name='slide_delete'),

    # Blog Posts
    path('posts/', views.post_list, name='post_list'),
    path('posts/new/', views.post_create, name='post_create'),
    path('posts/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('posts/<int:pk>/delete/', views.post_delete, name='post_delete'),

    # Programs
    path('programs/', views.program_list, name='program_list'),
    path('programs/new/', views.program_create, name='program_create'),
    path('programs/<int:pk>/edit/', views.program_edit, name='program_edit'),
    path('programs/<int:pk>/delete/', views.program_delete, name='program_delete'),

    # Proposals
    path('proposals/', views.proposal_list, name='proposal_list'),
    path('proposals/new/', views.proposal_create, name='proposal_create'),
    path('proposals/<int:pk>/edit/', views.proposal_edit, name='proposal_edit'),
    path('proposals/<int:pk>/delete/', views.proposal_delete, name='proposal_delete'),

    # Conference Info
    path('conference-info/', views.conference_info, name='conference_info'),

    # Gallery
    path('gallery/', views.gallery_list, name='gallery_list'),
    path('gallery/new/', views.gallery_create, name='gallery_create'),
    path('gallery/<int:pk>/edit/', views.gallery_edit, name='gallery_edit'),
    path('gallery/<int:pk>/delete/', views.gallery_delete, name='gallery_delete'),

    # Meetups
    path('meetups/', views.meetup_list, name='meetup_list'),
    path('meetups/new/', views.meetup_create, name='meetup_create'),
    path('meetups/<int:pk>/edit/', views.meetup_edit, name='meetup_edit'),
    path('meetups/<int:pk>/delete/', views.meetup_delete, name='meetup_delete'),

    # Projects
    path('projects/', views.project_list, name='project_list'),
    path('projects/new/', views.project_create, name='project_create'),
    path('projects/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('projects/<int:pk>/delete/', views.project_delete, name='project_delete'),

    # Sponsor Applications
    path('sponsor-applications/', views.sponsor_applications, name='sponsor_applications'),
    path('sponsor-applications/<int:pk>/update/', views.sponsor_application_update, name='sponsor_application_update'),

    # Shop
    path('products/', views.product_list, name='product_list'),
    path('categories/', views.category_list, name='category_list'),
    path('products/new/', views.product_create, name='product_create'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('categories/new/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    path('orders/', views.order_list, name='order_list'),
]
