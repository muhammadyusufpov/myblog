from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "content_format", "created_at")
    list_filter = ("content_format", "category")
    readonly_fields = ("content_format",)
