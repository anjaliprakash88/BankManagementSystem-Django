from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_form, name='home'),
    path('login', views.loginView, name='login'),

    path('regform', views.register_form, name='regform'),
    path('register', views. registerView, name='register'),

    path('banker', views.banker_view, name='banker'),
    path('view_user', views.view_user, name='view_user'),


    path('deposit', views.deposit_view, name='deposit'),
    path('withdraw', views.withdraw_view, name='withdraw'),
    path('customer', views.customer_view, name='customer'),
    path('history', views.history, name='history'),
    path('moreinfo', views.moreinfo, name='moreinfo'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('profile/<int:pk>/edit/', views.edit_profile, name='edit_profile'),

    path('logout', views.logoutView, name='logout'),
]
