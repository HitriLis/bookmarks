from django.db import models
from users.models import User


class LinkType(models.Model):
    name = models.CharField(max_length=250, verbose_name="Название")
    type = models.CharField(max_length=150, verbose_name="Тип")

    def __str__(self):
        return self.name or f'LinkType Id:{self.id}'

    class Meta:
        verbose_name = 'Тип ссылки'
        verbose_name_plural = 'Тип ссылки'


class Bookmarks(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    link_page = models.URLField(verbose_name="Ссылка на страницу")
    link_type = models.ForeignKey(
        LinkType,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Тип ссылки"
    )
    page_title = models.TextField(null=True, blank=True, verbose_name="Заголовок страницы")
    short_description = models.TextField(null=True, blank=True, verbose_name="Краткое описание")
    picture = models.URLField(verbose_name="Картинка превью")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f'Bookmarks Id:{self.id}'

    @property
    def type(self):
        if self.link_type:
            return self.link_type.type
        return None

    @property
    def type_name(self):
        if self.link_type:
            return self.link_type.name
        return None

    class Meta:
        verbose_name = 'Закладка'
        verbose_name_plural = 'Закладки'


class CollectionBookmarks(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    name = models.CharField(null=True, blank=True, max_length=250, verbose_name="Название")
    short_description = models.CharField(null=True, blank=True, max_length=300, verbose_name="Краткое описание")
    bookmarks = models.ManyToManyField(
        Bookmarks,
        blank=True,
        verbose_name="Закладки",
        related_name='collection'
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name or f'Collection Id:{self.id}'

    class Meta:
        verbose_name = 'Коллекция'
        verbose_name_plural = 'Коллекции'
