"""
URL Configuration for Academic Admission System
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    # Faculty Dashboard Views
    FacultyLoginView, FacultyProfileView, FacultyDashboardView,
    FacultyClassesView, FacultyActivityView, FacultyClassStudentsView,
    FacultyClassAttendanceView, FacultyStudentDetailView, FacultyStudentAttendanceView,
    FacultyStudentNotesView, SaveAttendanceView,
    # Original views
    attendance_list, attendance_detail, faculty_list, class_list, class_detail,
    student_list, student_detail,
    # Public API ViewSets
    ProgramViewSet, AchievementViewSet, GalleryViewSet, FacultyViewSet,
    ContentPageViewSet, EnquiryViewSet, HealthCheckView,
    AdmissionViewSet, WhatsAppConfigViewSet
)

router = DefaultRouter()
# Register public API endpoints
router.register(r'programs', ProgramViewSet, basename='program')
router.register(r'achievements', AchievementViewSet, basename='achievement')
router.register(r'gallery', GalleryViewSet, basename='gallery')
router.register(r'faculty', FacultyViewSet, basename='faculty')
router.register(r'content', ContentPageViewSet, basename='content')
router.register(r'admissions', AdmissionViewSet, basename='admission')
router.register(r'whatsapp', WhatsAppConfigViewSet, basename='whatsapp')

urlpatterns = [
    # JWT Authentication
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Faculty Dashboard API
    path('faculty/login/', FacultyLoginView.as_view(), name='faculty_login'),
    path('faculty/profile/', FacultyProfileView.as_view(), name='faculty_profile'),
    path('faculty/dashboard/', FacultyDashboardView.as_view(), name='faculty_dashboard'),
    path('faculty/classes/', FacultyClassesView.as_view(), name='faculty_classes'),
    path('faculty/classes/<str:class_id>/students/', FacultyClassStudentsView.as_view(), name='faculty_class_students'),
    path('faculty/classes/<str:class_id>/attendance/', FacultyClassAttendanceView.as_view(), name='faculty_class_attendance'),
    path('faculty/activity/', FacultyActivityView.as_view(), name='faculty_activity'),
    path('faculty/students/<str:student_id>/', FacultyStudentDetailView.as_view(), name='faculty_student_detail'),
    path('faculty/students/<str:student_id>/attendance/', FacultyStudentAttendanceView.as_view(), name='faculty_student_attendance'),
    path('faculty/students/<str:student_id>/notes/', FacultyStudentNotesView.as_view(), name='faculty_add_note'),
    path('faculty/classes/<str:class_id>/save-attendance/', SaveAttendanceView.as_view(), name='faculty_save_attendance'),
    
    # Additional endpoints
    path('faculties/', faculty_list, name='faculty_list'),
    path('classes/', class_list, name='class_list'),
    path('classes/<str:pk>/', class_detail, name='class_detail'),
    path('attendances/', attendance_list, name='attendance_list'),
    path('attendances/<str:pk>/', attendance_detail, name='attendance_detail'),
    path('student-list/', student_list, name='student_list'),
    path('students/<str:pk>/', student_detail, name='student_detail'),
    
    # Router URLs (ViewSets)
    path('', include(router.urls)),
    
    # Public endpoints
    path('enquiries/', EnquiryViewSet.as_view({'post': 'create'}), name='enquiry-create'),
    path('health/', HealthCheckView.as_view(), name='health-check'),
]
