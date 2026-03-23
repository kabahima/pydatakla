from django.shortcuts import render, get_object_or_404

from .models import Talk, Speaker, ScheduleSlot, Sponsor, JobPosting


def home(request):
    featured_talks = Talk.objects.filter(is_featured=True).select_related('speaker')[:3]
    sponsors = Sponsor.objects.all().order_by('tier')
    return render(request, 'conference/home.html', {
        'featured_talks': featured_talks,
        'sponsors': sponsors,
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
