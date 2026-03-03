"""
Serializers for Academic Admission System
Handles validation, state transitions, and frontend schema generation.
"""
from rest_framework import serializers
from django.utils import timezone
from .models import (
    Program, ProgramField, Admission, AdmissionState,
    AdmissionStateLog, AdmissionEvent, InternalNote,
    ContentPage, Achievement, GalleryItem, Enquiry, AnalyticEvent, Faculty
)


class ProgramFieldSerializer(serializers.ModelSerializer):
    """Serializer for dynamic form fields - frontend renders schema from this"""
    class Meta:
        model = ProgramField
        fields = [
            'id', 'step', 'field_key', 'label', 'field_type',
            'placeholder', 'help_text', 'required', 'validation_rules',
            'show_condition', 'choices', 'display_order', 'is_visible'
        ]


class ProgramSerializer(serializers.ModelSerializer):
    """Program serializer with embedded fields for schema generation"""
    fields = ProgramFieldSerializer(source='fields.filter(is_visible=True)', many=True)
    
    class Meta:
        model = Program
        fields = [
            'id', 'name', 'slug', 'description', 'min_age', 'max_age',
            'is_active', 'display_order', 'config', 'fields'
        ]


class ProgramSummarySerializer(serializers.ModelSerializer):
    """Lightweight program info for dropdowns and lists"""
    class Meta:
        model = Program
        fields = ['id', 'name', 'slug', 'min_age', 'max_age']


class AdmissionStateLogSerializer(serializers.ModelSerializer):
    """Serializer for admission state change history"""
    class Meta:
        model = AdmissionStateLog
        fields = [
            'id', 'old_state', 'new_state', 'action',
            'performed_by', 'details', 'created_at'
        ]


class InternalNoteSerializer(serializers.ModelSerializer):
    """Serializer for staff internal notes"""
    class Meta:
        model = InternalNote
        fields = ['id', 'author', 'content', 'created_at']


class AdmissionListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for admission lists"""
    program_name = serializers.CharField(source='program.name', read_only=True)
    
    class Meta:
        model = Admission
        fields = [
            'id', 'application_number', 'program', 'program_name',
            'state', 'current_step', 'name', 'phone', 'email',
            'created_at', 'submitted_at'
        ]


class AdmissionDetailSerializer(serializers.ModelSerializer):
    """Full admission details for admin view"""
    program_name = serializers.CharField(source='program.name', read_only=True)
    state_logs = AdmissionStateLogSerializer(many=True, read_only=True)
    notes = InternalNoteSerializer(many=True, read_only=True)
    age_verified = serializers.SerializerMethodField()
    
    class Meta:
        model = Admission
        fields = [
            'id', 'application_number', 'program', 'program_name', 'state',
            'current_step', 'completed_steps',
            
            # Personal
            'student_photo', 'photo_verified', 'name', 'dob', 'age_at_submission',
            'age_verified', 'phone', 'phone_country_code', 'email',
            'address_house_name', 'address_place', 'address_post_office',
            'address_pin_code', 'address_state', 'address_district',
            
            # Academic
            'madrassa_name', 'class_stopped', 'school_college', 'standard',
            'languages_known', 'languages_other', 'academic_data',
            'achievements_file', 'achievements_verified',
            
            # Guardian
            'guardian_name', 'guardian_relation', 'guardian_phone',
            'guardian_phone_country_code', 'guardian_email', 'guardian_occupation',
            
            # Tracking
            'completed_steps', 'time_spent_per_step', 'submitted_at',
            'draft_saved_at', 'internal_notes',
            
            # Related
            'state_logs', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['application_number', 'state', 'age_at_submission']
    
    def get_age_verified(self, obj):
        """Verify age calculation is correct"""
        if obj.dob:
            today = timezone.now().date()
            age = today.year - obj.dob.year
            if (today.month, today.day) < (obj.dob.month, obj.dob.day):
                age -= 1
            return age == obj.age_at_submission
        return None


class AdmissionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new admissions"""
    step = serializers.IntegerField(write_only=True, required=False, default=1)
    step_data = serializers.JSONField(write_only=True, required=False, default=dict)
    time_spent = serializers.IntegerField(write_only=True, required=False, default=0)
    
    class Meta:
        model = Admission
        fields = [
            'program', 'step', 'step_data', 'time_spent'
        ]
    
    def validate_program(self, value):
        """Ensure program is active"""
        if not value.is_active:
            raise serializers.ValidationError("This program is not currently accepting applications")
        return value
    
    def validate(self, attrs):
        """Validate admission creation"""
        program = attrs['program']
        step = attrs.get('step', 1)
        step_data = attrs.get('step_data', {})
        
        # For step 1, validate required fields
        if step == 1:
            required_fields = ['name', 'dob', 'phone', 'email']
            for field in required_fields:
                if field not in step_data:
                    raise serializers.ValidationError({
                        'step_data': f'{field} is required for step 1'
                    })
        
        return attrs
    
    def create(self, validated_data):
        """Create admission with step data"""
        step = validated_data.pop('step', 1)
        step_data = validated_data.pop('step_data', {})
        time_spent = validated_data.pop('time_spent', 0)
        
        admission = Admission.objects.create(**validated_data)
        
        # Complete first step
        admission.complete_step(step, step_data, time_spent)
        
        # Emit event
        AdmissionEvent.emit(admission, 'admission_created', {'step': step})
        
        return admission


