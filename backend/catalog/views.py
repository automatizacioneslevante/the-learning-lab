from .models import Course
from rest_framework import viewsets
from .serializers import CoursePreviewSerializer
from django.db.models import Sum, Count

class CoursePreviewViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CoursePreviewSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        qs = (
            Course.objects.filter(is_active=True)
            .annotate(
                video_duration=Sum('videos__duration'),
                materials_count=Count('materials', distinct=True)
            )
            .only('id', 'title', 'slug', 'description', 'is_active', 'updated_at')
            .prefetch_related('tags')
        )
        return qs


