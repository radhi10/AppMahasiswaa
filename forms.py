from django import forms
from .models import Matakuliah
from .models import Enrollment
from mahasiswa.models import Mahasiswa


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['mahasiswa', 'matakuliah']
        widgets = {
            'mahasiswa': forms.Select(attrs={'class': 'form-control'}),
            'matakuliah': forms.Select(attrs={'class': 'form-control'}),
        }


class MatakuliahForm(forms.ModelForm):
    class Meta:
        model = Matakuliah
        fields = ['nama', 'kode', 'sks', 'deskripsi', 'dosen']
        widgets = {
            'nama': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama Matakuliah'
            }),
            'kode': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Kode Matakuliah (mis. MK001)'
            }),
            'sks': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Jumlah SKS'
            }),
            'deskripsi': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Deskripsi Matakuliah',
                'rows': 3
            }),
            'dosen': forms.Select(attrs={
                'class': 'form-control',
            }),
        }