class AdmissionStepSerializer(serializers.ModelSerializer):
    """
    Serializer for completing steps.
    Each step owns its fields - cannot modify previous steps.
    """
    step_data = serializers.JSONField(write_only=True)
    time_spent = serializers.IntegerField(write_only=True, required=False, default=0)
    
    class Meta:
        model = Admission
        fields = ['step_data', 'time_spent']
    
    def validate_step_data(self, value):
        """Validate step data based on current step"""
        step = self.instance.current_step
        
        if step == 1:
            required = ['name', 'dob', 'phone', 'email']
            for field in required:
                if field not in value:
                    raise serializers.ValidationError(f'{field} is required')
        
        elif step == 2:
            required = ['madrassa_name', 'class_stopped', 'standard']
            for field in required:
                if field not in value:
                    raise serializers.ValidationError(f'{field} is required')
        
        elif step == 3:
            required = ['guardian_name', 'guardian_relation', 'guardian_phone']
            for field in required:
                if field not in value:
                    raise serializers.ValidationError(f'{field} is required')
        
        return value
    
    def update(self, instance, validated_data):
        """Complete current step"""
        step_data = validated_data.pop('step_data', {})
        time_spent = validated_data.pop('time_spent', 0)
        
        instance.complete_step(instance.current_step, step_data, time_spent)
        
        # Emit event
        AdmissionEvent.emit(instance, 'step_completed', {
            'step': instance.current_step,
            'time_spent': time_spent
        })
        
        return instance


class AdmissionSubmitSerializer(serializers.Serializer):
    """
    Serializer for final submission.
    Validates all required data is present and age is valid.
    """
    def validate(self, attrs):
        """Validate admission can be submitted"""
        admission = self.instance
        
        # Check all steps completed
        if len(admission.completed_steps) < 3:
            raise serializers.ValidationError({
                'non_field_errors': 'All steps must be completed before submission'
            })
        
        # Validate age
        if admission.age_at_submission:
            min_age = admission.program.min_age
            max_age = admission.program.max_age
            if not (min_age <= admission.age_at_submission <= max_age):
                raise serializers.ValidationError({
                    'non_field_errors': f'Age must be between {min_age} and {max_age}'
                })
        
        # Validate email domain
        if admission.email and not admission.email.endswith('@gmail.com'):
            raise serializers.ValidationError({
                'email': 'Email must be a Gmail address'
            })
        
        return attrs
    
    def submit(self):
        """Submit the admission"""
        self.instance.submit()
        return self.instance


class StateTransitionSerializer(serializers.Serializer):
    """Serializer for admin state transitions"""
    new_state = serializers.ChoiceField(choices=AdmissionState.choices)
    reason = serializers.CharField(required=False, allow_blank=True)
    
    def validate_new_state(self, value):
        """Ensure transition is valid"""
        if not self.instance.can_transition_to(value):
            raise serializers.ValidationError(
                f'Cannot transition from {self.instance.state} to {value}'
            )
        return value
    
    def transition(self, admin_user=None):
        """Perform the state transition"""
        new_state = self.validated_data['new_state']
        reason = self.validated_data.get('reason', '')
        
        if new_state == AdmissionState.REJECTED and reason:
            self.instance.reject(reason)
        else:
            self.instance.transition_to(new_state, user=admin_user)
        
        return self.instance


class ContentPageSerializer(serializers.ModelSerializer):
    """Serializer for content pages"""
    class Meta:
        model = ContentPage
        fields = [
            'id', 'slug', 'title', 'is_published', 'version',
            'meta_title', 'meta_description', 'content_blocks',
            'visible_from', 'visible_until', 'created_at', 'updated_at'
        ]


class AchievementSerializer(serializers.ModelSerializer):
    """Serializer for achievements"""
    class Meta:
        model = Achievement
        fields = [
            'id', 'title', 'description', 'date', 'image',
            'is_visible', 'display_order', 'created_at'
        ]


class GalleryItemSerializer(serializers.ModelSerializer):
    """Serializer for gallery items"""
    class Meta:
        model = GalleryItem
        fields = [
            'id', 'title', 'image', 'caption', 'date_taken',
            'display_order', 'is_visible', 'created_at'
        ]


class EnquirySerializer(serializers.ModelSerializer):
    """Serializer for contact enquiries"""
    program_name = serializers.CharField(source='program_interest.name', read_only=True, allow_null=True)
    
    class Meta:
        model = Enquiry
        fields = [
            'id', 'name', 'email', 'phone', 'program_interest',
            'program_name', 'message', 'status', 'tagged_programs',
            'assigned_to', 'follow_up_notes', 'created_at', 'closed_at'
        ]
        read_only_fields = ['status', 'created_at']


class EnquiryStatusSerializer(serializers.Serializer):
    """Serializer for updating enquiry status"""
    status = serializers.ChoiceField(choices=Enquiry.STATUS_CHOICES)
    assigned_to = serializers.CharField(required=False, allow_blank=True)
    follow_up_notes = serializers.CharField(required=False, allow_blank=True)


class AdmissionAnalyticsSerializer(serializers.Serializer):
    """Serializer for admission analytics data"""
    total_admissions = serializers.IntegerField()
    state_distribution = serializers.DictField()
    program_distribution = serializers.DictField()
    avg_time_per_step = serializers.DictField()
    drop_off_rate = serializers.DictField()
    validation_failures = serializers.ListField()


class FacultySerializer(serializers.ModelSerializer):
    """Serializer for faculty members"""
    class Meta:
        model = Faculty
        fields = [
            'id', 'name', 'role', 'qualification', 'bio',
            'photo', 'display_order', 'is_active'
        ]
