from django.contrib import admin

from .models import Speaker, Talk, ScheduleSlot, Sponsor, JobPosting


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
