from rest_framework import serializers
from titles.models import Title, Genre, Category, Review, Comment
from users.models import User


class CategoryField(serializers.SlugRelatedField):

    def to_representation(self, obj):
        return CategorySerializer(obj).data


class GenreField(serializers.SlugRelatedField):

    def to_representation(self, obj):
        return GenreSerializer(obj).data


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreField(required=True,
                       many=True,
                       slug_field='slug',
                       queryset=Genre.objects.all())
    category = CategoryField(slug_field='slug',
                             queryset=Category.objects.all(),
                             required=False)

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')
        model = Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        fields = '__all__'
        model = Comment


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')

    def validate_username(self, username):
        if username in 'me':
            raise serializers.ValidationError('Использовать имя me запрещено')
        return username


class TokenSerializer(serializers.Serializer):
    username = serializers.RegexField(regex=r'^[\w.@+-]+$',
                                      max_length=150,
                                      required=True)
    confirmation_code = serializers.CharField(max_length=254, required=True)


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания объекта класса User."""

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        """Запрещает пользователям присваивать себе имя me
        и использовать повторные username и email."""
        if data.get('username') == 'me':
            raise serializers.ValidationError('Использовать имя me запрещено')
        if User.objects.filter(username=data.get('username')):
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует')
        if User.objects.filter(email=data.get('email')):
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует')
        return data
