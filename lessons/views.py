from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Lesson, Attendance
from .serializers import LessonSerializer, AttendanceSerializer
from courses.models import Course
from django.contrib.auth import get_user_model
from django.utils import timezone
from courses.serializers import CourseSerializer
from .permissions import IsManagerOrReadOnly

User = get_user_model()

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsManagerOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        course_id = self.request.query_params.get('course_id')
        lesson_type = self.request.query_params.get('lesson_type')
        is_required = self.request.query_params.get('is_required')
        
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        if lesson_type:
            queryset = queryset.filter(lesson_type=lesson_type)
        if is_required is not None:
            queryset = queryset.filter(is_required=is_required.lower() == 'true')
            
        return queryset.order_by('course', 'order')

    @action(detail=True, methods=['post'])
    def mark_attendance(self, request, pk=None):
        lesson = self.get_object()
        student_id = request.data.get('student_id')
        is_present = request.data.get('is_present', True)
        
        if not student_id:
            return Response(
                {"error": "student_id обязателен"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        attendance, created = Attendance.objects.get_or_create(
            lesson=lesson,
            student_id=student_id,
            defaults={'is_present': is_present}
        )
        
        if not created:
            attendance.is_present = is_present
            attendance.save()
            
        serializer = AttendanceSerializer(
            attendance,
            context={'request': request}
        )
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def submit_homework(self, request, pk=None):
        lesson = self.get_object()
        student_id = request.data.get('student_id')
        homework_file = request.FILES.get('homework_file')
        
        if not student_id:
            return Response(
                {"error": "student_id обязателен"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if not homework_file:
            return Response(
                {"error": "homework_file обязателен"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if lesson.homework_deadline and timezone.now() > lesson.homework_deadline:
            return Response(
                {"error": "Срок сдачи домашнего задания истек"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        attendance = get_object_or_404(
            Attendance,
            lesson=lesson,
            student_id=student_id
        )
        
        attendance.homework_file = homework_file
        attendance.homework_completed = True
        attendance.homework_submitted_at = timezone.now()
        attendance.save()
        
        serializer = AttendanceSerializer(
            attendance,
            context={'request': request}
        )
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def grade_homework(self, request, pk=None):
        lesson = self.get_object()
        student_id = request.data.get('student_id')
        grade = request.data.get('grade')
        score = request.data.get('score')
        comment = request.data.get('comment')
        
        if not student_id:
            return Response(
                {"error": "student_id обязателен"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        attendance = get_object_or_404(
            Attendance,
            lesson=lesson,
            student_id=student_id
        )
        
        if grade is not None:
            attendance.grade = grade
        if score is not None:
            attendance.score = score
        if comment:
            attendance.comment = comment
            
        attendance.save()
        
        serializer = AttendanceSerializer(
            attendance,
            context={'request': request}
        )
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def attendance_list(self, request, pk=None):
        lesson = self.get_object()
        attendances = Attendance.objects.filter(lesson=lesson)
        serializer = AttendanceSerializer(
            attendances,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def course_lessons(self, request):
        course_id = request.query_params.get('course_id')
        if not course_id:
            return Response(
                {'error': 'Необходимо указать course_id'},
                status=status.HTTP_400_BAD_REQUEST
            )

        course = get_object_or_404(Course, id=course_id)
        lessons = self.get_queryset().filter(course=course)
        serializer = self.get_serializer(lessons, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def course_list(request):
    """
    Получение списка всех курсов
    """
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def course_lessons(request, course_id):
    """
    Получение списка всех уроков определенного курса
    """
    course = get_object_or_404(Course, id=course_id)
    lessons = Lesson.objects.filter(course=course).order_by('order')
    serializer = LessonSerializer(lessons, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def lesson_detail(request, lesson_id):
    """
    Получение информации об определенном уроке
    """
    lesson = get_object_or_404(Lesson, id=lesson_id)
    serializer = LessonSerializer(lesson)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def lesson_create(request):
    """
    Создание нового урока
    """
    serializer = LessonSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
@permission_classes([permissions.AllowAny])
def lesson_update(request, lesson_id):
    """
    Обновление существующего урока
    """
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    if request.method == 'PUT':
        serializer = LessonSerializer(lesson, data=request.data)
    else:  # PATCH
        serializer = LessonSerializer(lesson, data=request.data, partial=True)
        
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([permissions.AllowAny])
def lesson_delete(request, lesson_id):
    """
    Удаление урока
    """
    lesson = get_object_or_404(Lesson, id=lesson_id)
    lesson.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

def lesson_detail_view(request, lesson_id):
    """
    Отображение детальной информации об уроке в веб-интерфейсе
    """
    lesson = get_object_or_404(Lesson, id=lesson_id)
    context = {
        'lesson': lesson,
    }
    return render(request, 'lessons/lesson_detail.html', context)

def course_lessons_view(request, course_id):
    """
    Отображение списка уроков курса в веб-интерфейсе
    """
    course = get_object_or_404(Course, id=course_id)
    lessons = Lesson.objects.filter(course=course).order_by('order')
    context = {
        'course': course,
        'lessons': lessons,
    }
    return render(request, 'lessons/lesson_list.html', context)
