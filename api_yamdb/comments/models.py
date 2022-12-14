from django.db import models
from users.models import User


class Review(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField(max_length=4000)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='rewiews')
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)


class Comment(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField(max_length=500)
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name='comments')
