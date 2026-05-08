from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import datetime, time as dt_time

from .models import (
    Talk, Speaker, ScheduleSlot, Sponsor, JobPosting,
    HeroSlide, BlogPost, Program, CallForProposal,
    ConferenceInfo, GalleryPhoto, Meetup, Project, SponsorApplication,
)


def home(request):
    today = timezone.localdate()
    now = timezone.localtime()
    featured_talks = Talk.objects.filter(is_featured=True).select_related('speaker')[:3]
    sponsors = Sponsor.objects.all().order_by('tier')
    hero_slides = HeroSlide.objects.filter(is_active=True).order_by('order')[:4]
    latest_posts = BlogPost.objects.filter(is_published=True).order_by('-published_at', '-created_at')[:3]
    programs = Program.objects.filter(is_active=True).prefetch_related('proposals')[:3]
    gallery_photos = GalleryPhoto.objects.filter(is_active=True).order_by('order')[:6]
    if not gallery_photos.exists():
        gallery_photos = GalleryPhoto.objects.all().order_by('order')[:6]

    upcoming_meetups = Meetup.objects.filter(is_published=True, date__gte=today).order_by('date', 'time')[:3]
    if not upcoming_meetups.exists():
        upcoming_meetups = Meetup.objects.filter(date__gte=today).order_by('date', 'time')[:3]
    if not upcoming_meetups.exists():
        upcoming_meetups = Meetup.objects.filter(is_published=True).order_by('-date', '-time')[:3]
    next_meetup = upcoming_meetups.first()
    conf = ConferenceInfo.get()

    event_countdown_target = None
    event_countdown_active = False
    event_countdown_title = None
    event_countdown_detail = None

    if conf.start_date:
        event_start = timezone.make_aware(datetime.combine(conf.start_date, dt_time.min), timezone.get_current_timezone())
        event_end = None
        if conf.end_date:
            event_end = timezone.make_aware(datetime.combine(conf.end_date, dt_time.max), timezone.get_current_timezone())

        if now < event_start:
            event_countdown_target = event_start.isoformat()
            event_countdown_title = "Countdown to PyData Kampala"
            event_countdown_detail = conf.event_dates
        elif event_end and event_start <= now <= event_end:
            event_countdown_active = True
            event_countdown_title = "PyData Kampala is happening now"
            event_countdown_detail = conf.event_dates

    return render(request, 'conference/home.html', {
        'featured_talks': featured_talks,
        'sponsors': sponsors,
        'hero_slides': hero_slides,
        'latest_posts': latest_posts,
        'programs': programs,
        'conf': conf,
        'gallery_photos': gallery_photos,
        'upcoming_meetups': upcoming_meetups,
        'next_meetup': next_meetup,
        'event_countdown_target': event_countdown_target,
        'event_countdown_active': event_countdown_active,
        'event_countdown_title': event_countdown_title,
        'event_countdown_detail': event_countdown_detail,
    })


def talks(request):
    all_talks = Talk.objects.all().select_related('speaker').order_by('talk_type', 'title')
    return render(request, 'conference/talks.html', {'talks': all_talks})


def talk_detail(request, pk):
    talk = get_object_or_404(Talk, pk=pk)
    return render(request, 'conference/talk_detail.html', {'talk': talk})


def speakers(request):
    all_speakers = Speaker.objects.all().order_by('name')
    return render(request, 'conference/speakers.html', {'speakers': all_speakers})


def schedule(request):
    slots = ScheduleSlot.objects.all().select_related('talk', 'talk__speaker')
    days = {}
    for slot in slots:
        day = slot.date
        days.setdefault(day, []).append(slot)
    return render(request, 'conference/schedule.html', {'days': days})


def sponsors(request):
    all_sponsors = Sponsor.objects.all().order_by('tier', 'name')
    jobs = JobPosting.objects.all().select_related('sponsor').order_by('-posted_at')
    return render(request, 'conference/sponsors.html', {
        'sponsors': all_sponsors,
        'jobs': jobs,
    })


def conduct(request):
    return render(request, 'conference/conduct.html', {
        'positive_behaviours': [
            "Demonstrating empathy and kindness toward other people",
            "Being respectful of differing opinions, viewpoints, and experiences",
            "Giving and gracefully accepting constructive feedback",
            "Accepting responsibility and apologising to those affected by our mistakes",
            "Focusing on what is best not just for us as individuals, but for the overall community",
        ],
        'negative_behaviours': [
            "The use of sexualised language or imagery, and unwelcome sexual attention or advances",
            "Trolling, insulting or derogatory comments, and personal or political attacks",
            "Public or private harassment",
            "Publishing others' private information, such as a physical or email address, without their explicit permission",
            "Sustained disruption of talks or other events",
            "Other conduct which could reasonably be considered inappropriate in a professional setting",
        ],
        'consequences': [
            "A verbal or written warning",
            "Removal from the event without a refund",
            "Being banned from future PyData Kampala events",
            "Reporting the incident to NumFOCUS for further action",
        ],
    })


def about(request):
    return render(request, 'conference/about.html')


def blog(request):
    posts = BlogPost.objects.filter(is_published=True).order_by('-published_at', '-created_at')
    return render(request, 'conference/blog.html', {'posts': posts})


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    return render(request, 'conference/blog_detail.html', {'post': post})


def programs(request):
    all_programs = Program.objects.filter(is_active=True).prefetch_related('proposals')
    return render(request, 'conference/programs.html', {'programs': all_programs})


def program_detail(request, slug):
    program = get_object_or_404(Program.objects.prefetch_related('proposals'), slug=slug, is_active=True)
    return render(request, 'conference/program_detail.html', {'program': program})


def program_proposals(request, slug):
    program = get_object_or_404(Program, slug=slug, is_active=True)
    proposals = CallForProposal.objects.filter(program=program).order_by('-is_open', 'closes_at')
    return render(request, 'conference/program_proposals.html', {
        'program': program,
        'proposals': proposals,
    })


def meetups(request):
    today = timezone.localdate()
    upcoming = Meetup.objects.filter(is_published=True, date__gte=today).order_by('date', 'time')
    past = Meetup.objects.filter(is_published=True, date__lt=today).order_by('-date', '-time')
    return render(request, 'conference/meetups.html', {
        'upcoming': upcoming,
        'past': past,
    })


def meetup_detail(request, slug):
    meetup = get_object_or_404(Meetup, slug=slug, is_published=True)
    return render(request, 'conference/meetup_detail.html', {'meetup': meetup})


def projects(request):
    all_projects = Project.objects.filter(is_published=True)
    return render(request, 'conference/projects.html', {'projects': all_projects})


def sponsor_apply(request):
    from django import forms as django_forms

    class ApplicationForm(django_forms.ModelForm):
        class Meta:
            model = SponsorApplication
            fields = ['organisation', 'contact_name', 'email', 'website', 'tier_interest', 'message']

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'conference/sponsor_apply.html', {'form': ApplicationForm(), 'success': True})
    else:
        form = ApplicationForm()
    return render(request, 'conference/sponsor_apply.html', {'form': form})
