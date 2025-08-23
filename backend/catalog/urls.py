from django.urls import path, include
from .views import CoursePreviewViewSet, CourseDetailViewSet, ChapterDetailViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'courses_preview', CoursePreviewViewSet, basename='course-preview')
router.register(r'courses', CourseDetailViewSet, basename='course-detail')
router.register(r'chapters', ChapterDetailViewSet, basename='chapter-detail')
urlpatterns = [
    path('', include(router.urls)),
]