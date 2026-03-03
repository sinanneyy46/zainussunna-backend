"""
Admin Configuration for Academic Admission System
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    Program, ProgramField, Admission, AdmissionStateLog,
    AdmissionEvent, InternalNote, ContentPage,
    Achievement, GalleryItem, Enquiry, AnalyticEvent, Faculty
)


class ProgramFieldInline(admin.TabularInline):
    model = ProgramField
    extra = 1
    ordering = ['step', 'display_order']


class ProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'min_age', 'max_age', 'is_active', 'display_order']
    list_filter = ['is_active']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['display_order', 'name']
    inlines = [ProgramFieldInline]


admin.site.register(Program, ProgramAdmin)


class AdmissionStateLogInline(admin.TabularInline):
    model = AdmissionStateLog
    extra = 0
    readonly_fields = ['admission', 'old_state', 'new_state', 'action', 'performed_by', 'details', 'created_at']
    ordering = ['-created_at']
    can_delete = False


class InternalNoteInline(admin.TabularInline):
    model = InternalNote
    extra = 0
    readonly_fields = ['author', 'content', 'created_at']


@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = [
        'application_number', 'name', 'program_link',
        'state_badge', 'current_step', 'created_at'
    ]
    list_filter = ['state', 'program', 'current_step', 'created_at']
    search_fields = ['name', 'application_number', 'phone', 'email']
    readonly_fields = [
        'application_number', 'state', 'current_step',
        'completed_steps', 'time_spent_per_step',
        'age_at_submission', 'submitted_at', 'draft_saved_at',
        'created_at', 'updated_at'
    ]
    inlines = [AdmissionStateLogInline, InternalNoteInline]
    ordering = ['-created_at']
    
    fieldsets = (
        ('Application Info', {
            'fields': ('application_number', 'program', 'state', 'current_step')
        }),
        ('Personal Information', {
            'fields': (
                'student_photo', 'photo_verified', 'name', 'dob', 'age_at_submission',
                'phone', 'phone_country_code', 'email'
            )
        }),
        ('Address', {
            'fields': (
                'address_house_name', 'address_place', 'address_post_office',
                'address_pin_code', 'address_state', 'address_district'
            )
        }),
        ('Academic Details', {
            'fields': (
                'madrassa_name', 'class_stopped', 'school_college', 'standard',
                'languages_known', 'languages_other', 'academic_data',
                'achievements_file', 'achievements_verified'
            )
        }),
        ('Guardian Information', {
            'fields': (
                'guardian_name', 'guardian_relation', 'guardian_phone',
                'guardian_phone_country_code', 'guardian_email', 'guardian_occupation'
            )
        }),
        ('Tracking', {
            'fields': ('completed_steps', 'time_spent_per_step', 'submitted_at', 'draft_saved_at')
        }),
        ('Internal', {
            'fields': ('internal_notes',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_under_review', 'approve_admissions', 'reject_admissions']
    
    def program_link(self, obj):
        url = reverse('admin:core_program_change', args=[obj.program.id])
        return format_html('<a href="{}">{}</a>', url, obj.program.name)
    program_link.short_description = 'Program'
    
    def state_badge(self, obj):
        colors = {
            'draft': 'gray',
            'submitted': 'blue',
            'under_review': 'orange',
            'approved': 'green',
            'rejected': 'red',
        }
        color = colors.get(obj.state, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 4px;">{}</span>',
            color, obj.get_state_display()
        )
    state_badge.short_description = 'Status'
    
    def mark_under_review(self, request, queryset):
        updated = 0
        for admission in queryset.filter(state='submitted'):
            admission.start_review()
            updated += 1
        self.message_user(request, f'{updated} admissions marked as under review')
    mark_under_review.short_description = 'Mark as Under Review'
    
    def approve_admissions(self, request, queryset):
        updated = 0
        for admission in queryset.filter(state='under_review'):
            admission.approve()
            updated += 1
        self.message_user(request, f'{updated} admissions approved')
    approve_admissions.short_description = 'Approve Selected'
    
    def reject_admissions(self, request, queryset):
        updated = 0
        for admission in queryset.filter(state='under_review'):
            admission.reject('Rejected by admin')
            updated += 1
        self.message_user(request, f'{updated} admissions rejected')
    reject_admissions.short_description = 'Reject Selected'


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'status', 'program_interest', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['created_at', 'updated_at']
    
    actions = ['mark_contacted', 'close_enquiries']
    
    def mark_contacted(self, request, queryset):
        updated = queryset.update(status='contacted')
        self.message_user(request, f'{updated} enquiries marked as contacted')
    mark_contacted.short_description = 'Mark as Contacted'
    
    def close_enquiries(self, request, queryset):
        from django.utils import timezone
        updated = 0
        for enquiry in queryset.exclude(status='closed'):
            enquiry.status = 'closed'
            enquiry.closed_at = timezone.now()
            enquiry.save()
            updated += 1
        self.message_user(request, f'{updated} enquiries closed')
    close_enquiries.short_description = 'Close Selected'


@admin.register(ContentPage)
class ContentPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_published', 'version', 'created_at']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['version', 'created_at', 'updated_at']


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'is_visible', 'display_order', 'created_at']
    list_filter = ['is_visible', 'date']
    search_fields = ['title', 'description']
    ordering = ['-date', '-display_order']


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_preview', 'date_taken', 'is_visible', 'display_order']
    list_filter = ['is_visible', 'date_taken']
    search_fields = ['title', 'caption']
    ordering = ['-display_order']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 100px; height: auto; border-radius: 4px;" />',
                obj.image.url
            )
        return '-'
    image_preview.short_description = 'Preview'


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'qualification', 'is_active', 'display_order']
    list_filter = ['is_active', 'role']
    search_fields = ['name', 'role', 'qualification']
    ordering = ['display_order', 'name']

