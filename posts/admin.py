from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Post, Comment, Report

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ("restaurant_name", "address", "release_date",)
    prepopulated_fields = {"slug": ("restaurant_name", "address")}


class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "content", "date_posted", "CommentPost", "parent")


class ReportAdmin(admin.ModelAdmin):
    list_display = ("reported_by", "content", "link", "reason", "detail", "date_reported")
    list_filter = ("date_reported", "reason")


admin.site.register(Post, PostAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Report, ReportAdmin)
