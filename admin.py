from django.contrib import admin
from .models import Matakuliah
from .models import Enrollment


@admin.register(Matakuliah)
class MatakuliahAdmin(admin.ModelAdmin):
    list_display = ('nama', 'kode', 'sks', 'dosen')
    list_filter = ('sks', 'dosen')
    search_fields = ('nama', 'kode')
    fieldsets = (
        ('Informasi Dasar', {
            'fields': ('nama', 'kode', 'sks')
        }),
        ('Detail', {
            'fields': ('deskripsi', 'dosen')
        }),
    )


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('mahasiswa', 'matakuliah', 'tanggal_ambil')
    search_fields = ('mahasiswa__nama', 'mahasiswa__npm', 'matakuliah__nama', 'matakuliah__kode')
