from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('register/', views.register, name='register'),

    path('login/', views.login_view, name='login'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('predict/', views.predict, name='predict'),
    path('history/', views.history, name='history'),
    path(
    'delete-history/<int:id>/',
    views.delete_history,
    name='delete_history'
),
path('analytics/', views.analytics, name='analytics'),
path(
    'career-guidance/',
    views.career_guidance,
    name='career_guidance'
),
path(
    'export-csv/',
    views.export_csv,
    name='export_csv'
),
    path('logout/', views.logout_view, name='logout'),

]