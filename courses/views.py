from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Course
from .serializers import CourseSerializer, CourseCreateUpdateSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .permissions import IsManager

User = get_user_model()

@login_required
def course_list(request):
    courses = Course.objects.all().select_related('teacher').prefetch_related('students')
    return render(request, 'courses/course_list.html', {'courses': courses})

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course.objects.select_related('teacher').prefetch_related('students'), id=course_id)
    return render(request, 'courses/course_detail.html', {'course': course})

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsManager]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CourseCreateUpdateSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(teacher=self.request.user)
        else:
            serializer.save()

    @action(detail=True, methods=['post'])
    def add_student(self, request, pk=None):
        course = self.get_object()
        student_id = request.data.get('student_id')
        
        if not student_id:
            return Response(
                {'error': 'Необходимо указать student_id'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            student = User.objects.get(id=student_id, role='student')
        except User.DoesNotExist:
            return Response(
                {'error': 'Студент не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

        if course.students.count() >= course.max_students:
            return Response(
                {'error': 'Достигнуто максимальное количество студентов'},
                status=status.HTTP_400_BAD_REQUEST
            )

        course.students.add(student)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def remove_student(self, request, pk=None):
        course = self.get_object()
        student_id = request.data.get('student_id')
        
        if not student_id:
            return Response(
                {'error': 'Необходимо указать student_id'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            student = User.objects.get(id=student_id, role='student')
        except User.DoesNotExist:
            return Response(
                {'error': 'Студент не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

        course.students.remove(student)
        return Response(status=status.HTTP_200_OK)
