from rest_framework import serializers
from .models import Course, Chapter, Video, Material
from django.db.models import Sum

class CoursePreviewSerializer(serializers.ModelSerializer):
    tags_main = serializers.SerializerMethodField()
    video_duration = serializers.SerializerMethodField()
    resource_count = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 
                  'description', 'tags_main', 'updated_at',
                  'video_duration', 'resource_count', 'is_active', 'image_url']
        
        read_only_fields = fields

    def get_image_url(self, obj):
        if not obj.image_preview:
            return None
        request = self.context.get('request')
        url = obj.image_preview.url
        return request.build_absolute_uri(url) if request else url
    
    def get_tags_main(self, obj):
        return [tag.name for tag in obj.tags.all()[:3]]
    def get_video_duration(self, obj):
        total = getattr(obj, 'video_duration', None)
        if total is None:
            total = Video.objects.filter(chapter__course=obj)\
                                 .aggregate(total=Sum('duration'))['total']
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
        

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['id', 'title', 'order']
        read_only_fields = fields

class VideoOut(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    duration_seconds = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ("id","title","url",
                  "duration_seconds", "is_preview", "order")
        
        def get_url(self, obj):
            if obj.video_url:
                return obj.video_url
            if obj.video_file:
                request = self.context.get("request")
                url = obj.video_file.url
                return request.build_absolute_uri(url) if request else url
            return None
        
        def get_duration_seconds(self, obj):
            return int(obj.duration.total_seconds()) if obj.duration else None
        
class MaterialOut(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Material
        fields = ("id","title","url")

    def get_url(self, obj):
        if obj.file:
            request = self.context.get("request")
            url = obj.file.url
            return request.build_absolute_uri(url) if request else url
        return None
    
class ChapterDetailSerializer(serializers.ModelSerializer):
    required_material = serializers.SerializerMethodField()
    extra_material = serializers.SerializerMethodField()
    videos = VideoOut(many=True, read_only=True)
    test = serializers.SerializerMethodField()

    class Meta:
        model = Chapter
        fields = ("id","order","title",
                  "required_material", "extra_material", 
                  "videos","test")
        
    def get_required_material(self,obj):
        req = getattr(obj, 'materials_required', [])
        return MaterialOut(req, many=True, context=self.context).data
    def get_extra_material(self,obj): 
        ext = getattr(obj, 'materials_extra', [])
        return MaterialOut(ext, many=True, context=self.context).data
    def get_test(self, obj):
        t = getattr(obj, "test", None)
        if not t:
            return None
        return {
            "id": t.id,
            "title": t.title,
            "passing_score": t.passing_score,
            "time_limit": t.time_limit,
        }

class CourseDetailSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'chapters']
        read_only_fields = fields
