from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'role', 'is_email_verified', 'get_student_info', 'is_active', 'date_joined')
    list_filter = ('role', 'is_email_verified', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Персональная информация', {'fields': ('role', 'is_email_verified')}),
        ('Информация о студенте', {
            'fields': (
                'attendance_percentage',
                'lessons_count',
                'total_score',
                'get_attendance_progress'
            ),
            'classes': ('wide',),
            'description': 'Эти поля доступны только для пользователей с ролью "Студент"'
        }),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    
    readonly_fields = ('get_attendance_progress',)
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'role', 'password1', 'password2'),
        }),
    )
    
    def get_student_info(self, obj):
        if obj.role == User.Role.STUDENT:
            return format_html(
                '<div style="min-width:200px">'
                'Посещаемость: <b>{}%</b><br>'
                'Уроков: <b>{}</b><br>'
                'Баллы: <b>{}</b>'
                '</div>',
                obj.attendance_percentage,
                obj.lessons_count,
                obj.total_score
            )
        return '-'
    get_student_info.short_description = 'Информация о студенте'

    def get_attendance_progress(self, obj):
        if obj.role == User.Role.STUDENT:
            color = 'success' if obj.attendance_percentage >= 70 else 'warning' if obj.attendance_percentage >= 40 else 'danger'
            return format_html(
                '<div class="progress" style="height: 20px; width: 100%;">'
                '<div class="progress-bar bg-{}" role="progressbar" style="width: {}%">'
                '{:.1f}%'
                '</div>'
                '</div>',
                color,
                obj.attendance_percentage,
                obj.attendance_percentage
            )
        return '-'
    get_attendance_progress.short_description = 'Прогресс посещаемости'

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj and obj.role != User.Role.STUDENT:
            # Скрываем поля студента для не-студентов
            return [fs for fs in fieldsets if fs[0] != 'Информация о студенте']
        return fieldsets

    class Media:
        css = {
            'all': ('https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',)
        }
