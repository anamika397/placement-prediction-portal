from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('register/', views.register, name='register'),

    path('login/', views.login_view, name='login'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('predict/', views.predict, name='predict'),
    path('logout/', views.logout_view, name='logout'),

]