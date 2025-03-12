from rest_framework import serializers
from .models import Lesson, Attendance
from users.serializers import UserSerializer
from django.db import models

class LessonSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    lesson_type_display = serializers.CharField(source='get_lesson_type_display', read_only=True)
    
    class Meta:
        model = Lesson
        fields = [
            'id', 'title', 'description', 'course', 'course_title',
            'lesson_type', 'lesson_type_display', 'content', 'order',
            'duration', 'additional_materials', 'video_url',
            'presentation_url', 'homework', 'homework_deadline',
            'max_score', 'is_required', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        # Проверка порядкового номера урока
        if self.instance is None:  # Creating new lesson
            course = data.get('course')
            order = data.get('order')
            if Lesson.objects.filter(course=course, order=order).exists():
                raise serializers.ValidationError(
                    f"Урок с номером {order} уже существует в этом курсе"
                )
        
        # Проверка сроков домашнего задания
        homework = data.get('homework')
        homework_deadline = data.get('homework_deadline')
        if homework and not homework_deadline:
            raise serializers.ValidationError(
                "Для домашнего задания необходимо указать срок сдачи"
            )
        
        # Проверка длительности урока
        duration = data.get('duration')
        if duration and duration < 15:
            raise serializers.ValidationError(
                "Длительность урока должна быть не менее 15 минут"
            )
        
        return data

    def create(self, validated_data):
        # Если порядок не указан, устанавливаем следующий доступный
        if 'order' not in validated_data:
            course = validated_data.get('course')
            last_lesson = Lesson.objects.filter(course=course).order_by('-order').first()
            validated_data['order'] = (last_lesson.order + 1) if last_lesson else 1

        # Если тип урока - тест, устанавливаем дополнительные параметры
        if validated_data.get('lesson_type') == 'test':
            if 'duration' not in validated_data:
                validated_data['duration'] = 45  # стандартное время для теста
            if 'is_required' not in validated_data:
                validated_data['is_required'] = True  # тесты всегда обязательны

        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Проверяем изменение порядкового номера
        new_order = validated_data.get('order')
        if new_order and new_order != instance.order:
            # Если урок перемещается вниз
            if new_order > instance.order:
                Lesson.objects.filter(
                    course=instance.course,
                    order__gt=instance.order,
                    order__lte=new_order
                ).update(order=models.F('order') - 1)
            # Если урок перемещается вверх
            else:
                Lesson.objects.filter(
                    course=instance.course,
                    order__gte=new_order,
                    order__lt=instance.order
                ).update(order=models.F('order') + 1)

        # Если меняется тип урока на тест
        if validated_data.get('lesson_type') == 'test' and instance.lesson_type != 'test':
            validated_data['is_required'] = True  # тесты всегда обязательны
            if 'duration' not in validated_data:
                validated_data['duration'] = 45  # стандартное время для теста

        return super().update(instance, validated_data)

class AttendanceSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)
    homework_file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Attendance
        fields = [
            'id', 'lesson', 'lesson_title', 'student', 'is_present',
            'homework_completed', 'homework_file', 'homework_file_url',
            'homework_submitted_at', 'grade', 'score', 'comment',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'homework_file_url']

    def get_homework_file_url(self, obj):
        if obj.homework_file:
            return self.context['request'].build_absolute_uri(obj.homework_file.url)
        return None

    def validate_grade(self, value):
        if value is not None and not (1 <= value <= 5):
            raise serializers.ValidationError(
                "Оценка должна быть от 1 до 5"
            )
        return value

    def validate_score(self, value):
        if value is not None:
            lesson = self.instance.lesson if self.instance else self.initial_data.get('lesson')
            if value > lesson.max_score:
                raise serializers.ValidationError(
                    f"Балл не может быть больше максимального ({lesson.max_score})"
                )
        return value 