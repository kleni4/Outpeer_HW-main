from rest_framework import permissions

class IsManager(permissions.BasePermission):
    """
    Пользовательское разрешение, которое позволяет только менеджерам выполнять действия.
    """
    def has_permission(self, request, view):
        # Разрешаем GET запросы для аутентифицированных пользователей
        if request.method in permissions.SAFE_METHODS and request.user.is_authenticated:
            return True
            
        # Проверяем, является ли пользователь менеджером
        return request.user.is_authenticated and request.user.role == 'manager'

    def has_object_permission(self, request, view, obj):
        # Разрешаем GET запросы для аутентифицированных пользователей
        if request.method in permissions.SAFE_METHODS and request.user.is_authenticated:
            return True
            
        # Проверяем, является ли пользователь менеджером
        return request.user.is_authenticated and request.user.role == 'manager'
