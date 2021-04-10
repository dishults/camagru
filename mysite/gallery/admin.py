from django.contrib import admin

from .models import Image, Comment, Like


class ImageAdmin(admin.ModelAdmin):
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()


class CommentInline(admin.TabularInline):
    model = Comment


class LikeInline(admin.TabularInline):
    model = Like


@admin.register(Image)
class GalleryAdmin(ImageAdmin):
    inlines = [CommentInline, LikeInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass
