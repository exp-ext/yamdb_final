from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorModeratorAdminOrReadOnly(BasePermission):
    message = 'Изменение чужого контента запрещено!'

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or (request.user.is_moderator
                or request.user.is_admin)
        )


class IsAuthenticated(BasePermission):
    message = 'Доступно только для после аутентификации!'

    def has_permission(self, request, view):
        return request.user.is_authenticated


class IsAdmin(BasePermission):
    message = 'Доступно только для администратора!'

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )


class IsAdminOrReadOnly(BasePermission):
    message = 'Изменение доступно только для администратора!'

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (request.user.is_authenticated
                and request.user.is_admin)
        )
