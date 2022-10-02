from django.db import models


class Category(models.Model):
    class Meta:
        verbose_name = "жанр"
        verbose_name_plural = "жанры"

    title = models.CharField(max_length=100, verbose_name='Название жанра')

    def __str__(self):
        return self.title


class Film(models.Model):
    class Meta:
        verbose_name = "фильм"
        verbose_name_plural = "фильмы"

    image = models.ImageField(null=True, upload_to='films')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, verbose_name='Категория')
    title = models.CharField(max_length=80, verbose_name='заголовок')
    producer = models.CharField(max_length=30, blank=True, verbose_name='продюссер')
    rate = models.FloatField(default=0, verbose_name='рейтинг')
    time = models.FloatField(default=0, verbose_name="длительность")

    def __str__(self):
        return self.title


class Comments(models.Model):
    class Meta:
        verbose_name = 'коммент'
        verbose_name_plural = "комметарии"
        ordering = ['-created_at']

    films = models.ForeignKey(Film, on_delete=models.CASCADE, null=True, verbose_name='Выберите кино')
    text = models.TextField(verbose_name='Что думаете о фильме?')
    rate_user = models.FloatField(blank=True, verbose_name='оценка')
    created_at = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return self.text


#
# class Tags(models.Model):
#     class
