from django.contrib import admin
from .models import Title, Genre, Category, GenreTitle
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class TitleResource(resources.ModelResource):

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'category',
        )


class TitleAdmin(ImportExportModelAdmin):
    resource_classes = [TitleResource]
    # Перечисляем поля, которые должны отображаться в админке
    list_display = (
        'id',
        'name',
        'year',
        'category',
    )

    # Добавляем интерфейс для поиска
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class GenreResource(resources.ModelResource):

    class Meta:
        model = Genre
        fields = (
            'id',
            'name',
            'slug',
        )


class GenreAdmin(ImportExportModelAdmin):
    resource_classes = [GenreResource]
    # Перечисляем поля, которые должны отображаться в админке
    list_display = (
        'id',
        'name',
        'slug',
    )

    # Добавляем интерфейс для поиска
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class CategoryResource(resources.ModelResource):

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'slug',
        )


class CategoryAdmin(ImportExportModelAdmin):
    resource_classes = [CategoryResource]
    # Перечисляем поля, которые должны отображаться в админке
    list_display = (
        'id',
        'name',
        'slug',
    )

    # Добавляем интерфейс для поиска
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class GenreTitleResource(resources.ModelResource):

    def get_export_headers(self):
        headers = super().get_export_headers()
        for i, h in enumerate(headers):
            if h == 'genre_id':
                headers[i] = 'genre'
            if h == 'title_id':
                headers[i] = 'title'
        return headers

    class Meta:
        model = GenreTitle
        fields = (
            'id',
            'genre',
            'title',
        )


class GenreTitleAdmin(ImportExportModelAdmin):
    resource_classes = [GenreTitleResource]
    # Перечисляем поля, которые должны отображаться в админке
    list_display = (
        'id',
        'genre',
        'title',
    )

    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(GenreTitle, GenreTitleAdmin)
