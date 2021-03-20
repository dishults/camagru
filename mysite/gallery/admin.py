from django.contrib import admin

from .models import Image, Comment, Like


class CommentInline(admin.TabularInline):
    model = Comment


class LikeInline(admin.TabularInline):
    model = Like


@admin.register(Image)
class GalleryAdmin(admin.ModelAdmin):
    inlines = [CommentInline, LikeInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass
