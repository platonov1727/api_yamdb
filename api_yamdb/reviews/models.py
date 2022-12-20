from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User
from titles.models import Title


class Review(models.Model):
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='rewiews')
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)
    score = models.PositiveSmallIntegerField(
        'Рейтинг', validators=[MinValueValidator(1),
                               MaxValueValidator(10)])

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'],
                                    name='unique_review'),
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField(max_length=500)
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name='comments')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['pub_date']
