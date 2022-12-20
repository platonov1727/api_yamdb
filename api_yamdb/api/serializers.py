from rest_framework import serializers
from titles.models import Title, Genre, Category
from reviews.models import Review, Comment
from users.models import User
from rest_framework.validators import UniqueValidator
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError


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
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


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
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True)

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError('Только один отзыв на произведение!')
        return data

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(slug_field='text', read_only=True)
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')
        read_only_fields = ('role', )

    def validate_username(self, username):
        if username in 'me':
            raise serializers.ValidationError('Использовать имя me запрещено')
        return username


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class RegisterDataSerializer(serializers.Serializer):
    username = serializers.RegexField(regex=r'^[\w.@+-]+$', max_length=150)
    email = serializers.EmailField(required=True, max_length=254)

    def validate(self, data):
        """Запрещает пользователям присваивать себе имя me
        и использовать повторные username и email."""
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Использоваться имя me запрещено')
        if User.objects.filter(username=data.get('username'),
                               email=data.get('email')).exists():
            return data
        else:
            if User.objects.filter(username=data.get('username')):
                raise serializers.ValidationError(
                    'Пользователь с таким username уже существует')
            if User.objects.filter(email=data.get('email')):
                raise serializers.ValidationError(
                    'Пользователь с таким Email уже существует')
        return data

    def create(self, validated_data):
        User.objects.create(username=validated_data['username'],
                            email=validated_data['email'])
        return User(**validated_data)

    class Meta:
        model = User
        fields = ('username', 'email')


class AdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')

    def validate_username(self, username):
        if username in 'me':
            raise serializers.ValidationError('Использовать имя me запрещено')
        return username


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(source='reviews__score__avg',
                                      read_only=True)
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')
