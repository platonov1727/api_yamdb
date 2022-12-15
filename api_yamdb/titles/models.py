from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ManyToManyField(Genre,
                                   through='GenreTitle')
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='titles')

    def __str__(self):
        return self.text


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} в жанре {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='reviews')
    text = models.TextField(max_length=4000)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='rewiews')
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)
    score = models.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)])


class Comment(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField(max_length=500)
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name='comments')
