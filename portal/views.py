from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Count

from conference.models import (
    Speaker, Talk, ScheduleSlot, Sponsor, JobPosting,
    HeroSlide, BlogPost, Program, CallForProposal, ConferenceInfo,
    GalleryPhoto, Meetup, Project, SponsorApplication,
)
from .forms import (
    SpeakerForm, TalkForm, ScheduleSlotForm, SponsorForm, JobPostingForm,
    HeroSlideForm, BlogPostForm, ProgramForm, CallForProposalForm, ConferenceInfoForm,
    GalleryPhotoForm, MeetupForm, ProjectForm,
)

staff_required = user_passes_test(lambda u: u.is_staff, login_url='portal:login')


def portal_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('portal:dashboard')
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user and user.is_staff:
            login(request, user)
            return redirect(request.GET.get('next', 'portal:dashboard'))
        messages.error(request, 'Invalid credentials or insufficient permissions.')
    return render(request, 'portal/login.html')


def portal_logout(request):
    logout(request)
    return redirect('portal:login')


@login_required(login_url='portal:login')
@staff_required
def dashboard(request):
    stats = {
        'speakers': Speaker.objects.count(),
        'talks': Talk.objects.count(),
        'schedule_slots': ScheduleSlot.objects.count(),
        'sponsors': Sponsor.objects.count(),
        'jobs': JobPosting.objects.count(),
        'hero_slides': HeroSlide.objects.count(),
        'blog_posts': BlogPost.objects.count(),
        'published_posts': BlogPost.objects.filter(is_published=True).count(),
        'programs': Program.objects.count(),
        'proposals': CallForProposal.objects.count(),
        'meetups': Meetup.objects.count(),
        'projects': Project.objects.count(),
        'gallery': GalleryPhoto.objects.count(),
    }
    recent_posts = BlogPost.objects.order_by('-created_at')[:5]
    return render(request, 'portal/dashboard.html', {'stats': stats, 'recent_posts': recent_posts})


# ── Generic helpers ──────────────────────────────────────────────────────────

def _list_view(request, model, template, order_by=None):
    qs = model.objects.all()
    if order_by:
        qs = qs.order_by(*order_by)
    return render(request, template, {'objects': qs})


