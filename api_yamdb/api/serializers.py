from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from titles.models import Title, Genre, Category, Review, Comment, GenreTitle
from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        required_fields = ('email', 'username', )
        ref_name = 'ReadOnlyUsers'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(required=True, many=True)
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )

    class Meta:
        fields = ('name', 'year', 'description', 'genre', 'category')
        model = Title


class TitleCreateUpdateSerializer(serializers.ModelSerializer):
    genre = serializers.ListField(required=True)
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )

    class Meta:
        fields = ('name', 'year', 'description', 'genre', 'category')
        model = Title

    def create(self, validated_data):
        if 'genre' not in self.initial_data:
            print('no genre')
            title = Title.objects.create(**validated_data)
            return title
        else:
            genres = validated_data.pop('genre')
            title = Title.objects.create(**validated_data)
            for genre in genres:
                print(genre)
                current_genre, status = Genre.objects.get_or_create(
                    slug=genre
                )
                GenreTitle.objects.create(
                    genre=current_genre, title=title
                )
                return title

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.year = validated_data.get('year', instance.year)
        instance.discription = validated_data.get(
            'discription', instance.discription
        )
        instance.category = validated_data.get('category', instance.category)
        if 'genre' in validated_data:
            genre_data = validated_data.pop('genre')
            lst = []
            for genre in genre_data:
                current_genre, status = Genre.objects.get_or_create(
                    slug=genre
                )
                lst.append(current_genre)
            instance.genre.set(lst)

        instance.save()
        return instance


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


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
