from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'lessons', views.LessonViewSet)

app_name = 'lessons'

urlpatterns = [
    path('', include(router.urls)),
    # Маршруты для курсов
    path('courses/', views.course_list, name='course-list'),
    path('courses/<int:course_id>/lessons/', views.course_lessons, name='course-lessons'),
    # Маршруты для веб-интерфейса
    path('courses/<int:course_id>/lessons/view/', views.course_lessons_view, name='course-lessons-view'),
    # Маршрут для детального просмотра урока
    path('lessons/<int:lesson_id>/detail/', views.lesson_detail_view, name='lesson-detail'),
] 