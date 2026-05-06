from django.contrib import admin

from .models import (
    Speaker, Talk, ScheduleSlot, Sponsor, JobPosting,
    HeroSlide, BlogPost, Program, CallForProposal,
    ConferenceInfo, GalleryPhoto, Meetup, Project, SponsorApplication,
)


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'twitter', 'github')
    search_fields = ('name',)


@admin.register(Talk)
class TalkAdmin(admin.ModelAdmin):
    list_display = ('title', 'speaker', 'talk_type', 'is_featured')
    list_filter = ('talk_type', 'is_featured')
    search_fields = ('title', 'speaker__name')


@admin.register(ScheduleSlot)
class ScheduleSlotAdmin(admin.ModelAdmin):
    list_display = ('date', 'start_time', 'end_time', 'talk', 'room')
    list_filter = ('date',)


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('name', 'tier', 'website')
    list_filter = ('tier',)


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'sponsor', 'posted_at')


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_filter = ('is_active',)
    ordering = ('order',)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published', 'published_at')
    list_filter = ('is_published',)
    search_fields = ('title', 'excerpt', 'content')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'start_date', 'end_date')
    list_filter = ('is_active',)
    search_fields = ('title', 'summary', 'description')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(CallForProposal)
class CallForProposalAdmin(admin.ModelAdmin):
    list_display = ('title', 'program', 'is_open', 'closes_at')
    list_filter = ('is_open', 'program')
    search_fields = ('title', 'description', 'program__title')


@admin.register(ConferenceInfo)
class ConferenceInfoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not ConferenceInfo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'order', 'is_active')
    list_filter = ('is_active',)
    ordering = ('order',)


@admin.register(Meetup)
class MeetupAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'venue', 'is_published')
    list_filter = ('is_published',)
    search_fields = ('title', 'description', 'venue')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('date',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_featured', 'is_published', 'created_at')
    list_filter = ('is_featured', 'is_published')
    search_fields = ('title', 'description', 'tags')


@admin.register(SponsorApplication)
class SponsorApplicationAdmin(admin.ModelAdmin):
    list_display = ('organisation', 'contact_name', 'email', 'tier_interest', 'status', 'submitted_at')
    list_filter = ('status', 'tier_interest')
    search_fields = ('organisation', 'contact_name', 'email')
    readonly_fields = ('submitted_at',)
    ordering = ('-submitted_at',)
