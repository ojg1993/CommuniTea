from django.db import models
from django.utils.text import slugify

from accounts.models import CustomUser
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=150)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category-posts", args=[self.slug])


class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150)
    content = models.TextField()
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        Category, related_name="category_post", on_delete=models.PROTECT
    )
    writer = models.ForeignKey(
        CustomUser, related_name="user_post", on_delete=models.CASCADE
    )
    hits = models.IntegerField(default=0)

    def increase_hits(self):
        self.hits += 1
        self.save()

    def __str__(self):
        return f"[{str(self.category)}] {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    content = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    commenter = models.ForeignKey(
        CustomUser, related_name="user_comment", on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post, related_name="post_comment", on_delete=models.CASCADE
    )

    def get_username(self):
        email = self.commenter.email
        username = email.split("@")[0]
        return username

    def get_title(self):
        return self.content[:15] + "  ..."

    def __str__(self):
        return f"[{self.post.id}, {self.get_username()}] {self.get_title()}"
