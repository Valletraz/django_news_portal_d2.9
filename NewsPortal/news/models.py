from django.db import models
from django.contrib.auth.models import User

NEWS = 'NW'
ARTICLE = 'AR'
CATEGORY_CHOICES = (
    (NEWS, 'Новость'),
    (ARTICLE, 'Статья')
)


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.IntegerField(
        default=0)  # рейтинг пользователя. Ниже будет дано описание того, как этот рейтинг можно посчитать.

    def update_rating(self):
        self.ratingAuthor = 0
        self.save()

        for pa in Post.objects.filter(author=self.id):
            self.ratingAuthor += int(pa.rating) * 3
            self.save()

        for ct in Comment.objects.filter(commentUser=self.id):
            self.ratingAuthor += int(ct.rating)
            self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    type = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    time_create = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    text_header = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'

    def __str__(self):
        return f'{self.text_header}: {self.time_create} - {self.text}'

    def length(self):
        return pk.count()



class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

# Create your models here.
