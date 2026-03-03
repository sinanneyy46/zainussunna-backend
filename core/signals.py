"""
Django Signals for Academic Admission System
Handles automatic events, analytics tracking, and state transitions.
"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Admission, AdmissionEvent, AnalyticEvent, Enquiry


@receiver(pre_save, sender=Admission)
def admission_pre_save(sender, instance, **kwargs):
    """Track state changes for events"""
    if instance.pk:
        try:
            old_instance = Admission.objects.get(pk=instance.pk)
            instance._old_state = old_instance.state
            instance._old_step = old_instance.current_step
        except Admission.DoesNotExist:
            instance._old_state = None
            instance._old_step = 1
    else:
        instance._old_state = None
        instance._old_step = 1


@receiver(post_save, sender=Admission)
def admission_post_save(sender, instance, created, **kwargs):
    """Create events on state changes and track analytics"""
    old_state = getattr(instance, '_old_state', None)
    
    # State transition detected
    if old_state and old_state != instance.state:
        # Emit state change event
        AdmissionEvent.emit(
            instance,
            'state_changed',
            {
                'old_state': old_state,
                'new_state': instance.state,
                'transition_time': (instance.updated_at - instance.created_at).total_seconds()
            }
        )
        
        # Track analytics
        AnalyticEvent.objects.create(
            category='conversion',
            event_data={
                'from_state': old_state,
                'to_state': instance.state,
                'admission_id': str(instance.id)
            },
            admission=instance
        )
    
    # Step completed (but state not changed)
    elif not created and old_state == instance.state == 'draft':
        old_step = getattr(instance, '_old_step', None)
        if old_step and old_step != instance.current_step:
            AdmissionEvent.emit(
                instance,
                'step_completed',
                {
                    'completed_step': instance.current_step,
                    'total_completed': len(instance.completed_steps)
                }
            )
    
    # Submission tracking
    if created or (old_state == 'draft' and instance.state == 'submitted'):
        AnalyticEvent.objects.create(
            category='conversion',
            event_data={
                'event': 'submission',
                'program': instance.program.name if instance.program else None
            },
            admission=instance
        )


@receiver(pre_save, sender=Enquiry)
def enquiry_pre_save(sender, instance, **kwargs):
    """Track enquiry status changes"""
    if instance.pk:
        try:
            old_instance = Enquiry.objects.get(pk=instance.pk)
            instance._old_status = old_instance.status
        except Enquiry.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None


@receiver(post_save, sender=Enquiry)
def enquiry_post_save(sender, instance, created, **kwargs):
    """Track enquiry conversions"""
    old_status = getattr(instance, '_old_status', None)
    
    if not created and old_status and old_status != instance.status:
        AnalyticEvent.objects.create(
            category='conversion',
            event_data={
                'event': 'enquiry_status_change',
                'from_status': old_status,
                'to_status': instance.status
            }
        )
    
    # New enquiry from admission
    if created and instance.tagged_programs:
        AnalyticEvent.objects.create(
            category='program_demand',
            event_data={
                'programs': instance.tagged_programs,
                'source': 'admission_enquiry'
            }
        )


@receiver(post_save, sender=AdmissionEvent)
def process_event(sender, instance, created, **kwargs):
    """
    Process events asynchronously.
    In production, this would trigger emails, SMS, webhooks, etc.
    """
    if created and not instance.is_processed:
        # Mark as processed (in production, use Celery/Redis Queue)
        # For now, just log the event
        print(f"Event processed: {instance.event_type} for {instance.admission.application_number}")
        
        # TODO: Add actual processing:
        # - Send email notifications on approval/rejection
        # - Send SMS reminders
        # - Trigger webhook to admin Slack/Discord
        # - Update real-time dashboards
        
        instance.is_processed = True
        instance.processed_at = timezone.now()
        instance.save(update_fields=['is_processed', 'processed_at'])

