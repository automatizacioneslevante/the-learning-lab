from django.db import models
from django.utils.text import slugify

class Course(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    image_preview = models.ImageField(upload_to='course_previews/', blank=True, null=True)
    slug = models.SlugField(unique=True, max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, max_length=60)
    courses = models.ManyToManyField(Course, related_name='tags', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Chapter(models.Model):
    course = models.ForeignKey(Course, related_name='chapters', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False, null=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
class Test(models.Model):
    chapter = models.OneToOneField(Chapter, related_name='test', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    passing_score = models.PositiveIntegerField(default=5)
    time_limit = models.DurationField(blank=True, null=True)

    def __str__(self):
        return f"{self.chapter.course.title} - {self.title}"
    
    @property
    def course(self):
        return self.chapter.course
    
class Material(models.Model):
    class Kind(models.TextChoices):
        REQUIRED = "required", "Material obligatorio"
        EXTRA = "extra", "Material de refuerzo"

    chapter = models.ForeignKey(Chapter, related_name='materials', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False, null=False)
    kind = models.CharField(max_length=20, choices=Kind.choices, default=Kind.REQUIRED)
    file = models.FileField(upload_to='materials/', blank=False, null=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.chapter.course.title} - {self.chapter.title} - {self.title}"
    
class Video(models.Model):
    chapter = models.ForeignKey(Chapter, related_name='videos', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False, null=False)
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    is_preview = models.BooleanField(default=False)
    duration = models.DurationField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.chapter.course.title} - {self.chapter.title} - {self.title}"