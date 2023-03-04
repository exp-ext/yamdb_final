from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title

from .filters import TitleFilterSet
from .permissions import (IsAdmin, IsAdminOrReadOnly, IsAuthenticated,
                          IsAuthorModeratorAdminOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          CustomUserSerializer, GenreSerializer,
                          ReviewSerializer, SignupSerializer,
                          TitleGetSerializer, TitlePostSerializer,
                          TokenSerializer, UserSerializer)

User = get_user_model()


class SignupViewSet(APIView):
    """
    Получить код подтверждения на переданный email.

    Права доступа: Доступно без токена.

    Использовать имя 'me' в качестве username запрещено.
    Поля email и username должны быть уникальными.
    """
    permission_classes = (AllowAny,)

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        При POST запросе, сохраняет стерилизованные данные в юзера
        и добавляет к нему токен из класса :obj:`PasswordResetTokenGenerator`.
        """
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, _ = User.objects.get_or_create(**serializer.validated_data)
        confirmation_code = default_token_generator.make_token(user)
        self.send_message(user, confirmation_code)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def send_message(user: QuerySet, confirmation_code: str) -> None:
        """
        Отправка юзеру сообщения с confirmation_code.
        - user (:obj:`QuerySet`)
        - confirmation_code (:obj:`str`)
        """
        massage = (
            'Для получения токена и доступа к YaMD '
            'создайте POST-запрос на эндпоинт:\n'
            f'http://{settings.ALLOWED_HOSTS[0]}/api/v1/auth/token/\n'
            'с параметрами\n{\n'
            f'  "username": "{user.username}",\n'
            f'  "confirmation_code": "{confirmation_code}"\n'
            '}'
        )
        send_mail(
            'Код подтверждения для получения токена на YaMDB',
            massage,
            settings.EMAIL_HOST_USER,
            (user.email,)
        )


class TokenViewSet(APIView):
    """
        Получение JWT-токена в обмен на username и confirmation code.

        Права доступа: Доступно без токена.
    """
    permission_classes = (AllowAny,)

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        При POST запросе, на основании стерилизованных данных
        проверяет токен в классе :obj:`PasswordResetTokenGenerator`.

        Возвращает AccessToken.
        """
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        user = get_object_or_404(User, username=username)
        confirmation_code = serializer.validated_data['confirmation_code']
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
        return Response(
            'Неверный Confirmation_code!',
            status=status.HTTP_400_BAD_REQUEST
        )


class UserViewSet(ModelViewSet):
    """
    Пользователи.

    Получение списка всех пользователей: Администратор
        GET: /users/
    Добавление пользователя: Администратор
        Поля email и username должны быть уникальными
        POST: /users/
    Получение пользователя по username: Администратор
        GET: /users/{username}/
    Изменение данных пользователя по username: Администратор
        Поля email и username должны быть уникальными.
        PATCH: /users/{username}/
    Удаление пользователя по username: Администратор
        DELETE: /users/{username}/
    """
    permission_classes = (IsAdmin,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(methods=('GET', 'PATCH'), detail=False,
            permission_classes=(IsAuthenticated,))
    def me(self, request: HttpRequest) -> HttpResponse:
        """
        Получение данных своей учетной записи:
        Любой авторизованный пользователь
            GET: /users/me/
        Изменение данных своей учетной записи:
        Любой авторизованный пользователь
            PATCH: /users/me/
        Поля email и username должны быть уникальными.
        """
        user = get_object_or_404(User, username=request.user.username)
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)
        serializer = CustomUserSerializer(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.GenericViewSet,
                      mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin):
    """
    Категории (типы) произведений.

    Получение списка всех категорий: Доступно без токена
        GET: /categories/
    Добавление новой категории: Администратор
        Поле slug каждой категории должно быть уникальным
        POST: /categories/
    Удаление категории: Администратор
        DELETE: /categories/{slug}/
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter, )
    lookup_field = 'slug'
    search_fields = ('name',)


class GenreViewSet(viewsets.GenericViewSet,
                   mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin):
    """
    Категории жанров.

    Получение списка всех жанров: Доступно без токена
        GET: /genres/
    Добавление жанра: Администратор
        Поле slug каждого жанра должно быть уникальным.
        POST: /genres/
    Удаление жанра: Администратор
        DELETE: /genres/{slug}/
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter, )
    lookup_field = 'slug'
    search_fields = ('name',)


class TitleViewSet(ModelViewSet):
    """
    Произведения, к которым пишут отзывы
    (определённый фильм, книга или песенка).

    Получение списка всех произведений: Доступно без токена
        GET: /titles/
    Добавление произведения: Администратор
        Нельзя добавлять произведения, которые еще не вышли
    (год выпуска не может быть больше текущего).
        При добавлении нового произведения требуется указать уже
        существующие категорию и жанр.
        POST: /titles/
    Получение информации о произведении: Доступно без токена
        GET: /titles/{titles_id}/
    Частичное обновление информации о произведении: Администратор
        PATCH: /titles/{titles_id}/
    Удаление произведения: Администратор
        DELETE /titles/{titles_id}/
    """
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilterSet

    def get_serializer_class(self) -> ModelSerializer:
        if self.action in ('list', 'retrieve'):
            return TitleGetSerializer
        return TitlePostSerializer


class ReviewViewSet(ModelViewSet):
    """
    Отзывы.

    Получение списка всех отзывов: Доступно без токена
        GET: /titles/{title_id}/reviews/
    Добавление нового отзыва: Аутентифицированные пользователи
        POST: /titles/{title_id}/reviews/
    Получение отзыва по id: Доступно без токена
        GET: /titles/{title_id}/reviews/{review_id}/
    Частичное обновление отзыва по id: Автор отзыва, модератор или админ
        PATCH: /titles/{title_id}/reviews/{review_id}/
    Удаление отзыва по id: Автор отзыва, модератор или админ
        DELETE: /titles/{title_id}/reviews/{review_id}/
    """
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

    def get_queryset(self) -> QuerySet:
        """Возвращает отзывы."""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer: ModelSerializer) -> None:
        """Создаёт отзыв в БД."""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    """
    Комментарии к отзывам

    Получение списка всех комментариев к отзыву: Доступно без токена
        GET: /titles/{title_id}/reviews/{review_id}/comments/
    Добавление комментария к отзыву: Аутентифицированные пользователи
        POST: /titles/{title_id}/reviews/{review_id}/comments/
    Получение комментария к отзыву: Доступно без токена
        GET: /titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
    Частичное обновление комментария к отзыву:
    Автор комментария, модератор или админ
        PATCH: /titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
    Удаление комментария к отзыву: Автор комментария, модератор или админ
        DELETE: /titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
    """
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

    def get_queryset(self) -> QuerySet:
        """Возвращает комментарий."""
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer: ModelSerializer) -> None:
        """Создаёт комментарий в БД."""
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)
