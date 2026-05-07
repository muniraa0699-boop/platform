from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('report/create/', views.create_report, name='create_report'),
    path('report/<int:pk>/', views.report_detail, name='report_detail'),
    path('report/<int:pk>/edit/', views.edit_report, name='edit_report'),
    path('my-reports/', views.my_reports, name='my_reports'),
    path('authority/', views.authority_panel, name='authority_panel'),
    path('authority/export/', views.export_csv, name='export_csv'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('profile/', views.profile_view, name='profile'),
    path('statistics/', views.statistics_view, name='statistics'),
    path('api/tumanlar/', views.get_tumanlar, name='get_tumanlar'),
]
