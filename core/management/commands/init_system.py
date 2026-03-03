"""
Management command to initialize the admission system with sample data.
Run: python manage.py init_system
"""
from django.core.management.base import BaseCommand
from core.models import Program, ProgramField, ContentPage, Achievement, GalleryItem


class Command(BaseCommand):
    help = 'Initialize Zainussunna Academy with sample programs and content'

    def handle(self, *args, **options):
        self.stdout.write('Initializing Zainussunna Academy Backend...\n')
        
        # Create Programs
        self.create_programs()
        
        # Create Content Pages
        self.create_content_pages()
        
        # Create Sample Achievements
        self.create_achievements()
        
        self.stdout.write(self.style.SUCCESS('\n✓ System initialized successfully!'))

    def create_programs(self):
        self.stdout.write('Creating Programs...')
        
        # Integrated Sharee'a Program
        shareea, created = Program.objects.get_or_create(
            slug='shareea',
            defaults={
                'name': 'Integrated Sharee\'a',
                'description': 'Comprehensive Islamic studies program combining Sharee\'a with modern education',
                'min_age': 10,
                'max_age': 18,
                'display_order': 1,
                'config': {
                    'duration': '4 years',
                    'qualification': 'Higher Secondary',
                    'features': ['Arabic fluency', 'Quran memorization', 'Islamic jurisprudence']
                }
            }
        )
        
        if created:
            self.create_shareea_fields(shareea)
            self.stdout.write(f'  ✓ Created program: {shareea.name}')
        else:
            self.stdout.write(f'  ✓ Program exists: {shareea.name}')

        # Thahfīẓ-ul-Qur'an Program
        thahfeez, created = Program.objects.get_or_create(
            slug='thahfeez',
            defaults={
                'name': 'Thahfīẓ-ul-Qur\'an',
                'description': 'Complete Quran memorization program with Tajweed rules',
                'min_age': 9,
                'max_age': 18,
                'display_order': 2,
                'config': {
                    'duration': '3-5 years',
                    'qualification': 'Hifz Certificate',
                    'features': ['Tajweed rules', 'Memorization techniques', 'Review sessions']
                }
            }
        )
        
        if created:
            self.create_thahfeez_fields(thahfeez)
            self.stdout.write(f'  ✓ Created program: {thahfeez.name}')
        else:
            self.stdout.write(f'  ✓ Program exists: {thahfeez.name}')

    def create_shareea_fields(self, program):
        """Create form fields for Sharee'a program"""
        fields = [
            # Step 1: Personal
            (1, 'student_photo', 'Student Photo', 'file', 'required'),
            (1, 'name', 'Full Name', 'text', 'required'),
            (1, 'dob', 'Date of Birth', 'date', 'required'),
            (1, 'phone', 'Phone Number', 'phone', 'required'),
            (1, 'email', 'Email Address', 'email', 'required'),
            (1, 'address_house_name', 'House Name', 'text', 'required'),
            (1, 'address_place', 'Place', 'text', 'required'),
            (1, 'address_post_office', 'Post Office', 'text', 'required'),
            (1, 'address_pin_code', 'PIN Code', 'text', 'required'),
            (1, 'address_state', 'State', 'text', 'required'),
            (1, 'address_district', 'District', 'text', 'required'),
            
            # Step 2: Academic
            (2, 'school_college', 'School/College Name', 'text', 'required'),
            (2, 'standard', 'Current Class', 'text', 'required'),
            (2, 'madrassa_name', 'Madrassa/Dars Currently Attending', 'text', 'optional'),
            (2, 'arabic_fluent', 'Are you fluent in Arabic?', 'checkbox', 'required'),
            (2, 'previous_quran', 'How much Quran have you memorized?', 'select', 'required'),
            (2, 'languages_known', 'Languages Known', 'multiselect', 'required'),
            (2, 'previous_institution', 'Previous Islamic Institution (if any)', 'textarea', 'optional'),
            
            # Step 3: Guardian
            (3, 'guardian_name', 'Guardian Name', 'text', 'required'),
            (3, 'guardian_relation', 'Relationship', 'select', 'required'),
            (3, 'guardian_phone', 'Guardian Phone', 'phone', 'required'),
            (3, 'guardian_email', 'Guardian Email', 'email', 'optional'),
            (3, 'guardian_occupation', 'Guardian Occupation', 'text', 'optional'),
        ]
        
        self.save_fields(program, fields)

    def create_thahfeez_fields(self, program):
        """Create form fields for Thahfīẓ program"""
        fields = [
            # Step 1: Personal
            (1, 'student_photo', 'Student Photo', 'file', 'required'),
            (1, 'name', 'Full Name', 'text', 'required'),
            (1, 'dob', 'Date of Birth', 'date', 'required'),
            (1, 'phone', 'Phone Number', 'phone', 'required'),
            (1, 'email', 'Email Address', 'email', 'required'),
            (1, 'address_house_name', 'House Name', 'text', 'required'),
            (1, 'address_place', 'Place', 'text', 'required'),
            (1, 'address_post_office', 'Post Office', 'text', 'required'),
            (1, 'address_pin_code', 'PIN Code', 'text', 'required'),
            (1, 'address_state', 'State', 'text', 'required'),
            (1, 'address_district', 'District', 'text', 'required'),
            
            # Step 2: Academic (Thahfīẓ specific)
            (2, 'madrassa_name', 'Current Madrassa', 'text', 'required'),
            (2, 'hifz_started', 'When did you start Hifz?', 'date', 'required'),
            (2, 'parts_memorized', 'Parts of Quran Memorized', 'number', 'required'),
            (2, 'tajweed_known', 'Do you know Tajweed rules?', 'checkbox', 'required'),
            (2, 'recitation_ability', 'Current Recitation Ability', 'select', 'required'),
            (2, 'memorization_speed', 'Approximate memorization speed (pages/month)', 'number', 'optional'),
            (2, 'has_mishap', 'Have you had any memorization gaps?', 'checkbox', 'optional'),
            (2, 'languages_known', 'Languages Known', 'multiselect', 'required'),
            
            # Step 3: Guardian
            (3, 'guardian_name', 'Guardian Name', 'text', 'required'),
            (3, 'guardian_relation', 'Relationship', 'select', 'required'),
            (3, 'guardian_phone', 'Guardian Phone', 'phone', 'required'),
            (3, 'guardian_email', 'Guardian Email', 'email', 'optional'),
            (3, 'guardian_occupation', 'Guardian Occupation', 'text', 'optional'),
            (3, 'supporting_hifz', 'Will you support the student\'s Hifz journey?', 'checkbox', 'required'),
        ]
        
        self.save_fields(program, fields)

    def save_fields(self, program, field_defs):
        field_type_map = {
            'text': 'text',
            'textarea': 'textarea',
            'date': 'date',
            'phone': 'phone',
            'email': 'email',
            'number': 'number',
            'file': 'file',
            'checkbox': 'checkbox',
            'select': 'select',
            'multiselect': 'multiselect',
        }
        
        choices_map = {
            'Relationship': ['Father', 'Mother', 'Brother', 'Sister', 'Uncle', 'Aunt', 'Other'],
            'Current Recitation Ability': ['Beginner', 'Intermediate', 'Advanced', 'Expert'],
            'How much Quran have you memorized?': ['None', '1-5 parts', '5-10 parts', '10-15 parts', '15+ parts'],
            'Languages Known': ['Arabic', 'English', 'Malayalam', 'Hindi', 'Urdu', 'Tamil', 'Other'],
        }
        
        for order, key, label, ftype, required in field_defs:
            required_map = {'required': 'required', 'optional': 'optional', 'conditional': 'conditional'}
            
            choices = choices_map.get(label, [])
            if ftype not in ['select', 'multiselect']:
                choices = []
            
            ProgramField.objects.get_or_create(
                program=program,
                field_key=key,
                defaults={
                    'step': order,
                    'label': label,
                    'field_type': field_type_map.get(ftype, 'text'),
                    'placeholder': f'Enter {label.lower()}',
                    'required': required_map.get(required, 'optional'),
                    'choices': choices,
                    'display_order': order,
                    'is_visible': True
                }
            )

    def create_content_pages(self):
        self.stdout.write('Creating Content Pages...')
        
        pages = [
            {
                'slug': 'about',
                'title': 'About Zainussunna Academy',
                'is_published': True,
                'content_blocks': [
                    {'type': 'text', 'order': 1, 'data': {'content': '<h1>About Us</h1><p>Zainussunna Academy is a premier Islamic educational institution dedicated to nurturing future scholars and leaders through comprehensive Islamic and modern education.</p>'}},
                    {'type': 'text', 'order': 2, 'data': {'content': '<h2>Our Mission</h2><p>To produce pious, knowledgeable, and responsible individuals who can serve humanity with Islamic values and modern expertise.</p>'}},
                ]
            },
            {
                'slug': 'programs',
                'title': 'Our Programs',
                'is_published': True,
                'content_blocks': [
                    {'type': 'text', 'order': 1, 'data': {'content': '<h1>Academic Programs</h1><p>We offer comprehensive Islamic education programs designed to cater to students of various age groups and educational backgrounds.</p>'}},
                ]
            },
            {
                'slug': 'contact',
                'title': 'Contact Us',
                'is_published': True,
                'content_blocks': [
                    {'type': 'text', 'order': 1, 'data': {'content': '<h1>Get in Touch</h1><p>We are here to answer any questions you may have.</p>'}},
                ]
            },
        ]
        
        for page_data in pages:
            page, created = ContentPage.objects.get_or_create(
                slug=page_data['slug'],
                defaults=page_data
            )
            status = 'Created' if created else 'Exists'
            self.stdout.write(f'  ✓ {status}: {page_data["title"]}')

    def create_achievements(self):
        self.stdout.write('Creating Sample Achievements...')
        
        achievements = [
            {
                'title': 'National Quran Competition',
                'description': 'Our students secured top positions in the National Quran Recitation Competition 2023',
                'date': '2023-12-15',
                'images': [],
                'is_visible': True
            },
            {
                'title': 'Islamic Scholarship Award',
                'description': 'Recognized for excellence in Islamic Studies at the State Level',
                'date': '2023-11-20',
                'images': [],
                'is_visible': True
            },
        ]
        
        for ach_data in achievements:
            ach, created = Achievement.objects.get_or_create(
                title=ach_data['title'],
                defaults=ach_data
            )
            status = 'Created' if created else 'Exists'
            self.stdout.write(f'  ✓ {status}: {ach_data["title"]}')
