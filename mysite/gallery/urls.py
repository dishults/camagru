from django.urls import path

from . import views

urlpatterns = [
    path('', views.GalleryView.as_view(), name='gallery'),
    path('images/<image>', views.show_image, name='show-image'),
]
