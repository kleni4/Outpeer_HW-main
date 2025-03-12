from django.db import models
from django.conf import settings
from courses.models import Course

class Lesson(models.Model):
    LESSON_TYPE_CHOICES = [
        ('lecture', 'Лекция'),
        ('practice', 'Практическое занятие'),
        ('seminar', 'Семинар'),
        ('test', 'Тест'),
    ]

    title = models.CharField(max_length=200, verbose_name='Название урока')
    description = models.TextField(verbose_name='Краткое описание урока')
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Курс'
    )
    lesson_type = models.CharField(
        max_length=20,
        choices=LESSON_TYPE_CHOICES,
        default='lecture',
        verbose_name='Тип занятия'
    )
    content = models.TextField(
        verbose_name='Содержание урока',
        help_text='Основной текст урока'
    )
    order = models.PositiveIntegerField(
        verbose_name='Порядковый номер',
        help_text='Порядковый номер урока в курсе'
    )
    duration = models.PositiveIntegerField(
        verbose_name='Продолжительность (в минутах)',
        default=60
    )
    additional_materials = models.TextField(
        verbose_name='Дополнительные материалы',
        blank=True,
        null=True,
        help_text='Ссылки на дополнительные материалы, литературу и т.д.'
    )
    video_url = models.URLField(
        verbose_name='Ссылка на видео',
        blank=True,
        null=True,
        help_text='Ссылка на видеозапись урока'
    )
    presentation_url = models.URLField(
        verbose_name='Ссылка на презентацию',
        blank=True,
        null=True,
        help_text='Ссылка на презентацию к уроку'
    )
    homework = models.TextField(
        verbose_name='Домашнее задание',
        blank=True,
        null=True,
        help_text='Задание для самостоятельной работы'
    )
    homework_deadline = models.DateTimeField(
        verbose_name='Срок сдачи ДЗ',
        blank=True,
        null=True,
        help_text='Крайний срок сдачи домашнего задания'
    )
    max_score = models.PositiveSmallIntegerField(
        verbose_name='Максимальный балл',
        default=100,
        help_text='Максимальный балл за урок'
    )
    is_required = models.BooleanField(
        default=True,
        verbose_name='Обязательный урок',
        help_text='Является ли урок обязательным для прохождения'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['course', 'order']
        unique_together = ['course', 'order']

    def __str__(self):
        return f"{self.course.title} - Урок {self.order}: {self.title}"

class Attendance(models.Model):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='attendances',
        verbose_name='Урок'
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='attendances',
        verbose_name='Студент'
    )
    is_present = models.BooleanField(default=False, verbose_name='Присутствовал')
    homework_file = models.FileField(
        upload_to='homework_files/',
        null=True,
        blank=True,
        verbose_name='Файл с домашним заданием'
    )
    homework_completed = models.BooleanField(
        default=False,
        verbose_name='Домашнее задание выполнено'
    )
    homework_submitted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Время сдачи домашнего задания'
    )
    grade = models.CharField(
        max_length=2,
        null=True,
        blank=True,
        verbose_name='Оценка'
    )
    score = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name='Баллы'
    )
    comment = models.TextField(
        null=True,
        blank=True,
        verbose_name='Комментарий преподавателя'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Посещаемость'
        verbose_name_plural = 'Посещаемость'
        unique_together = ['lesson', 'student']

    def __str__(self):
        return f"{self.student.username} - {self.lesson.title}"

    def clean(self):
        if self.score and self.score > self.lesson.max_score:
            raise models.ValidationError({
                'score': f'Балл не может быть больше максимального ({self.lesson.max_score})'
            })
