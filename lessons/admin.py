from django.contrib import admin
from .models import Lesson, Attendance

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'duration', 'created_at')
    list_filter = ('course', 'created_at')
    search_fields = ('title', 'description', 'course__title')
    ordering = ('course', 'order')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'student', 'is_present', 'homework_completed', 'grade')
    list_filter = ('is_present', 'homework_completed', 'lesson__course')
    search_fields = ('student__email', 'lesson__title', 'comment')
    ordering = ('lesson', 'student')
