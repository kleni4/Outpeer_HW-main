from rest_framework import permissions

class IsManagerOrReadOnly(permissions.BasePermission):
    """
    Пользовательское разрешение, которое позволяет только менеджерам создавать/редактировать/удалять уроки,
    а просматривать могут все аутентифицированные пользователи.
    """
    def has_permission(self, request, view):
        # Проверяем аутентификацию
        if not request.user.is_authenticated:
            return False
            
        # Разрешаем GET запросы для всех аутентифицированных пользователей
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Для остальных методов (POST, PUT, DELETE) проверяем роль менеджера
        return request.user.role == 'manager'

    def has_object_permission(self, request, view, obj):
        # Проверяем аутентификацию
        if not request.user.is_authenticated:
            return False
            
        # Разрешаем GET запросы для всех аутентифицированных пользователей
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Для остальных методов (POST, PUT, DELETE) проверяем роль менеджера
        return request.user.role == 'manager'
