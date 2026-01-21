from django.shortcuts import render
from .forms import MatakuliahForm
from .models import Matakuliah, Enrollment
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from mahasiswa.models import Mahasiswa
from dosen.models import Dosen
import json
from django.utils import timezone


@login_required(login_url='/admin/login/')
def input_matakuliah(request):
    pesan = ""
    if request.method == 'POST':
        form = MatakuliahForm(request.POST)
        if form.is_valid():
            form.save()
            pesan = "Data berhasil tersimpan"
            return redirect('matakuliah:input_matakuliah')
    else:
        form = MatakuliahForm()

    semua_matakuliah = Matakuliah.objects.all()

    # Dashboard counts
    total_matakuliah = semua_matakuliah.count()
    total_dosen = Dosen.objects.count()
    total_mahasiswa = Mahasiswa.objects.count()

    # prepare sparkline data (last 6 months)
    months = _last_n_months(6)
    matakuliah_trend = _counts_by_month_for_model(Matakuliah, 'created_at', months)
    mahasiswa_trend = _counts_by_month_for_model(Mahasiswa, 'created_at', months)
    dosen_trend = _counts_by_month_for_model(Dosen, 'created_at', months)

    context = {
        'form': form,
        'pesan': pesan,
        'semua_matakuliah': semua_matakuliah,
        'total_matakuliah': total_matakuliah,
        'total_dosen': total_dosen,
        'total_mahasiswa': total_mahasiswa,
        'trend_months': json.dumps(months),
        'matakuliah_trend': json.dumps(matakuliah_trend),
        'mahasiswa_trend': json.dumps(mahasiswa_trend),
        'dosen_trend': json.dumps(dosen_trend),
    }
    return render(request, 'matakuliah/input.html', context)


def _last_n_months(n=6):
    today = timezone.now().date().replace(day=1)
    months = []
    for i in range(n-1, -1, -1):
        m = (today.replace(day=1) - timezone.timedelta(days=30*i))
        months.append(m)
    # Better: generate proper year-month strings
    labels = []
    for i in range(n-1, -1, -1):
        dt = (today - timezone.timedelta(days=30*i))
        labels.append(dt.strftime('%Y-%m'))
    return labels

def _counts_by_month_for_model(model, date_field_name, months):
    counts = []
    for m in months:
        year, month = map(int, m.split('-'))
        qs = model.objects.filter(**{f"{date_field_name}__year": year, f"{date_field_name}__month": month})
        counts.append(qs.count())
    return counts


@login_required(login_url='/admin/login/')
def edit_matakuliah(request, pk):
    mk = get_object_or_404(Matakuliah, pk=pk)
    if request.method == 'POST':
        form = MatakuliahForm(request.POST, instance=mk)
        if form.is_valid():
            form.save()
            return redirect('matakuliah:input_matakuliah')
    else:
        form = MatakuliahForm(instance=mk)
    return render(request, 'matakuliah/edit.html', {'form': form, 'mk': mk})


@login_required(login_url='/admin/login/')
def delete_matakuliah(request, pk):
    mk = get_object_or_404(Matakuliah, pk=pk)
    # Only allow deletion via POST (form from the list). For GET, redirect back.
    if request.method == 'POST':
        mk.delete()
    return redirect('matakuliah:input_matakuliah')


@login_required(login_url='/admin/login/')
def stats(request):
    from .models import Enrollment
    
    # Dashboard counts
    total_matakuliah = Matakuliah.objects.count()
    total_dosen = Dosen.objects.count()
    total_mahasiswa = Mahasiswa.objects.count()

    # prepare sparkline data (last 6 months)
    months = _last_n_months(6)
    matakuliah_trend = _counts_by_month_for_model(Matakuliah, 'created_at', months)
    mahasiswa_trend = _counts_by_month_for_model(Mahasiswa, 'created_at', months)
    dosen_trend = _counts_by_month_for_model(Dosen, 'created_at', months)

    # Data untuk charts
    dosen_list = Dosen.objects.all()
    courses_labels = [d.nama for d in dosen_list]
    courses_data = [d.matakuliah.count() for d in dosen_list]
    
    students_labels = courses_labels
    students_data = []
    for dosen in dosen_list:
        count = 0
        for matakuliah in dosen.matakuliah.all():
            count += matakuliah.enrollments.count()
        students_data.append(count)
    
    matakuliah_list = Matakuliah.objects.all()
    enroll_labels = [m.nama for m in matakuliah_list]
    enroll_data = [m.enrollments.count() for m in matakuliah_list]

    context = {
        'total_matakuliah': total_matakuliah,
        'total_dosen': total_dosen,
        'total_mahasiswa': total_mahasiswa,
        'trend_months': json.dumps(months),
        'matakuliah_trend': json.dumps(matakuliah_trend),
        'mahasiswa_trend': json.dumps(mahasiswa_trend),
        'dosen_trend': json.dumps(dosen_trend),
        'courses_labels': json.dumps(courses_labels),
        'courses_data': json.dumps(courses_data),
        'students_labels': json.dumps(students_labels),
        'students_data': json.dumps(students_data),
        'enroll_labels': json.dumps(enroll_labels),
        'enroll_data': json.dumps(enroll_data),
    }
    return render(request, 'matakuliah/stats.html', context)


@login_required(login_url='/admin/login/')
def enroll(request):
    from .forms import EnrollmentForm
    pesan = ""
    
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            pesan = "Mahasiswa berhasil didaftarkan ke mata kuliah"
            return redirect('matakuliah:enroll')
    else:
        form = EnrollmentForm()
    
    # Dashboard counts
    total_matakuliah = Matakuliah.objects.count()
    total_dosen = Dosen.objects.count()
    total_mahasiswa = Mahasiswa.objects.count()
    total_enrollments = Enrollment.objects.count()
    
    # Get all enrollments
    semua_enrollments = Enrollment.objects.select_related('mahasiswa', 'matakuliah').all()
    
    context = {
        'form': form,
        'pesan': pesan,
        'total_matakuliah': total_matakuliah,
        'total_dosen': total_dosen,
        'total_mahasiswa': total_mahasiswa,
        'total_enrollments': total_enrollments,
        'semua_enrollments': semua_enrollments,
    }
    return render(request, 'matakuliah/enroll.html', context)
