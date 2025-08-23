from .models import Course, Video, Material, Chapter
from rest_framework import viewsets
from .serializers import CoursePreviewSerializer, CourseDetailSerializer, ChapterDetailSerializer
from django.db.models import Sum, Count, OuterRef, Subquery, DurationField, Prefetch
from django.db.models.functions import Coalesce
import datetime

class CoursePreviewViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CoursePreviewSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        video_duration_sq = (
            Video.objects
            .filter(chapter__course=OuterRef('pk'))
            .values('chapter__course')
            .annotate(total=Sum('duration'))
            .values('total')[:1]
        )


        qs = (
            Course.objects.filter(is_active=True)
            .annotate(
                materials_count=Count('chapters__materials', distinct=True),
                video_duration=Coalesce(
                    Subquery(video_duration_sq, output_field=DurationField()),
                    datetime.timedelta()
                ),
            )
            .only('id', 'title', 'slug', 'description', 'is_active', 'updated_at', 'image_preview')
            .prefetch_related('tags')
        )
        return qs

class CourseDetailViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CourseDetailSerializer

    def get_queryset(self):

        qs = (
            Course.objects.filter(is_active=True)
            .only('id', 'title', 'description', 'slug')
            .prefetch_related('chapters')
        )
        return qs
    
class ChapterDetailViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ChapterDetailSerializer

    def get_queryset(self):

        qs = (
            Chapter.objects
            .select_related('course','test')
            .prefetch_related(
                Prefetch(
                    'materials',
                    queryset=Material.objects.filter(kind='required').order_by('order','id'),
                    to_attr='materials_required'
                ),
                Prefetch(
                    'materials',
                    queryset=Material.objects.filter(kind='extra').order_by('order','id'),
                    to_attr='materials_extra'
                ),
                'videos'
            )
        )
        return qs