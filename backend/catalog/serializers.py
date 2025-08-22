from rest_framework import serializers
from .models import Course
from django.db.models import Sum

class CoursePreviewSerializer(serializers.ModelSerializer):
    tags_main = serializers.SerializerMethodField()
    video_duration = serializers.SerializerMethodField()
    resource_count = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 
                  'description', 'tags_main', 'updated_at',
                  'video_duration', 'resource_count', 'is_active', 'image_preview']
        
        read_only_fields = fields
    
    def get_tags_main(self, obj):
        return [tag.name for tag in obj.tags.all()[:3]]
    def get_video_duration(self, obj):
        total = getattr(obj, 'video_duration', None)
        if total is None:
            total = obj.videos.aggregate(total=Sum('duration'))['total']
        if not total:
            return "00:00:00"
        secs = int(total.total_seconds())
        h, r = divmod(secs, 3600)
        m, s = divmod(r, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"
    def get_resource_count(self, obj):
        mcount = getattr(obj, 'materials_count', None)
        if mcount is None:
            mcount = obj.materials.count()
        return mcount or 0        
        
    
