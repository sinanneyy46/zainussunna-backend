"""
URL Configuration for Academic Admission System
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    ProgramViewSet, AdmissionViewSet, InternalNoteViewSet,
    ContentPageViewSet, AchievementViewSet, GalleryViewSet,
    EnquiryViewSet, AnalyticsViewSet, HealthCheckView, FacultyViewSet,
    AdmissionExportView
)

router = DefaultRouter()
router.register(r'programs', ProgramViewSet, basename='program')
router.register(r'admissions', AdmissionViewSet, basename='admission')
router.register(r'notes', InternalNoteViewSet, basename='note')
router.register(r'content', ContentPageViewSet, basename='content')
router.register(r'achievements', AchievementViewSet, basename='achievement')
router.register(r'gallery', GalleryViewSet, basename='gallery')
router.register(r'enquiries', EnquiryViewSet, basename='enquiry')
router.register(r'analytics', AnalyticsViewSet, basename='analytics')

urlpatterns = [
    path('', include(router.urls)),
    
    # JWT Authentication
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Health check
    path('health/', HealthCheckView.as_view(), name='health_check'),
    
    # Admissions export
    path('admissions/export/', AdmissionExportView.as_view(), name='admissions_export'),
]

