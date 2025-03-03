from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('verify-email/<int:user_id>/', views.verify_email, name='verify_email'),
    path('list/', views.user_list, name='user_list'),
    path('export-excel/', views.export_users_excel, name='export_users_excel'),
]