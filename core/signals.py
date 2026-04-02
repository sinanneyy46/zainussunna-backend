"""
Django Signals for Academic Admission System
Handles automatic events, analytics tracking, and state transitions.
"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Admission, AdmissionEvent, AnalyticEvent, Enquiry, Student


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
        
        # Auto-create student when admission is approved
        if instance.state == 'approved' and old_state != 'approved':
            create_student_from_admission(instance)
    
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
        # Get program name safely - handle case where program might be a UUID or not loaded
        program_name = None
        if instance.program_id:
            try:
                program_name = instance.program.name
            except AttributeError:
                # If program is just an ID (not loaded), try to get it
                from .models import Program
                try:
                    program_name = Program.objects.get(pk=instance.program_id).name
                except Program.DoesNotExist:
                    program_name = None
        
        AnalyticEvent.objects.create(
            category='conversion',
            event_data={
                'event': 'submission',
                'program': program_name
            },
            admission=instance
        )


def create_student_from_admission(admission):
    """
    Automatically create a Student record when an Admission is approved.
    Copies all relevant data from the admission to the student record.
    """
    # Check if student already exists for this admission
    if hasattr(admission, 'student_record') and admission.student_record:
        print(f"Student already exists for admission {admission.application_number}")
        return admission.student_record
    
    # Generate batch name from program and current year
    current_year = timezone.now().year
    batch_name = f"{admission.program.name} {current_year}" if admission.program else f"Batch {current_year}"
    
    # Create student record from admission data
    student = Student.objects.create(
        admission=admission,
        name=admission.name,
        student_photo=admission.student_photo,
        dob=admission.dob,
        phone=admission.phone,
        phone_country_code=admission.phone_country_code,
        email=admission.email,
        address_house_name=admission.address_house_name,
        address_place=admission.address_place,
        address_post_office=admission.address_post_office,
        address_pin_code=admission.address_pin_code,
        address_state=admission.address_state,
        address_district=admission.address_district,
        guardian_name=admission.guardian_name,
        guardian_relation=admission.guardian_relation,
        guardian_phone=admission.guardian_phone,
        guardian_phone_country_code=admission.guardian_phone_country_code,
        guardian_email=admission.guardian_email,
        guardian_occupation=admission.guardian_occupation,
        program=admission.program,
        batch=batch_name,
        student_status='studying',
        languages_known=admission.languages_known or [],
        enrollment_date=timezone.now().date()
    )
    
    print(f"Auto-created student {student.student_number} from admission {admission.application_number}")
    return student


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

