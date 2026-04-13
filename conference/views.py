from django.shortcuts import render, get_object_or_404

from .models import (
    Talk,
    Speaker,
    ScheduleSlot,
    Sponsor,
    JobPosting,
    HeroSlide,
    BlogPost,
    Program,
    CallForProposal,
)


def home(request):
    featured_talks = Talk.objects.filter(is_featured=True).select_related('speaker')[:3]
    sponsors = Sponsor.objects.all().order_by('tier')
    hero_slides = HeroSlide.objects.filter(is_active=True).order_by('order')[:4]
    latest_posts = BlogPost.objects.filter(is_published=True).order_by('-published_at', '-created_at')[:3]
    programs = Program.objects.filter(is_active=True).prefetch_related('proposals')[:3]
    return render(request, 'conference/home.html', {
        'featured_talks': featured_talks,
        'sponsors': sponsors,
        'hero_slides': hero_slides,
        'latest_posts': latest_posts,
        'programs': programs,
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
    return render(request, 'conference/conduct.html')


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
