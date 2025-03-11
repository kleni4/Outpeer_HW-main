from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from datetime import timedelta 
import random

# Create your models here.

class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'student', 'Студент'
        TEACHER = 'teacher', 'Преподаватель'
        MANAGER = 'manager', 'Менеджер'
        ADMINISTRATOR = 'administrator', 'Администратор'

    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT
    )
    is_email_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, null=True, blank=True)
    verification_code_created_at = models.DateTimeField(null=True, blank=True)
    
    # Поля только для студентов
    attendance_percentage = models.FloatField(
        verbose_name='Посещаемость (%)',
        default=0,
        help_text='Процент посещаемости занятий'
    )
    lessons_count = models.IntegerField(
        verbose_name='Количество уроков',
        default=0,
        help_text='Общее количество уроков'
    )
    total_score = models.IntegerField(
        verbose_name='Общий балл',
        default=0,
        help_text='Общий балл за все уроки'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def generate_verification_code(self):
        """
        Генерю  6-знач код
        """
        self.verification_code = str(random.randint(100000, 999999))
        self.verification_code_created_at = now()
        self.save()
        return self.verification_code

    def save(self, *args, **kwargs):
        # Если пользователь не студент, обнуляем специфичные для студента поля
        if self.role != self.Role.STUDENT:
            self.attendance_percentage = 0
            self.lessons_count = 0
            self.total_score = 0
        super().save(*args, **kwargs)