def _create_view(request, form_class, template, redirect_name):
    form = form_class(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Created successfully.')
        return redirect(redirect_name)
    return render(request, template, {'form': form, 'action': 'Create'})


def _edit_view(request, form_class, template, redirect_name, pk):
    obj = get_object_or_404(form_class.Meta.model, pk=pk)
    form = form_class(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Updated successfully.')
        return redirect(redirect_name)
    return render(request, template, {'form': form, 'action': 'Edit', 'object': obj})


def _delete_view(request, model, redirect_name, pk):
    obj = get_object_or_404(model, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Deleted successfully.')
        return redirect(redirect_name)
    return render(request, 'portal/confirm_delete.html', {'object': obj})


# ── Speakers ─────────────────────────────────────────────────────────────────

@login_required(login_url='portal:login')
@staff_required
def speaker_list(request):
    return _list_view(request, Speaker, 'portal/speakers.html', ['name'])

@login_required(login_url='portal:login')
@staff_required
def speaker_create(request):
    return _create_view(request, SpeakerForm, 'portal/form.html', 'portal:speaker_list')

@login_required(login_url='portal:login')
@staff_required
def speaker_edit(request, pk):
    return _edit_view(request, SpeakerForm, 'portal/form.html', 'portal:speaker_list', pk)

@login_required(login_url='portal:login')
@staff_required
def speaker_delete(request, pk):
    return _delete_view(request, Speaker, 'portal:speaker_list', pk)


# ── Talks ─────────────────────────────────────────────────────────────────────

@login_required(login_url='portal:login')
@staff_required
def talk_list(request):
    return _list_view(request, Talk, 'portal/talks.html', ['talk_type', 'title'])

@login_required(login_url='portal:login')
@staff_required
def talk_create(request):
    return _create_view(request, TalkForm, 'portal/form.html', 'portal:talk_list')

@login_required(login_url='portal:login')
@staff_required
def talk_edit(request, pk):
    return _edit_view(request, TalkForm, 'portal/form.html', 'portal:talk_list', pk)

@login_required(login_url='portal:login')
@staff_required
def talk_delete(request, pk):
    return _delete_view(request, Talk, 'portal:talk_list', pk)


# ── Schedule ──────────────────────────────────────────────────────────────────

@login_required(login_url='portal:login')
@staff_required
def slot_list(request):
    return _list_view(request, ScheduleSlot, 'portal/slots.html', ['date', 'start_time'])

@login_required(login_url='portal:login')
@staff_required
def slot_create(request):
    return _create_view(request, ScheduleSlotForm, 'portal/form.html', 'portal:slot_list')

@login_required(login_url='portal:login')
@staff_required
def slot_edit(request, pk):
    return _edit_view(request, ScheduleSlotForm, 'portal/form.html', 'portal:slot_list', pk)

@login_required(login_url='portal:login')
@staff_required
def slot_delete(request, pk):
    return _delete_view(request, ScheduleSlot, 'portal:slot_list', pk)


# ── Sponsors ──────────────────────────────────────────────────────────────────

@login_required(login_url='portal:login')
@staff_required
def sponsor_list(request):
    return _list_view(request, Sponsor, 'portal/sponsors.html', ['tier', 'name'])

@login_required(login_url='portal:login')
@staff_required
def sponsor_create(request):
    return _create_view(request, SponsorForm, 'portal/form.html', 'portal:sponsor_list')

@login_required(login_url='portal:login')
@staff_required
def sponsor_edit(request, pk):
    return _edit_view(request, SponsorForm, 'portal/form.html', 'portal:sponsor_list', pk)

@login_required(login_url='portal:login')
@staff_required
def sponsor_delete(request, pk):
    return _delete_view(request, Sponsor, 'portal:sponsor_list', pk)


# ── Jobs ──────────────────────────────────────────────────────────────────────

@login_required(login_url='portal:login')
@staff_required
def job_list(request):
    return _list_view(request, JobPosting, 'portal/jobs.html', ['-posted_at'])

@login_required(login_url='portal:login')
@staff_required
def job_create(request):
    return _create_view(request, JobPostingForm, 'portal/form.html', 'portal:job_list')

@login_required(login_url='portal:login')
@staff_required
def job_edit(request, pk):
    return _edit_view(request, JobPostingForm, 'portal/form.html', 'portal:job_list', pk)

@login_required(login_url='portal:login')
@staff_required
def job_delete(request, pk):
    return _delete_view(request, JobPosting, 'portal:job_list', pk)


# ── Hero Slides ───────────────────────────────────────────────────────────────

@login_required(login_url='portal:login')
@staff_required
def slide_list(request):
    return _list_view(request, HeroSlide, 'portal/slides.html', ['order'])

@login_required(login_url='portal:login')
@staff_required
def slide_create(request):
    return _create_view(request, HeroSlideForm, 'portal/form.html', 'portal:slide_list')

@login_required(login_url='portal:login')
@staff_required
def slide_edit(request, pk):
    return _edit_view(request, HeroSlideForm, 'portal/form.html', 'portal:slide_list', pk)

@login_required(login_url='portal:login')
@staff_required
def slide_delete(request, pk):
    return _delete_view(request, HeroSlide, 'portal:slide_list', pk)


# ── Blog Posts ────────────────────────────────────────────────────────────────

@login_required(login_url='portal:login')
@staff_required
def post_list(request):
    return _list_view(request, BlogPost, 'portal/posts.html', ['-created_at'])

@login_required(login_url='portal:login')
@staff_required
def post_create(request):
    return _create_view(request, BlogPostForm, 'portal/form.html', 'portal:post_list')

@login_required(login_url='portal:login')
@staff_required
def post_edit(request, pk):
    return _edit_view(request, BlogPostForm, 'portal/form.html', 'portal:post_list', pk)

@login_required(login_url='portal:login')
@staff_required
def post_delete(request, pk):
    return _delete_view(request, BlogPost, 'portal:post_list', pk)


# ── Programs ──────────────────────────────────────────────────────────────────

@login_required(login_url='portal:login')
@staff_required
def program_list(request):
    return _list_view(request, Program, 'portal/programs.html', ['title'])

@login_required(login_url='portal:login')
@staff_required
def program_create(request):
    return _create_view(request, ProgramForm, 'portal/form.html', 'portal:program_list')

@login_required(login_url='portal:login')
@staff_required
def program_edit(request, pk):
    return _edit_view(request, ProgramForm, 'portal/form.html', 'portal:program_list', pk)

@login_required(login_url='portal:login')
@staff_required
def program_delete(request, pk):
    return _delete_view(request, Program, 'portal:program_list', pk)


# ── Call for Proposals ────────────────────────────────────────────────────────

@login_required(login_url='portal:login')
@staff_required
def proposal_list(request):
    return _list_view(request, CallForProposal, 'portal/proposals.html', ['program__title'])

@login_required(login_url='portal:login')
@staff_required
def proposal_create(request):
    return _create_view(request, CallForProposalForm, 'portal/form.html', 'portal:proposal_list')

@login_required(login_url='portal:login')
@staff_required
def proposal_edit(request, pk):
    return _edit_view(request, CallForProposalForm, 'portal/form.html', 'portal:proposal_list', pk)

@login_required(login_url='portal:login')
@staff_required
def proposal_delete(request, pk):
    return _delete_view(request, CallForProposal, 'portal:proposal_list', pk)


# ── Conference Info ───────────────────────────────────────────────────────────

@login_required(login_url='portal:login')
@staff_required
def conference_info(request):
    obj = ConferenceInfo.get()
    form = ConferenceInfoForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, 'Conference info updated.')
        return redirect('portal:conference_info')
    return render(request, 'portal/conference_info.html', {'form': form})


# ── Gallery ───────────────────────────────────────────────────────────────────

@login_required(login_url='portal:login')
@staff_required
def gallery_list(request):
    return _list_view(request, GalleryPhoto, 'portal/gallery.html', ['order'])

@login_required(login_url='portal:login')
@staff_required
def gallery_create(request):
    return _create_view(request, GalleryPhotoForm, 'portal/form.html', 'portal:gallery_list')

@login_required(login_url='portal:login')
@staff_required
def gallery_edit(request, pk):
    return _edit_view(request, GalleryPhotoForm, 'portal/form.html', 'portal:gallery_list', pk)

@login_required(login_url='portal:login')
@staff_required
def gallery_delete(request, pk):
    return _delete_view(request, GalleryPhoto, 'portal:gallery_list', pk)


# ── Meetups ───────────────────────────────────────────────────────────────────

@login_required(login_url='portal:login')
@staff_required
def meetup_list(request):
    return _list_view(request, Meetup, 'portal/meetups.html', ['date', 'time'])

@login_required(login_url='portal:login')
@staff_required
def meetup_create(request):
    return _create_view(request, MeetupForm, 'portal/form.html', 'portal:meetup_list')

@login_required(login_url='portal:login')
@staff_required
def meetup_edit(request, pk):
    return _edit_view(request, MeetupForm, 'portal/form.html', 'portal:meetup_list', pk)

@login_required(login_url='portal:login')
@staff_required
def meetup_delete(request, pk):
    return _delete_view(request, Meetup, 'portal:meetup_list', pk)


# ── Projects ──────────────────────────────────────────────────────────────────

@login_required(login_url='portal:login')
@staff_required
def project_list(request):
    return _list_view(request, Project, 'portal/projects.html', ['-is_featured', '-created_at'])

@login_required(login_url='portal:login')
@staff_required
def project_create(request):
    return _create_view(request, ProjectForm, 'portal/form.html', 'portal:project_list')

@login_required(login_url='portal:login')
@staff_required
def project_edit(request, pk):
    return _edit_view(request, ProjectForm, 'portal/form.html', 'portal:project_list', pk)

@login_required(login_url='portal:login')
@staff_required
def project_delete(request, pk):
    return _delete_view(request, Project, 'portal:project_list', pk)


# ── Sponsor Applications ──────────────────────────────────────────────────────

@login_required(login_url='portal:login')
@staff_required
def sponsor_applications(request):
    from django.db.models import Q
    status_filter = request.GET.get('status', '')
    qs = SponsorApplication.objects.all()
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'portal/sponsor_applications.html', {
        'applications': qs,
        'status_filter': status_filter,
    })

@login_required(login_url='portal:login')
@staff_required
def sponsor_application_update(request, pk):
    app = get_object_or_404(SponsorApplication, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ('pending', 'approved', 'rejected'):
            app.status = new_status
            app.save()
            messages.success(request, f'Application marked as {new_status}.')
    return redirect('portal:sponsor_applications')
