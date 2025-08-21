from django.urls import path, include
from .views import CoursePreviewViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'courses_preview', CoursePreviewViewSet, basename='course-preview')
urlpatterns = [
    path('', include(router.urls)),
]