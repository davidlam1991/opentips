from django.urls import path

from . import views

urlpatterns = [
    path('', views.AllPostsView.as_view(), name='post-main-page'),
    path('create', views.CreatePostView.as_view(), name='post-create-post'),
    path('posts/<slug:slug>', views.SinglePostView.as_view(), name='post-detail'),
    path('posts/<slug:slug>/edit', views.EditPostView.as_view(), name='edit-post'),
    path('report', views.ReportView.as_view(), name='report'),
    path('comments/edit/<int:comment_id>', views.EditCommentView.as_view(), name='edit-comment'),
    path('comments/delete/<int:pk>', views.DeleteCommentView.as_view(), name='delete-comment'),
    path('posts/<slug:slug>/delete/<int:pk>', views.DeletePostView.as_view(), name='delete-post'),
]
