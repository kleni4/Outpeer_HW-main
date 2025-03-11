from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'start_date', 'end_date', 'get_students_count', 'max_students', 'is_active')
    list_filter = ('is_active', 'teacher', 'start_date', 'end_date')
    search_fields = ('title', 'description', 'teacher__email')
    filter_horizontal = ('students',)
    date_hierarchy = 'start_date'
    
    def get_students_count(self, obj):
        return obj.students.count()
    get_students_count.short_description = 'Количество студентов'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Ограничиваем выбор teacher только пользователями с ролью teacher
        form.base_fields['teacher'].queryset = form.base_fields['teacher'].queryset.filter(role='teacher')
        # Ограничиваем выбор students только пользователями с ролью student
        form.base_fields['students'].queryset = form.base_fields['students'].queryset.filter(role='student')
        return form

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'teacher')
        }),
        ('Даты', {
            'fields': ('start_date', 'end_date')
        }),
        ('Студенты', {
            'fields': ('students', 'max_students')
        }),
        ('Статус', {
            'fields': ('is_active',)
        })
    )
