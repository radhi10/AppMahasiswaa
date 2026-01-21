"""
URL configuration for project1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mahasiswa/', include('mahasiswa.urls')),
    path('dosen/', include('dosen.urls')),
    path('matakuliah/', include('matakuliah.urls')),
    path('', include('AppMahasiswa.urls')),
]
