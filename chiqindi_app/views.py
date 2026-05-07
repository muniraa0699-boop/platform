import csv
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Q
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from .models import CustomUser, WasteReport, Notification, VILOYATLAR, TUMANLAR
from .forms import RegisterForm, WasteReportForm, StatusUpdateForm, FilterForm


def send_notification(recipient, report, notif_type, message_text):
    """Sayt ichidagi bildirishnoma yaratish"""
    Notification.objects.create(
        recipient=recipient,
        report=report,
        notification_type=notif_type,
        message=message_text
    )
    # Email (konsolga)
    try:
        send_mail(
            subject=f"Chiqindi Platform: {message_text[:50]}",
            message=message_text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient.email],
            fail_silently=True,
        )
    except Exception:
        pass


def home(request):
    filter_form = FilterForm(request.GET or None)
    reports = WasteReport.objects.all()

    viloyat_filter = request.GET.get('viloyat', '')
    tuman_filter = request.GET.get('tuman', '')
    status_filter = request.GET.get('status', '')
    waste_type_filter = request.GET.get('waste_type', '')

    if viloyat_filter:
        reports = reports.filter(viloyat=viloyat_filter)
    if tuman_filter:
        reports = reports.filter(tuman__icontains=tuman_filter)
    if status_filter:
        reports = reports.filter(status=status_filter)
    if waste_type_filter:
        reports = reports.filter(waste_type=waste_type_filter)

    # Xarita uchun JSON data
    map_data = []
    for r in reports:
        map_data.append({
            'id': r.pk,
            'lat': r.latitude,
            'lng': r.longitude,
            'status': r.status,
            'color': r.get_marker_color(),
            'waste_type': r.get_waste_type_display(),
            'size': r.get_size_display(),
            'viloyat': r.get_viloyat_display() if r.viloyat else '',
            'tuman': r.tuman,
            'created_at': r.created_at.strftime('%d.%m.%Y %H:%M'),
            'status_display': r.get_status_display(),
            'url': f'/report/{r.pk}/',
        })

    # Statistika
    total = WasteReport.objects.count()
    done = WasteReport.objects.filter(status=WasteReport.STATUS_DONE).count()
    pending = WasteReport.objects.filter(status=WasteReport.STATUS_PENDING).count()
    in_progress = WasteReport.objects.filter(
        status__in=[WasteReport.STATUS_ACCEPTED, WasteReport.STATUS_IN_PROGRESS, WasteReport.STATUS_CLEANING]
    ).count()

    top_regions = WasteReport.objects.values('viloyat').annotate(
        count=Count('id')).order_by('-count')[:5]

    region_names = dict(VILOYATLAR)
    top_regions_display = [
        {'viloyat': region_names.get(r['viloyat'], r['viloyat']), 'count': r['count']}
        for r in top_regions if r['viloyat']
    ]

    recent_reports = WasteReport.objects.select_related('citizen').order_by('-created_at')[:10]

    # Map center
    map_center_lat = 41.2995
    map_center_lng = 69.2401
    if viloyat_filter:
        VILOYAT_CENTERS = {
            'toshkent_sh': (41.2995, 69.2401),
            'toshkent': (41.1231, 69.8597),
            'samarqand': (39.6542, 66.9597),
            'buxoro': (39.7747, 64.4286),
            'andijon': (40.7821, 72.3442),
            'fargona': (40.3864, 71.7864),
            'namangan': (41.0011, 71.6726),
            'qashqadaryo': (38.8610, 65.7919),
            'surxondaryo': (37.9400, 67.5700),
            'navoiy': (40.1036, 65.3792),
            'xorazm': (41.5228, 60.6225),
            'jizzax': (40.1158, 67.8422),
            'sirdaryo': (40.8406, 68.6636),
            'qoraqalpogiston': (43.7333, 59.0167),
        }
        center = VILOYAT_CENTERS.get(viloyat_filter, (41.2995, 69.2401))
        map_center_lat, map_center_lng = center

    context = {
        'filter_form': filter_form,
        'map_data_json': json.dumps(map_data),
        'total': total,
        'done': done,
        'pending': pending,
        'in_progress': in_progress,
        'top_regions': top_regions_display,
        'recent_reports': recent_reports,
        'map_center_lat': map_center_lat,
        'map_center_lng': map_center_lng,
        'viloyatlar': VILOYATLAR,
        'tumanlar_json': json.dumps(TUMANLAR),
        'viloyat_filter': viloyat_filter,
    }
    return render(request, 'chiqindi_app/home.html', context)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.get_full_name() or user.username}!")
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'chiqindi_app/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.get_full_name() or user.username}!")
            return redirect(request.GET.get('next', 'home'))
        else:
            messages.error(request, "Foydalanuvchi nomi yoki parol noto'g'ri!")
    return render(request, 'chiqindi_app/login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Tizimdan chiqildi.")
    return redirect('home')


@login_required
def create_report(request):
    if not request.user.is_citizen():
        messages.error(request, "Faqat fuqarolar chiqindi xabari yuborishi mumkin.")
        return redirect('home')

    if request.method == 'POST':
        form = WasteReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.citizen = request.user
            report.save()

            # Hokimiyat xodimlariga bildirishnoma
            authority_users = CustomUser.objects.filter(role=CustomUser.ROLE_AUTHORITY, is_active=True)
            for auth_user in authority_users:
                send_notification(
                    recipient=auth_user,
                    report=report,
                    notif_type=Notification.TYPE_NEW_REPORT,
                    message_text=f"Yangi chiqindi xabari #{report.pk}: {report.get_waste_type_display()}, {report.get_size_display()}. Manzil: {report.viloyat}, {report.tuman}"
                )

            messages.success(request, f"Chiqindi xabari #{report.pk} muvaffaqiyatli yuborildi! Hokimiyat xodimlari xabardor qilindi.")
            return redirect('report_detail', pk=report.pk)
    else:
        lat = request.GET.get('lat', '')
        lng = request.GET.get('lng', '')
        form = WasteReportForm(initial={'latitude': lat, 'longitude': lng})

    return render(request, 'chiqindi_app/create_report.html', {
        'form': form,
        'tumanlar_json': json.dumps(TUMANLAR),
        'viloyatlar': VILOYATLAR,
    })


def report_detail(request, pk):
    report = get_object_or_404(WasteReport, pk=pk)
    can_edit_status = request.user.is_authenticated and request.user.is_authority()
    status_form = None

    if can_edit_status and request.method == 'POST':
        old_status = report.status
        status_form = StatusUpdateForm(request.POST, instance=report)
        if status_form.is_valid():
            updated = status_form.save()
            if old_status != updated.status:
                # Fuqaroga bildirishnoma
                send_notification(
                    recipient=report.citizen,
                    report=report,
                    notif_type=Notification.TYPE_STATUS_CHANGED,
                    message_text=f"Sizning #{report.pk}-xabaringiz holati o'zgardi: {report.get_status_display()}"
                )
                messages.success(request, f"Holat muvaffaqiyatli yangilandi: {report.get_status_display()}")
            return redirect('report_detail', pk=pk)
    elif can_edit_status:
        status_form = StatusUpdateForm(instance=report)

    return render(request, 'chiqindi_app/report_detail.html', {
        'report': report,
        'status_form': status_form,
        'can_edit': request.user.is_authenticated and request.user == report.citizen,
    })


@login_required
def edit_report(request, pk):
    report = get_object_or_404(WasteReport, pk=pk, citizen=request.user)
    if report.status != WasteReport.STATUS_PENDING:
        messages.warning(request, "Faqat 'Kutilmoqda' holatidagi xabarlarni tahrirlash mumkin.")
        return redirect('report_detail', pk=pk)

    if request.method == 'POST':
        form = WasteReportForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            form.save()
            messages.success(request, "Xabar muvaffaqiyatli yangilandi.")
            return redirect('report_detail', pk=pk)
    else:
        form = WasteReportForm(instance=report)

    return render(request, 'chiqindi_app/create_report.html', {
        'form': form,
        'edit_mode': True,
        'report': report,
        'tumanlar_json': json.dumps(TUMANLAR),
    })


@login_required
def my_reports(request):
    if request.user.is_authority():
        reports = WasteReport.objects.filter(assigned_to=request.user).order_by('-created_at')
        return render(request, 'chiqindi_app/my_reports.html', {'reports': reports, 'is_authority': True})
    else:
        reports = WasteReport.objects.filter(citizen=request.user).order_by('-created_at')
        return render(request, 'chiqindi_app/my_reports.html', {'reports': reports, 'is_authority': False})


@login_required
def authority_panel(request):
    if not request.user.is_authority() and not request.user.is_staff:
        messages.error(request, "Sizda bu sahifaga kirish huquqi yo'q.")
        return redirect('home')

    filter_form = FilterForm(request.GET or None)
    reports = WasteReport.objects.select_related('citizen', 'assigned_to').all()

    viloyat = request.GET.get('viloyat', '')
    status_f = request.GET.get('status', '')
    waste_type_f = request.GET.get('waste_type', '')

    if viloyat:
        reports = reports.filter(viloyat=viloyat)
    if status_f:
        reports = reports.filter(status=status_f)
    if waste_type_f:
        reports = reports.filter(waste_type=waste_type_f)

    reports = reports.order_by('-created_at')

    stats = {
        'total': WasteReport.objects.count(),
        'pending': WasteReport.objects.filter(status=WasteReport.STATUS_PENDING).count(),
        'in_progress': WasteReport.objects.filter(status__in=[WasteReport.STATUS_ACCEPTED, WasteReport.STATUS_IN_PROGRESS, WasteReport.STATUS_CLEANING]).count(),
        'done': WasteReport.objects.filter(status=WasteReport.STATUS_DONE).count(),
    }

    return render(request, 'chiqindi_app/authority_panel.html', {
        'reports': reports,
        'filter_form': filter_form,
        'stats': stats,
    })


@login_required
def export_csv(request):
    if not request.user.is_authority() and not request.user.is_staff:
        return redirect('home')

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="chiqindi_xabarlari.csv"'
    response.write('\ufeff')  # BOM for Excel

    writer = csv.writer(response)
    writer.writerow(['ID', 'Fuqaro', 'Viloyat', 'Tuman', 'Manzil', 'Chiqindi turi', 'Hajmi', 'Holati', 'Latitude', 'Longitude', 'Yaratilgan', 'Yangilangan'])

    for r in WasteReport.objects.select_related('citizen').order_by('-created_at'):
        writer.writerow([
            r.pk, r.citizen.get_full_name() or r.citizen.username,
            r.get_viloyat_display() if r.viloyat else '', r.tuman, r.address,
            r.get_waste_type_display(), r.get_size_display(), r.get_status_display(),
            r.latitude, r.longitude,
            r.created_at.strftime('%d.%m.%Y %H:%M'),
            r.updated_at.strftime('%d.%m.%Y %H:%M'),
        ])

    return response


@login_required
def notifications_view(request):
    notifs = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    # Mark all as read
    notifs.filter(is_read=False).update(is_read=True)
    return render(request, 'chiqindi_app/notifications.html', {'notifications': notifs})


@login_required
def profile_view(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.phone = request.POST.get('phone', user.phone)
        user.email = request.POST.get('email', user.email)
        user.save()
        messages.success(request, "Profil muvaffaqiyatli yangilandi.")
        return redirect('profile')
    return render(request, 'chiqindi_app/profile.html')


def statistics_view(request):
    total = WasteReport.objects.count()
    done = WasteReport.objects.filter(status=WasteReport.STATUS_DONE).count()
    pending = WasteReport.objects.filter(status=WasteReport.STATUS_PENDING).count()
    in_progress = WasteReport.objects.filter(status__in=[WasteReport.STATUS_ACCEPTED, WasteReport.STATUS_IN_PROGRESS, WasteReport.STATUS_CLEANING]).count()

    by_type = WasteReport.objects.values('waste_type').annotate(count=Count('id')).order_by('-count')
    by_viloyat = WasteReport.objects.values('viloyat').annotate(count=Count('id')).order_by('-count')
    by_status = WasteReport.objects.values('status').annotate(count=Count('id'))

    region_names = dict(VILOYATLAR)
    type_names = dict(WasteReport.WASTE_TYPE_CHOICES)
    status_names = dict(WasteReport.STATUS_CHOICES)

    chart_type = json.dumps([{'label': type_names.get(t['waste_type'], t['waste_type']), 'count': t['count']} for t in by_type])
    chart_viloyat = json.dumps([{'label': region_names.get(v['viloyat'], v['viloyat']), 'count': v['count']} for v in by_viloyat if v['viloyat']])
    chart_status = json.dumps([{'label': status_names.get(s['status'], s['status']), 'count': s['count']} for s in by_status])

    return render(request, 'chiqindi_app/statistics.html', {
        'total': total, 'done': done, 'pending': pending, 'in_progress': in_progress,
        'chart_type': chart_type, 'chart_viloyat': chart_viloyat, 'chart_status': chart_status,
    })


# AJAX: tuman list
def get_tumanlar(request):
    viloyat = request.GET.get('viloyat', '')
    tumanlar = TUMANLAR.get(viloyat, [])
    return JsonResponse({'tumanlar': tumanlar})
