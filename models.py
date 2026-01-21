from django.db import models
from dosen.models import Dosen
from mahasiswa.models import Mahasiswa


class Matakuliah(models.Model):
    nama = models.CharField(max_length=200)
    kode = models.CharField(max_length=50, unique=True)
    sks = models.PositiveIntegerField()
    deskripsi = models.TextField(blank=True)
    dosen = models.ForeignKey(Dosen, on_delete=models.SET_NULL, null=True, blank=True, related_name='matakuliah')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name = "Matakuliah"
        verbose_name_plural = "Matakuliah"

    def __str__(self):
        return f"{self.nama} ({self.kode})"


class Enrollment(models.Model):
    mahasiswa = models.ForeignKey(Mahasiswa, on_delete=models.CASCADE, related_name='enrollments')
    matakuliah = models.ForeignKey(Matakuliah, on_delete=models.CASCADE, related_name='enrollments')
    tanggal_ambil = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('mahasiswa', 'matakuliah')
        verbose_name = 'Enrollment'
        verbose_name_plural = 'Enrollments'

    def __str__(self):
        return f"{self.mahasiswa} -> {self.matakuliah}"
