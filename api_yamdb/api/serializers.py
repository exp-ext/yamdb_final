from collections import OrderedDict

from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from rest_framework.serializers import (CharField, CurrentUserDefault,
                                        IntegerField, ModelSerializer,
                                        SlugRelatedField, ValidationError)
from reviews.models import Category, Comment, Genre, Review, Title
from reviews.validators import validate_username

User = get_user_model()


class SignupSerializer(ModelSerializer):
    """Сериалайзер авторизации."""

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_email(self, value: str) -> str:
        """Проверка email на валидность."""
        try:
            validate_email(value)
        except ValidationError as error:
            raise ValidationError(
                f'Email не валидно: {error}'
            )
        return value

    def validate_username(self, value: str) -> str:
        """Проверка на me и на валидное username."""
        try:
            validate_username(value)
        except ValidationError as error:
            raise ValidationError(
                f'username не валидно: {error}'
            )
        return value


class TokenSerializer(ModelSerializer):
    """Сериалайзер получения токена."""
    confirmation_code = CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def validate_username(self, value: str) -> str:
        """Проверка на валидное username."""
        try:
            validate_username(value)
        except ValidationError as error:
            raise ValidationError(
                f'username не валидно: {error}'
            )
        return value


class UserSerializer(ModelSerializer):
    """Сериалайзер модели User для админа."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate_username(self, value: str) -> str:
        """Проверка на валидное username."""
        try:
            validate_username(value)
        except ValidationError as error:
            raise ValidationError(
                f'username не валидно: {error}'
            )
        return value


class CustomUserSerializer(UserSerializer):
    """Сериалайзер модели User для пользователя."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)

    def validate_username(self, value: str) -> str:
        """Проверка на валидное username."""
        try:
            validate_username(value)
        except ValidationError as error:
            raise ValidationError(
                f'username не валидно: {error}'
            )
        return value


class CategorySerializer(ModelSerializer):
    """Сериалайзер модели Category."""

    class Meta:
        model = Category
        exclude = ('id', )


class GenreSerializer(ModelSerializer):
    """Сериалайзер модели Genre."""

    class Meta:
        model = Genre
        exclude = ('id', )


class TitleGetSerializer(ModelSerializer):
    """Сериалайзер модели Title для чтения."""
    category = CategorySerializer(read_only=True, many=False)
    genre = GenreSerializer(read_only=True, many=True)
    rating = IntegerField(max_value=10, min_value=0)

    class Meta:
        model = Title
        fields = '__all__'


class TitlePostSerializer(ModelSerializer):
    """Сериалайзер модели Title для редактирования."""
    category = SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(ModelSerializer):
    """Сериалайзер модели Review."""
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=CurrentUserDefault()
    )
    title = SlugRelatedField(
        slug_field='name',
        read_only=True
    )

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data: OrderedDict) -> OrderedDict:
        """Защита от повторов отзыва от пользователя."""
        if self.context['request'].method != 'POST':
            return data
        author = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        if Review.objects.filter(author=author, title_id=title_id).exists():
            raise ValidationError('Отзыв уже был ранее')
        return data


class CommentSerializer(ModelSerializer):
    """Сериалайзер модели Comment."""
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=CurrentUserDefault()
    )
    review = SlugRelatedField(
        slug_field='text',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
