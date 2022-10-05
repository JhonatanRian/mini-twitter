from django.contrib import admin
from django.urls import path, re_path
from .views import index, search
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('', index, name="home"),
    path('search/', search, name="search"),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
]
