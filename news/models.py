from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField('Рейтинг', default=0)
    photo = models.ImageField('Фото', upload_to='authors/')

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def update_rating(self):
        news_rating = Post.objects.filter(author=self).aggregate(total_news=Sum('rating') * 3)['total_news']
        comment_rating = Comment.objects.filter(user=self.user).aggregate(total_comment=Sum('rating'))['total_comment']
        to_author_rating = Comment.objects.filter(post__author_id=self.id).aggregate(total_to_author=Sum('rating'))['total_to_author']
        self.rating = news_rating + comment_rating + to_author_rating
        self.save()


class Category(models.Model):
    name = models.CharField('Категория', max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, verbose_name='Подписчики')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    CHAPTER_CHOICES = (
        ('N', 'news'),
        ('A', 'article')
    )
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, related_name='post_author', null=True)
    chapter = models.CharField('Раздел', max_length=10, choices=CHAPTER_CHOICES, default='N')
    time_in = models.DateTimeField('Время добавления', auto_now_add=True)
    categories = models.ManyToManyField(Category, verbose_name='Категория')
    header = models.CharField('Заголовок', max_length=255, blank=False, null=False)
    content = models.TextField('Новость', blank=False, null=False)
    rating = models.IntegerField('Рейтинг', default=0)
    billboard = models.ImageField('Превью', upload_to='billboards/')
    draft = models.BooleanField('Черновик', default=False)

    def __str__(self):
        return f'{self.header[:20]}'

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.id})

    class Meta:
        verbose_name = 'Посты'
        verbose_name_plural = 'Посты'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.content[:124]}...'

    def get_comment(self):
        return self.comment_set.filter(parent__isnull=True)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    content = models.TextField('Комментарий', blank=False, null=False)
    rating = models.IntegerField('Рейтинг', default=0)
    parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True)
    time_in = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return f'{self.user} - {self.post}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Коментарии'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class Newsletter(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email