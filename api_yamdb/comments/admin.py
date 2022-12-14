from django.contrib import admin

from titles.models import Genre, Title, GenreTitle, Category

admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(GenreTitle)
admin.site.register(Category)
