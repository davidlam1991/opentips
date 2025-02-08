from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import timedelta, datetime
from django.utils.timesince import timesince

from users.models import CustomUser
from .choices import FOOD_TYPE_CHOICES, JOB_TYPE_CHOICES, TIPS_SITUATION_CHOICES, REASON_CHOICES

# Create your models here.


class Post(models.Model):
    restaurant_name = models.CharField(verbose_name="Restaurant", max_length=255, null=True, blank=True)
    address = models.CharField(verbose_name="Address", db_index=True, max_length=150, null=True, blank=True)
    tips_situation = models.CharField(verbose_name="Tips Situation", max_length=10, choices=TIPS_SITUATION_CHOICES, null=True, blank=True)
    tips_sit_detail = models.CharField(verbose_name="Describe", max_length=100, null=True, blank=True)
    food_type = models.CharField(verbose_name="Food Type", max_length=3, choices=FOOD_TYPE_CHOICES, null=True, blank=True)
    job_type = models.CharField(verbose_name="Job Type", max_length=3, choices=JOB_TYPE_CHOICES, null=True, blank=True)
    date = models.DateField(verbose_name="Date")
    content = models.TextField(verbose_name="Detail", max_length=1000)
    release_date = models.DateTimeField(verbose_name="Now")
    slug = models.SlugField(default="", max_length=100, null=True, blank=True)
    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="posts", null=True, blank=True)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.date += timedelta(days=1)
        count_address = Post.objects.filter(address=self.address).count()
        while True:
            self.slug = slugify(f"{self.restaurant_name} {self.address} {count_address}")
            if not Post.objects.filter(slug=self.slug).exists():
                super().save(*args, **kwargs)
                break
            count_address += 1

    def shortened_release_date(self):
        now = datetime.now(self.release_date.tzinfo)
        time_diff = timesince(self.release_date, now).split(",")[0]
        return f"{time_diff} ago"


class Comment(models.Model):
    CommentPost = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(verbose_name="Comment", null=True, blank=True)
    date_posted = models.DateTimeField(verbose_name="Created By", auto_now_add=True, null=True, blank=True)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies")
    quoted_text = models.TextField(blank=True, null=True)

    class Meta:
        ordering=['-date_posted']

    def __str__(self):
        return f"{str(self.author)} comment {str(self.content)}"

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.CommentPost.slug}) + f"#comment-{self.id}"

    @property
    def children(self):
        return Comment.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False


class Report(models.Model):
    reported_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    content = models.CharField(max_length=1000, null=True, blank=True)
    link = models.CharField(max_length=1000, null=True, blank=True)
    reason = models.CharField(max_length=50, choices=REASON_CHOICES, null=True, blank=True)
    detail = models.TextField(max_length=1000, null=True, blank=True)
    date_reported = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"Report by {self.reported_by}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


