from rest_framework import serializers
from .models import Course
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'role']

class CourseSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)
    students = UserSerializer(many=True, read_only=True)
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'teacher', 'students', 
                 'start_date', 'end_date', 'max_students', 'is_active',
                 'student_count', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def get_student_count(self, obj):
        return obj.students.count()

class CourseCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['title', 'description', 'teacher', 'start_date', 
                 'end_date', 'max_students', 'is_active']

    def validate(self, data):
        if 'start_date' in data and 'end_date' in data:
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError(
                    "Дата окончания должна быть позже даты начала"
                )
        return data 