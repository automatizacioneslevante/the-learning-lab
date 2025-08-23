from django.contrib import admin
from .models import Course, Tag, Video, Material, Chapter, Test

admin.site.register([Course, Tag, Video, Material, Chapter, Test])
