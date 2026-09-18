from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "content_format", "created_at")
    list_filter = ("content_format", "category")
    fields = ("category", "title", "content", "content_format", "created_at")
    readonly_fields = ("created_at",)
